# -------------------------------------------------------------------------------------------
# Name: MultiLayerPlanner
# Description: Controller-neutral Multilayer seam grouping, ordering, flattening, and direction
#              resolution. Consumed by both the E2-native and KUKA AML projections so ordering
#              logic exists exactly once. See docs/ctrl-specific/KUKA/spec/multilayer.md
#              sections 6 and 10.
# Debug info: E2@localhost:5254
# Author: Cenit AG
# Changelog:
#     Version: 1.0
#        Changed by:
#        Date:
#
# -------------------------------------------------------------------------------------------
import sys, inspect, os
sys.dont_write_bytecode = True
sys.path.append(str(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))))

from dataclasses import dataclass
from enum import Enum
from typing import Sequence

import MultiLayerMetadata
import MultiLayerDiagnostics as diag


class Direction(Enum):
    FORWARD = "Forward"
    REVERSE = "Reverse"


class SequenceMode(Enum):
    COMPLETE_SEAM = MultiLayerMetadata.SEQUENCE_MODE_COMPLETE_SEAM
    LAYER_BEAD_ACROSS_SEAMS = MultiLayerMetadata.SEQUENCE_MODE_LAYER_BEAD_ACROSS_SEAMS


class DirectionMode(Enum):
    SAME_DIRECTION = MultiLayerMetadata.DIRECTION_MODE_SAME
    ALTERNATING = MultiLayerMetadata.DIRECTION_MODE_ALTERNATING
    ZIGZAG = MultiLayerMetadata.DIRECTION_MODE_ZIGZAG


class DirectionOverride(Enum):
    INHERIT_PROGRAM = MultiLayerMetadata.DIRECTION_OVERRIDE_INHERIT
    FORWARD = MultiLayerMetadata.DIRECTION_OVERRIDE_FORWARD
    REVERSE = MultiLayerMetadata.DIRECTION_OVERRIDE_REVERSE


@dataclass(frozen=True)
class PassInput:
    """One resolved operation's stable Multilayer metadata, ready for planning.

    seam_ordinal is deliberately not part of the input: it is derived from
    first-appearance order across all inputs (section 10.1), not supplied
    per-pass, so it cannot be inconsistent within one seam.
    """
    seam_uuid: str
    wps_main_id: int
    wps_sub_id: int
    wps_name: str
    layer: int
    bead: int
    source_operation: object
    source_operation_ordinal: int
    recipe_fingerprint: str
    direction_override: DirectionOverride = DirectionOverride.INHERIT_PROGRAM


@dataclass(frozen=True)
class MultilayerPass:
    seam_uuid: str
    seam_ordinal: int
    wps_main_id: int
    wps_sub_id: int
    wps_name: str
    layer: int
    bead: int
    source_operation: object
    source_operation_ordinal: int
    flat_index_in_seam: int
    flat_index_in_program: int
    direction: Direction
    recipe_fingerprint: str


@dataclass(frozen=True)
class SeamSensingPlan:
    """Sensing envelope placeholder; populated once technology sensing wiring lands (section 11)."""
    has_touch_sensing: bool = False
    has_seam_finding: bool = False
    has_seam_tracking: bool = False


@dataclass(frozen=True)
class MultilayerSeam:
    seam_uuid: str
    seam_ordinal: int
    passes: tuple
    sensing: SeamSensingPlan


@dataclass(frozen=True)
class MultilayerPlan:
    schema_version: int
    output_mode: str
    sequence_mode: str
    direction_mode: str
    seams: tuple
    execution: tuple
    diagnostics: tuple


def group_by_seam(pass_inputs: Sequence[PassInput]):
    """Group by seam UUID, preserving first-appearance order (section 10.1).

    Returns a list of (seam_uuid, [PassInput, ...]) in first-appearance order.
    """
    order = []
    groups = {}
    for item in pass_inputs:
        if item.seam_uuid not in groups:
            groups[item.seam_uuid] = []
            order.append(item.seam_uuid)
        groups[item.seam_uuid].append(item)
    return [(uuid, groups[uuid]) for uuid in order]


def sort_seam_passes(entries: Sequence[PassInput]):
    """Sort by (layer, bead, source_operation_ordinal); section 10.2."""
    return sorted(entries, key=lambda p: (p.layer, p.bead, p.source_operation_ordinal))


def find_duplicate_layer_bead(entries: Sequence[PassInput]):
    """Sorted list of (layer, bead) pairs that appear more than once in one seam."""
    counts = {}
    for item in entries:
        key = (item.layer, item.bead)
        counts[key] = counts.get(key, 0) + 1
    return sorted(key for key, count in counts.items() if count > 1)


def complete_seam_order(seam_groups):
    """Concatenate seams in original order; passes already sorted (section 10.3)."""
    execution = []
    for _, entries in seam_groups:
        execution.extend(entries)
    return execution


def layer_bead_across_seams_order(seam_groups):
    """Iterate sorted (layer, bead) coordinates, then seams in original order.

    Missing coordinates are skipped without renumbering the remaining WPS
    metadata (section 10.3). Not yet enabled for production use (section 10.4).
    """
    coordinates = sorted({(item.layer, item.bead) for _, entries in seam_groups for item in entries})
    by_seam_coordinate = {}
    for seam_uuid, entries in seam_groups:
        for item in entries:
            by_seam_coordinate[(seam_uuid, item.layer, item.bead)] = item

    execution = []
    for layer, bead in coordinates:
        for seam_uuid, _ in seam_groups:
            item = by_seam_coordinate.get((seam_uuid, layer, bead))
            if item is not None:
                execution.append(item)
    return execution


def resolve_direction(execution_ordinal: int, layer_position: int, direction_mode: DirectionMode, override: DirectionOverride) -> Direction:
    """Compute pass direction (section 10.5).

    ZigZag alternates continuously by flat execution position across the whole program (the
    original Alternating behavior); no known KUKA AML option pack can render this, it is for
    controllers/E2 native paths with true per-pass zigzag capability.
    Alternating flips once per distinct layer number within a seam - layer_position is that
    layer's 0-based rank among the seam's own distinct layer numbers, not the raw layer number,
    so it stays well-defined regardless of whether layer numbering starts at 0 or 1 or has gaps.
    This is the mode the KUKA ArcTech Multilayer option pack can actually render: one direction
    per CASE/layer, no zigzag within a layer.
    An override never shifts the parity of later passes because parity depends only on
    execution_ordinal/layer_position, not on prior overrides.
    """
    if direction_mode == DirectionMode.ZIGZAG:
        computed = Direction.FORWARD if execution_ordinal % 2 == 0 else Direction.REVERSE
    elif direction_mode == DirectionMode.ALTERNATING:
        computed = Direction.FORWARD if layer_position % 2 == 0 else Direction.REVERSE
    else:
        computed = Direction.FORWARD

    if override == DirectionOverride.FORWARD:
        return Direction.FORWARD
    if override == DirectionOverride.REVERSE:
        return Direction.REVERSE
    return computed


def build_multilayer_plan(
    pass_inputs: Sequence[PassInput],
    output_mode: str,
    sequence_mode: SequenceMode,
    direction_mode: DirectionMode,
    schema_version: int = MultiLayerMetadata.SCHEMA_VERSION,
) -> MultilayerPlan:
    """Build the full neutral plan: seam grouping, ordering, flattening, direction.

    LAYER_BEAD_ACROSS_SEAMS is implemented and unit-tested here but stays
    feature-gated for production use until Balancing/Sequencing integration
    lands (section 10.4); callers must not expose it in the UI until then.
    """
    diagnostics = []

    grouped = group_by_seam(pass_inputs)
    seam_ordinal_by_uuid = {uuid: ordinal for ordinal, (uuid, _) in enumerate(grouped)}

    sorted_groups = []
    flat_index_in_seam = {}
    for seam_uuid, entries in grouped:
        duplicates = find_duplicate_layer_bead(entries)
        if duplicates:
            diagnostics.append(diag.make_diagnostic(
                "ML005", seam_uuid=seam_uuid,
                message="Duplicate layer/bead coordinate(s) %s in seam %s" % (duplicates, seam_uuid),
            ))
        ordered_entries = sort_seam_passes(entries)
        sorted_groups.append((seam_uuid, ordered_entries))
        for seam_index, item in enumerate(ordered_entries):
            key = (item.seam_uuid, item.layer, item.bead, item.source_operation_ordinal)
            flat_index_in_seam[key] = seam_index

    if sequence_mode == SequenceMode.LAYER_BEAD_ACROSS_SEAMS:
        execution_order = layer_bead_across_seams_order(sorted_groups)
    else:
        execution_order = complete_seam_order(sorted_groups)

    # Layer's 0-based rank among the seam's own distinct layer numbers (section 10.5's
    # Alternating), computed per seam so it stays well-defined regardless of numbering
    # convention or gaps.
    layer_position_by_seam = {}
    for seam_uuid, entries in sorted_groups:
        distinct_layers = sorted({item.layer for item in entries})
        layer_position_by_seam[seam_uuid] = {layer_num: idx for idx, layer_num in enumerate(distinct_layers)}

    execution_passes = []
    for program_index, item in enumerate(execution_order):
        layer_position = layer_position_by_seam[item.seam_uuid][item.layer]
        direction = resolve_direction(program_index, layer_position, direction_mode, item.direction_override)
        key = (item.seam_uuid, item.layer, item.bead, item.source_operation_ordinal)
        execution_passes.append(MultilayerPass(
            seam_uuid=item.seam_uuid,
            seam_ordinal=seam_ordinal_by_uuid[item.seam_uuid],
            wps_main_id=item.wps_main_id,
            wps_sub_id=item.wps_sub_id,
            wps_name=item.wps_name,
            layer=item.layer,
            bead=item.bead,
            source_operation=item.source_operation,
            source_operation_ordinal=item.source_operation_ordinal,
            flat_index_in_seam=flat_index_in_seam[key],
            flat_index_in_program=program_index,
            direction=direction,
            recipe_fingerprint=item.recipe_fingerprint,
        ))

    passes_by_seam = {}
    for p in execution_passes:
        passes_by_seam.setdefault(p.seam_uuid, []).append(p)

    seams = []
    for seam_uuid, entries in sorted_groups:
        seam_passes = tuple(sorted(passes_by_seam.get(seam_uuid, []), key=lambda p: p.flat_index_in_seam))
        seams.append(MultilayerSeam(
            seam_uuid=seam_uuid,
            seam_ordinal=seam_ordinal_by_uuid[seam_uuid],
            passes=seam_passes,
            sensing=SeamSensingPlan(),
        ))

    return MultilayerPlan(
        schema_version=schema_version,
        output_mode=output_mode,
        sequence_mode=sequence_mode.value,
        direction_mode=direction_mode.value,
        seams=tuple(seams),
        execution=tuple(execution_passes),
        diagnostics=tuple(diagnostics),
    )

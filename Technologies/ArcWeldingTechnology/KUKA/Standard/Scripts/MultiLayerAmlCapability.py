# -------------------------------------------------------------------------------------------
# Name: MultiLayerAmlCapability
# Description: Decides which seams may be projected to KUKA ArcTech MultiLayer and which must
#              fall back to native output. Pure: no E2 API, no KRL emission. Consumed by the
#              downloader before any AML rendering happens.
#              See the focused unit tests for supported seam shapes and fallback behavior.
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
from typing import Optional, Sequence

import MultiLayerMetadata
import MultiLayerDiagnostics as diag
from MultiLayerPlanner import Direction


CONTROLLER_FAMILY = "KRC5"
SUPPORTED_KSS = ((8, 6), (8, 7))
COMPATIBLE_AML_MAJOR_MINOR = (3, 7)

# Section 13.2: one root plus at most 99 filler/cover cases.
MAX_FILLER_CASES = 99

# Reconciliation F15 is resolved: the reverse-layer shape is specified. This stays False until the
# emitter implements the reversed walk and a reverse golden exists.
REVERSE_DIRECTION_SUPPORTED = False


@dataclass(frozen=True)
class AmlConfiguration:
    """User assertion about the physical controller. FASTSUITE does not probe it (section 13.1)."""
    controller_family: str
    kss_version: str
    aml_installed: bool
    aml_version: str


@dataclass(frozen=True)
class AmlCapabilityResult:
    program_allows_aml: bool
    aml_seam_uuids: frozenset
    native_seam_uuids: frozenset
    diagnostics: tuple


def parse_version(text) -> Optional[tuple]:
    """Parse a dotted numeric version into a tuple, or None if it is not one.

    Returns None rather than raising: an unparseable version is a configuration
    problem the caller reports as ML008, not a programming defect.
    """
    if not isinstance(text, str):
        return None
    parts = text.strip().split(".")
    if not parts or any(not p.isdigit() for p in parts):
        return None
    return tuple(int(p) for p in parts)


def check_program_configuration(config: AmlConfiguration, program: Optional[str] = None):
    """Evaluate the section 13.1 program-wide gate.

    Returns (allowed, [Diagnostic, ...]). All failing conditions are reported, not just the
    first, so one download surfaces every configuration problem at once.
    """
    diagnostics = []

    if not config.aml_installed:
        diagnostics.append(diag.make_diagnostic(
            "ML007",
            "AML option pack is not configured for this program",
            program=program,
            selected_mode=MultiLayerMetadata.OUTPUT_MODE_KUKA_AML,
            fallback_mode=MultiLayerMetadata.OUTPUT_MODE_E2_NATIVE,
        ))

    family = (config.controller_family or "").strip().upper()
    if family != CONTROLLER_FAMILY:
        diagnostics.append(diag.make_diagnostic(
            "ML008",
            "Controller family %r is not %s" % (config.controller_family, CONTROLLER_FAMILY),
            program=program,
            selected_mode=MultiLayerMetadata.OUTPUT_MODE_KUKA_AML,
            fallback_mode=MultiLayerMetadata.OUTPUT_MODE_E2_NATIVE,
        ))

    kss = parse_version(config.kss_version)
    if kss is None or kss[:2] not in SUPPORTED_KSS:
        diagnostics.append(diag.make_diagnostic(
            "ML008",
            "KSS version %r is not one of %s" % (
                config.kss_version, ", ".join("%d.%d" % v for v in SUPPORTED_KSS)),
            program=program,
            selected_mode=MultiLayerMetadata.OUTPUT_MODE_KUKA_AML,
            fallback_mode=MultiLayerMetadata.OUTPUT_MODE_E2_NATIVE,
        ))

    aml = parse_version(config.aml_version)
    if aml is None or aml[:2] != COMPATIBLE_AML_MAJOR_MINOR:
        diagnostics.append(diag.make_diagnostic(
            "ML008",
            "ArcTech MultiLayer version %r is not compatible with %d.%d behavior" % (
                (config.aml_version,) + COMPATIBLE_AML_MAJOR_MINOR),
            program=program,
            selected_mode=MultiLayerMetadata.OUTPUT_MODE_KUKA_AML,
            fallback_mode=MultiLayerMetadata.OUTPUT_MODE_E2_NATIVE,
        ))

    return (not diagnostics), diagnostics


def check_seam(seam, geometry_for=None, program: Optional[str] = None):
    """Evaluate the section 13.6 structural restrictions for one seam.

    geometry_for maps a MultilayerPass to its PassGeometryData, or None when the row could not
    be resolved. Fallback is per seam: a rejected seam never disables a valid one.
    """
    diagnostics = []

    def warn(code, message, mlpass=None):
        diagnostics.append(diag.make_diagnostic(
            code, message,
            program=program,
            seam_uuid=seam.seam_uuid,
            wps_main_id=mlpass.wps_main_id if mlpass else None,
            wps_sub_id=mlpass.wps_sub_id if mlpass else None,
            layer=mlpass.layer if mlpass else None,
            bead=mlpass.bead if mlpass else None,
            selected_mode=MultiLayerMetadata.OUTPUT_MODE_KUKA_AML,
            fallback_mode=MultiLayerMetadata.OUTPUT_MODE_E2_NATIVE,
        ))

    if not seam.seam_uuid:
        warn("ML006", "Seam has no stable UUID")

    filler_count = max(len(seam.passes) - 1, 0)
    if filler_count > MAX_FILLER_CASES:
        warn("ML009", "Seam has %d filler passes; AML supports at most %d" % (
            filler_count, MAX_FILLER_CASES))

    for mlpass in seam.passes:
        if not REVERSE_DIRECTION_SUPPORTED and mlpass.direction == Direction.REVERSE:
            warn("ML017", "Reverse layer direction is specified but not yet emitted; "
                          "see reconciliation F15", mlpass)
        if geometry_for is None:
            continue
        geometry = geometry_for(mlpass)
        if geometry is None:
            warn("ML003", "No process-table geometry resolved for this pass", mlpass)
        elif geometry.contour_start_offset:
            warn("ML012", "Contour start offset %r requires a path-tangent X translation, "
                          "which AML cannot express" % (geometry.contour_start_offset,), mlpass)

    return (not diagnostics), diagnostics


def select_aml_seams(plan, config: AmlConfiguration, geometry_for=None,
                     program: Optional[str] = None) -> AmlCapabilityResult:
    """Partition a MultilayerPlan's seams into AML and native-fallback sets.

    A program that did not select AML is not a fallback and raises nothing.
    """
    all_uuids = frozenset(s.seam_uuid for s in plan.seams)

    if plan.output_mode != MultiLayerMetadata.OUTPUT_MODE_KUKA_AML:
        return AmlCapabilityResult(False, frozenset(), all_uuids, ())

    programOk, diagnostics = check_program_configuration(config, program=program)
    if not programOk:
        return AmlCapabilityResult(False, frozenset(), all_uuids, tuple(diagnostics))

    amlUuids = set()
    for seam in plan.seams:
        seamOk, seamDiagnostics = check_seam(seam, geometry_for=geometry_for, program=program)
        diagnostics.extend(seamDiagnostics)
        if seamOk:
            amlUuids.add(seam.seam_uuid)

    if amlUuids:
        # Section 13.7 requires this on every download that emits AML, not only on failures.
        diagnostics.append(diag.make_diagnostic(
            "ML016",
            "AML filler geometry is generated by the KUKA controller from the root path and may "
            "differ from the FASTSUITE E2 simulation. Perform a reduced-speed dry run in T1 "
            "Continuous before production use.",
            program=program,
            selected_mode=MultiLayerMetadata.OUTPUT_MODE_KUKA_AML,
        ))

    return AmlCapabilityResult(
        program_allows_aml=True,
        aml_seam_uuids=frozenset(amlUuids),
        native_seam_uuids=all_uuids - frozenset(amlUuids),
        diagnostics=tuple(diagnostics),
    )

# -------------------------------------------------------------------------------------------
# Name: MultiLayerRecipeState
# Description: Controller-neutral Multilayer recipe snapshot fingerprint and application state.
#              Recipe data is an applied snapshot; source changes must be visible but never
#              silently applied. See docs/ctrl-specific/KUKA/spec/multilayer.md section 9.
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

from enum import Enum
from typing import Sequence

import MultiLayerMetadata
import MultiLayerProcessTable as process_table


class RecipeState(Enum):
    NOT_APPLICABLE = MultiLayerMetadata.RECIPE_STATE_NOT_APPLICABLE
    CURRENT_SNAPSHOT = MultiLayerMetadata.RECIPE_STATE_CURRENT_SNAPSHOT
    UPDATE_AVAILABLE = MultiLayerMetadata.RECIPE_STATE_UPDATE_AVAILABLE
    DETACHED = MultiLayerMetadata.RECIPE_STATE_DETACHED
    MISSING_SOURCE = MultiLayerMetadata.RECIPE_STATE_MISSING_SOURCE


def compute_recipe_fingerprint(
    passes: Sequence[process_table.WpsPassRecord],
    schema_version: int = MultiLayerMetadata.SCHEMA_VERSION,
) -> str:
    """Deterministic fingerprint over an ordered, applied set of WPS pass records.

    Normalizes by (layer, bead, sub_id), excludes transient/runtime-only
    fields, and reuses the shared hashing helper so row-level and recipe-level
    fingerprints stay consistent (section 9.1).
    """
    ordered = sorted(passes, key=lambda p: (p.layer, p.bead, p.sub_id))
    payload = {"schema_version": schema_version, "main_id": ordered[0].main_id if ordered else -1}
    for position, record in enumerate(ordered):
        prefix = "pass_%d_" % position
        payload[prefix + "sub_id"] = record.sub_id
        payload[prefix + "layer"] = record.layer
        payload[prefix + "bead"] = record.bead
        payload[prefix + "bead"] = record.bead
        for key, value in record.geometry.__dict__.items():
            payload[prefix + "geometry_" + key] = value
        for key, value in record.process.__dict__.items():
            payload[prefix + "process_" + key] = value
    return process_table.build_fingerprint(payload)


def resolve_recipe_state(
    is_multilayer_process_table: bool,
    source_exists: bool,
    applied_fingerprint: str,
    current_fingerprint: str,
    locally_modified: bool,
) -> RecipeState:
    """Resolve the recipe state transitions defined in section 9.2."""
    if not is_multilayer_process_table:
        return RecipeState.NOT_APPLICABLE
    if not source_exists:
        return RecipeState.MISSING_SOURCE
    if locally_modified:
        return RecipeState.DETACHED
    if applied_fingerprint != current_fingerprint:
        return RecipeState.UPDATE_AVAILABLE
    return RecipeState.CURRENT_SNAPSHOT

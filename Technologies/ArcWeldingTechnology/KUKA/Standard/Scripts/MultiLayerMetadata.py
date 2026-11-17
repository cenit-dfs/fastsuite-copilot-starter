# -------------------------------------------------------------------------------------------
# Name: MultiLayerMetadata
# Description: Controller-neutral Multilayer attribute names, literals, and schema version.
#              No KUKA-specific behavior belongs here. See MultiLayerProcessTable,
#              MultiLayerPlanner, and MultiLayerRecipeState for the rest of the shared model.
#              See docs/ctrl-specific/KUKA/spec/multilayer.md section 8.
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

SCHEMA_VERSION = 1

# Core ArcWeldingTechnology attributes read (never created) by the resolver. Both are scoped
# User|Global with no Process flag, so they are readable during workmethod sync but NOT from
# the download APIs - hence the section-8.3 operation attributes exist to carry identity.
ATTR_WPS_AUTOMATIC = "WPSAutomatic"
ATTR_WPS_AUTOMATIC_NAMES = "WPSAutomaticNames"

# Process-geometry attributes E2 uses to auto-match a WPS when WPSAutomatic is true. They arrive
# with geometry imported from third-party CAD; all four must match a dataset for the recipe to be
# applied automatically.
PG_CAD_MATCH_INTEGER_ATTRIBUTES = ("WeldIdAttribute", "WeldingPositionAttribute")
PG_CAD_MATCH_STRING_ATTRIBUTES = ("MaterialAttribute",)
PG_CAD_MATCH_DOUBLE_ATTRIBUTES = ("SeamSizeAttribute",)

# Section 8.2 - user-facing program/operation attributes.
ATTR_OUTPUT_MODE = "MultiLayerOutputMode"
ATTR_SEQUENCE_MODE = "MultiLayerSequenceMode"
ATTR_DIRECTION_MODE = "MultiLayerDirectionMode"
ATTR_DIRECTION_OVERRIDE = "MultiLayerDirectionOverride"
ATTR_KUKA_AML_INSTALLED = "KukaArcTechMultilayerInstalled"
ATTR_KUKA_AML_VERSION = "KukaArcTechMultilayerVersion"

# Section 8.3 - stable read-only operation metadata.
ATTR_METADATA_VERSION = "MultiLayerMetadataVersion"
ATTR_USES_PROCESS_TABLE = "MultiLayerUsesProcessTable"
ATTR_WPS_MAIN_ID = "MultiLayerWpsMainId"
ATTR_WPS_SUB_ID = "MultiLayerWpsSubId"
ATTR_WPS_NAME = "MultiLayerWpsName"
ATTR_LAYER_NUMBER = "MultiLayerLayerNumber"
ATTR_BEAD_NUMBER = "MultiLayerBeadNumber"
ATTR_FLAT_PASS_INDEX = "MultiLayerFlatPassIndex"
ATTR_SEAM_UUID = "MultiLayerSeamUuid"
ATTR_RECIPE_FINGERPRINT = "MultiLayerRecipeFingerprint"
ATTR_RECIPE_STATE = "MultiLayerRecipeState"
ATTR_WORK_ANGLE_OFFSET = "MultiLayerWorkAngleOffset"
ATTR_ABSOLUTE_TRAVEL_ANGLE = "MultiLayerAbsoluteTravelAngle"
ATTR_NORMAL_OFFSET = "MultiLayerNormalOffset"
ATTR_CONTOUR_START_OFFSET = "MultiLayerContourStartOffset"
ATTR_CONTOUR_OFFSET = "MultiLayerContourOffset"

OUTPUT_MODE_E2_NATIVE = "E2NativePaths"
OUTPUT_MODE_KUKA_AML = "KukaArcTechMultilayer"
OUTPUT_MODE_LITERALS = [OUTPUT_MODE_E2_NATIVE, OUTPUT_MODE_KUKA_AML]
OUTPUT_MODE_DEFAULT = OUTPUT_MODE_E2_NATIVE

SEQUENCE_MODE_COMPLETE_SEAM = "CompleteSeam"
SEQUENCE_MODE_LAYER_BEAD_ACROSS_SEAMS = "LayerBeadAcrossSeams"
SEQUENCE_MODE_LITERALS = [SEQUENCE_MODE_COMPLETE_SEAM, SEQUENCE_MODE_LAYER_BEAD_ACROSS_SEAMS]
SEQUENCE_MODE_DEFAULT = SEQUENCE_MODE_COMPLETE_SEAM

DIRECTION_MODE_SAME = "SameDirection"
DIRECTION_MODE_ALTERNATING = "Alternating"
DIRECTION_MODE_ZIGZAG = "ZigZag"
# Alternating flips once per distinct layer number within a seam (matches the KUKA ArcTech
# Multilayer option pack: one direction per CASE/layer, no zigzag within a layer). ZigZag
# flips every single pass, continuously across the whole program - not achievable on
# controllers whose option pack only exposes a per-layer direction (e.g. KUKA AML).
DIRECTION_MODE_LITERALS = [DIRECTION_MODE_SAME, DIRECTION_MODE_ALTERNATING, DIRECTION_MODE_ZIGZAG]
DIRECTION_MODE_DEFAULT = DIRECTION_MODE_SAME

DIRECTION_OVERRIDE_INHERIT = "InheritProgram"
DIRECTION_OVERRIDE_FORWARD = "Forward"
DIRECTION_OVERRIDE_REVERSE = "Reverse"
DIRECTION_OVERRIDE_LITERALS = [DIRECTION_OVERRIDE_INHERIT, DIRECTION_OVERRIDE_FORWARD, DIRECTION_OVERRIDE_REVERSE]
DIRECTION_OVERRIDE_DEFAULT = DIRECTION_OVERRIDE_INHERIT

RECIPE_STATE_NOT_APPLICABLE = "NotApplicable"
RECIPE_STATE_CURRENT_SNAPSHOT = "CurrentSnapshot"
RECIPE_STATE_UPDATE_AVAILABLE = "UpdateAvailable"
RECIPE_STATE_DETACHED = "Detached"
RECIPE_STATE_MISSING_SOURCE = "MissingSource"
RECIPE_STATE_LITERALS = [
    RECIPE_STATE_NOT_APPLICABLE,
    RECIPE_STATE_CURRENT_SNAPSHOT,
    RECIPE_STATE_UPDATE_AVAILABLE,
    RECIPE_STATE_DETACHED,
    RECIPE_STATE_MISSING_SOURCE,
]

KUKA_AML_INSTALLED_DEFAULT = False
KUKA_AML_VERSION_DEFAULT = "3.7.1.4"

# Defaults applied when stable metadata is first created on an operation (section 8.3).
METADATA_DEFAULTS = {
    ATTR_METADATA_VERSION: SCHEMA_VERSION,
    ATTR_USES_PROCESS_TABLE: False,
    ATTR_WPS_MAIN_ID: -1,
    ATTR_WPS_SUB_ID: -1,
    ATTR_WPS_NAME: "",
    ATTR_LAYER_NUMBER: -1,
    ATTR_BEAD_NUMBER: -1,
    ATTR_FLAT_PASS_INDEX: -1,
    ATTR_SEAM_UUID: "",
    ATTR_RECIPE_FINGERPRINT: "",
    ATTR_RECIPE_STATE: RECIPE_STATE_NOT_APPLICABLE,
    ATTR_WORK_ANGLE_OFFSET: 0.0,
    ATTR_ABSOLUTE_TRAVEL_ANGLE: 0.0,
    ATTR_NORMAL_OFFSET: 0.0,
    ATTR_CONTOUR_START_OFFSET: 0.0,
    ATTR_CONTOUR_OFFSET: 0.0,
}

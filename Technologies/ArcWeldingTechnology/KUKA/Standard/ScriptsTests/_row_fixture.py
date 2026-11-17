"""Shared row-building helper for Multilayer pure unit tests.

Not a test module itself; imported by test_*.py files under ScriptsTests.
"""
import sys
import os

_SCRIPTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Scripts")
if _SCRIPTS_DIR not in sys.path:
    sys.path.append(_SCRIPTS_DIR)

import MultiLayerProcessTable as process_table  # noqa: E402


def make_row(overrides=None):
    """Build a valid 38-field GetWeldingDataSetsFromDataBase() row as a list.

    Defaults describe a single Multilayer pass (layer=1, bead=1). Override by
    Row constant value, e.g. make_row({process_table.Row.LAYER_NUMBER: 2}).
    Row indices are ints, so overrides must be a plain dict, not **kwargs.
    """
    row = [None] * process_table.Row.COUNT
    row[process_table.Row.MAIN_ID] = 100
    row[process_table.Row.SUB_ID] = 1
    row[process_table.Row.NAME] = "WPS_A"
    row[process_table.Row.MATERIAL] = "S355"
    row[process_table.Row.PLATE_THICKNESS] = 6.0
    row[process_table.Row.SEAM_SIZE] = 5.0
    row[process_table.Row.SEAM_TYPE] = "Fillet"
    row[process_table.Row.OPENING_ANGLE] = 60.0
    row[process_table.Row.GROOVE_DISTANCE] = 0.0
    row[process_table.Row.WELDING_POSITION] = "PA"
    row[process_table.Row.WELDING_SPEED] = 0.008
    row[process_table.Row.WIRE_DIAMETER] = 0.0012
    row[process_table.Row.WEAVE_ENABLED] = False
    row[process_table.Row.WEAVE_FREQUENCY] = 0.0
    row[process_table.Row.WEAVE_WIDTH] = 0.0
    row[process_table.Row.WEAVE_TIME_1] = 0.0
    row[process_table.Row.WEAVE_TIME_2] = 0.0
    row[process_table.Row.OVERRUN] = 0.002
    row[process_table.Row.WIRE_FEED] = 8.0
    row[process_table.Row.WIRE_CONSUMPTION] = 0.0
    row[process_table.Row.VOLTAGE] = 24.0
    row[process_table.Row.CURRENT] = 220.0
    row[process_table.Row.GAS_FLOW_RATE] = 15.0
    row[process_table.Row.GAS_CONSUMPTION] = 0.0
    row[process_table.Row.WELDING_TIME] = 0.0
    row[process_table.Row.LAYER_NUMBER] = 1
    row[process_table.Row.BEAD_NUMBER] = 1
    row[process_table.Row.ARC_ON_PROGRAM] = "ARCON1"
    row[process_table.Row.ARC_OFF_PROGRAM] = "ARCOFF1"
    row[process_table.Row.WORK_ANGLE_OFFSET] = 0.0
    row[process_table.Row.ABSOLUTE_TRAVEL_ANGLE] = 0.0
    row[process_table.Row.NORMAL_OFFSET] = 0.0
    row[process_table.Row.CONTOUR_START_OFFSET] = 0.0
    row[process_table.Row.CONTOUR_OFFSET] = 0.0
    row[process_table.Row.WEAVE_PROGRAM] = ""
    row[process_table.Row.IS_USED] = False
    row[process_table.Row.UNVERIFIED_FLAG] = False
    row[process_table.Row.DATA_VALID] = True

    for index, value in (overrides or {}).items():
        row[index] = value
    return row

# -------------------------------------------------------------------------------------------
# Name: MultiLayerProcessTable
# Description: Controller-neutral parsing of GetWeldingDataSetsFromDataBase() rows into typed,
#              validated records. Row indices are defined once here; raw numeric indexing
#              elsewhere is forbidden. See docs/ctrl-specific/KUKA/spec/multilayer.md section 7.
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

import hashlib
from dataclasses import dataclass
from typing import Sequence

# Decimal places used to normalize floats before hashing (spec section 9.1.3).
FLOAT_FINGERPRINT_PRECISION = 6


class ProcessTableRowError(ValueError):
    """A process-table row is too short or has an invalid type for a required field."""


class Row:
    """Zero-based column indices for GetWeldingDataSetsFromDataBase() rows (spec section 7.2)."""
    MAIN_ID = 0
    SUB_ID = 1
    NAME = 2
    MATERIAL = 3
    PLATE_THICKNESS = 4
    SEAM_SIZE = 5
    SEAM_TYPE = 6
    OPENING_ANGLE = 7
    GROOVE_DISTANCE = 8
    WELDING_POSITION = 9
    WELDING_SPEED = 10
    WIRE_DIAMETER = 11
    WEAVE_ENABLED = 12
    WEAVE_FREQUENCY = 13
    WEAVE_WIDTH = 14
    WEAVE_TIME_1 = 15
    WEAVE_TIME_2 = 16
    OVERRUN = 17
    WIRE_FEED = 18
    WIRE_CONSUMPTION = 19
    VOLTAGE = 20
    CURRENT = 21
    GAS_FLOW_RATE = 22
    GAS_CONSUMPTION = 23
    WELDING_TIME = 24
    LAYER_NUMBER = 25
    BEAD_NUMBER = 26
    ARC_ON_PROGRAM = 27
    ARC_OFF_PROGRAM = 28
    WORK_ANGLE_OFFSET = 29
    ABSOLUTE_TRAVEL_ANGLE = 30
    NORMAL_OFFSET = 31
    CONTOUR_START_OFFSET = 32
    CONTOUR_OFFSET = 33
    WEAVE_PROGRAM = 34
    IS_USED = 35
    # Spec section 7.2 calls index 36 the Multilayer flag, but ArcTech 3.7.2.112 returns False
    # here on every row, including both multilayer WPSs (ML1, ML2) in the reference table.
    # Multilayer status is derived from pass count instead - see is_multilayer_wps().
    UNVERIFIED_FLAG = 36
    DATA_VALID = 37
    COUNT = 38


@dataclass(frozen=True)
class EffectiveWeldData:
    """Process-table welding values consumed by the existing ArcWelding events.

    Must not redefine those events or become a second source of truth (section 6).
    """
    material: str
    plate_thickness: float
    seam_size: float
    seam_type: str
    opening_angle: float
    groove_distance: float
    welding_position: str
    welding_speed: float
    wire_diameter: float
    weave_enabled: bool
    weave_frequency: float
    weave_width: float
    weave_time_1: float
    weave_time_2: float
    overrun: float
    wire_feed: float
    wire_consumption: float
    voltage: float
    current: float
    gas_flow_rate: float
    gas_consumption: float
    welding_time: float
    arc_on_program: str
    arc_off_program: str
    weave_program: str


@dataclass(frozen=True)
class PassGeometryData:
    """Neutral contour/normal offsets and work/travel angles, not KUKA A/B/C values."""
    work_angle_offset: float
    absolute_travel_angle: float
    normal_offset: float
    contour_start_offset: float
    contour_offset: float


@dataclass(frozen=True)
class WpsPassRecord:
    main_id: int
    sub_id: int
    name: str
    layer: int
    bead: int
    process: EffectiveWeldData
    geometry: PassGeometryData
    raw_row_fingerprint: str


def _as_int(value, field_name):
    try:
        return int(value)
    except (TypeError, ValueError):
        raise ProcessTableRowError("Field '%s' is not a valid integer: %r" % (field_name, value))


def _as_float(value, field_name):
    try:
        return float(value)
    except (TypeError, ValueError):
        raise ProcessTableRowError("Field '%s' is not a valid float: %r" % (field_name, value))


def _as_bool(value, field_name):
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    raise ProcessTableRowError("Field '%s' is not a valid boolean: %r" % (field_name, value))


def _as_str(value, field_name):
    if value is None:
        raise ProcessTableRowError("Field '%s' must not be None" % field_name)
    return str(value)


def build_fingerprint(payload: dict) -> str:
    """Deterministic SHA-256 hex fingerprint over named fields, sorted by key.

    Floats are rounded to FLOAT_FINGERPRINT_PRECISION so equal process meaning
    yields an equal fingerprint across processes/machines (spec section 9.1).
    """
    normalized = {}
    for key in sorted(payload.keys()):
        value = payload[key]
        if isinstance(value, float):
            value = round(value, FLOAT_FINGERPRINT_PRECISION)
        normalized[key] = value
    serialized = repr(sorted(normalized.items()))
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def parse_row(row: Sequence) -> WpsPassRecord:
    """Parse and validate one GetWeldingDataSetsFromDataBase() row.

    Excludes the transient _isUsed flag (row 35) from the row fingerprint so
    core's creation-time cursor never affects change detection (section 9.1.4).
    """
    if row is None or len(row) < Row.COUNT:
        raise ProcessTableRowError(
            "Row has %d fields, expected at least %d" % (0 if row is None else len(row), Row.COUNT)
        )

    process = EffectiveWeldData(
        material=_as_str(row[Row.MATERIAL], "Material"),
        plate_thickness=_as_float(row[Row.PLATE_THICKNESS], "PlateThickness"),
        seam_size=_as_float(row[Row.SEAM_SIZE], "SeamSize"),
        seam_type=_as_str(row[Row.SEAM_TYPE], "SeamType"),
        opening_angle=_as_float(row[Row.OPENING_ANGLE], "OpeningAngle"),
        groove_distance=_as_float(row[Row.GROOVE_DISTANCE], "GrooveDistance"),
        welding_position=_as_str(row[Row.WELDING_POSITION], "WeldingPosition"),
        welding_speed=_as_float(row[Row.WELDING_SPEED], "WeldingSpeed"),
        wire_diameter=_as_float(row[Row.WIRE_DIAMETER], "WireDiameter"),
        weave_enabled=_as_bool(row[Row.WEAVE_ENABLED], "WeaveEnabled"),
        weave_frequency=_as_float(row[Row.WEAVE_FREQUENCY], "WeaveFrequency"),
        weave_width=_as_float(row[Row.WEAVE_WIDTH], "WeaveWidth"),
        weave_time_1=_as_float(row[Row.WEAVE_TIME_1], "WeaveTime1"),
        weave_time_2=_as_float(row[Row.WEAVE_TIME_2], "WeaveTime2"),
        overrun=_as_float(row[Row.OVERRUN], "Overrun"),
        wire_feed=_as_float(row[Row.WIRE_FEED], "WireFeed"),
        wire_consumption=_as_float(row[Row.WIRE_CONSUMPTION], "WireConsumption"),
        voltage=_as_float(row[Row.VOLTAGE], "Voltage"),
        current=_as_float(row[Row.CURRENT], "Current"),
        gas_flow_rate=_as_float(row[Row.GAS_FLOW_RATE], "GasFlowRate"),
        gas_consumption=_as_float(row[Row.GAS_CONSUMPTION], "GasConsumption"),
        welding_time=_as_float(row[Row.WELDING_TIME], "WeldingTime"),
        arc_on_program=_as_str(row[Row.ARC_ON_PROGRAM], "ArcOnProgram"),
        arc_off_program=_as_str(row[Row.ARC_OFF_PROGRAM], "ArcOffProgram"),
        weave_program=_as_str(row[Row.WEAVE_PROGRAM], "WeaveProgram"),
    )
    geometry = PassGeometryData(
        work_angle_offset=_as_float(row[Row.WORK_ANGLE_OFFSET], "WorkAngleOffset"),
        absolute_travel_angle=_as_float(row[Row.ABSOLUTE_TRAVEL_ANGLE], "AbsoluteTravelAngle"),
        normal_offset=_as_float(row[Row.NORMAL_OFFSET], "NormalOffset"),
        contour_start_offset=_as_float(row[Row.CONTOUR_START_OFFSET], "ContourStartOffset"),
        contour_offset=_as_float(row[Row.CONTOUR_OFFSET], "ContourOffset"),
    )

    fingerprint_payload = {
        "main_id": _as_int(row[Row.MAIN_ID], "MainId"),
        "sub_id": _as_int(row[Row.SUB_ID], "SubId"),
        "name": _as_str(row[Row.NAME], "Name"),
        "layer": _as_int(row[Row.LAYER_NUMBER], "LayerNumber"),
        "bead": _as_int(row[Row.BEAD_NUMBER], "BeadNumber"),
    }
    for key, value in process.__dict__.items():
        fingerprint_payload["process_" + key] = value
    for key, value in geometry.__dict__.items():
        fingerprint_payload["geometry_" + key] = value

    return WpsPassRecord(
        main_id=fingerprint_payload["main_id"],
        sub_id=fingerprint_payload["sub_id"],
        name=fingerprint_payload["name"],
        layer=fingerprint_payload["layer"],
        bead=fingerprint_payload["bead"],
        process=process,
        geometry=geometry,
        raw_row_fingerprint=build_fingerprint(fingerprint_payload),
    )


def is_data_valid(row: Sequence) -> bool:
    return _as_bool(row[Row.DATA_VALID], "DataValid")


def is_used(row: Sequence) -> bool:
    return _as_bool(row[Row.IS_USED], "IsUsed")


def find_rows_by_name(rows: Sequence[Sequence], wps_name: str):
    """Name-matching, data-valid rows regardless of pass count.

    Returns a list of (original_index, row) pairs, preserving row order.
    """
    matches = []
    for index, row in enumerate(rows):
        if len(row) < Row.COUNT:
            continue
        if str(row[Row.NAME]) != wps_name:
            continue
        if not is_data_valid(row):
            continue
        matches.append((index, row))
    return matches


def is_multilayer_wps(rows: Sequence[Sequence], wps_name: str) -> bool:
    """True when the named WPS describes more than one pass.

    The process table exposes no usable per-row Multilayer flag (see Row.UNVERIFIED_FLAG),
    so pass count is the signal: single-layer WPSs own exactly one data-valid row.
    """
    return len(find_rows_by_name(rows, wps_name)) > 1


def find_candidate_rows(rows: Sequence[Sequence], wps_name: str):
    """Rows eligible for Multilayer resolution (spec section 7.4 step 4).

    Empty for a single-layer WPS, which the resolver reports as ML002.
    """
    matches = find_rows_by_name(rows, wps_name)
    return matches if len(matches) > 1 else []


def select_first_unused(rows: Sequence[Sequence], wps_name: str):
    """Mirror the core's first-unused row selection for a given WPS name.

    Returns (row_index, WpsPassRecord) or None. Only valid while an operation
    is being created; never call this at download time (section 7.3).
    """
    for index, row in find_candidate_rows(rows, wps_name):
        if not is_used(row):
            return index, parse_row(row)
    return None


def find_ambiguous_main_ids(rows: Sequence[Sequence], wps_name: str):
    """Distinct main IDs sharing wps_name among valid Multilayer rows (diagnostic ML004)."""
    main_ids = set()
    for _, row in find_candidate_rows(rows, wps_name):
        main_ids.add(_as_int(row[Row.MAIN_ID], "MainId"))
    return main_ids


def find_by_stable_id(rows: Sequence[Sequence], main_id: int, sub_id: int, layer: int, bead: int):
    """Resolve a row at download time by stable IDs, never by _isUsed (section 7.3/7.4)."""
    for row in rows:
        if len(row) < Row.COUNT:
            continue
        if not is_data_valid(row):
            continue
        if (_as_int(row[Row.MAIN_ID], "MainId") == main_id
                and _as_int(row[Row.SUB_ID], "SubId") == sub_id
                and _as_int(row[Row.LAYER_NUMBER], "LayerNumber") == layer
                and _as_int(row[Row.BEAD_NUMBER], "BeadNumber") == bead):
            return parse_row(row)
    return None

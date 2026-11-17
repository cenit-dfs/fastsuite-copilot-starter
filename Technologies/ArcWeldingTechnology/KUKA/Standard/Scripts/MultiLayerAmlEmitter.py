# -------------------------------------------------------------------------------------------
# Name: MultiLayerAmlEmitter
# Description: Pure KRL text builder for one KUKA ArcTech Multilayer seam module (root layer +
#              N Direct filler layers). No E2 API, no I/O. Every construct here traces to a row
#              the synthetic golden fixtures and focused unit tests. Consumed by the downloader only after
#              MultiLayerAmlCapability.select_aml_seams has approved the seam (Direct-only,
#              REVERSE_DIRECTION_SUPPORTED stays False until reverse has its own golden).
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
import uuid

ARCON = "ARCON"
ARCSWI = "ARCSWI"
ARCOFF = "ARCOFF"
_ROLE_TOKEN = {ARCON: "ARCON", ARCSWI: "ARCSWI", ARCOFF: "ARCOFF"}
_ROLE_TOKEN_ML = {ARCON: "MLARCON", ARCSWI: "MLARCSWI", ARCOFF: "MLARCOFF"}
_ROLE_ILF = {ARCON: "arconlin", ARCSWI: "arcswilin", ARCOFF: "arcofflin"}


class SeamShapeError(ValueError):
    """The root role sequence does not start with ARCON and end with ARCOFF (reconciliation §11.2)."""


class UnsupportedLayerGeometryError(ValueError):
    """The neutral pass geometry cannot be represented by a KUKA AML layer frame."""


class InvalidWdatError(ValueError):
    """A native WDAT declaration cannot be transformed safely for an AML filler layer."""


@dataclass(frozen=True)
class MotionObservation:
    """Controller-neutral motion facts collected by the downloader before AML emission."""
    point: str
    is_linear: bool
    event_names: tuple = ()
    vel: Optional[str] = None
    via_point: Optional[str] = None


@dataclass(frozen=True)
class WeldPoint:
    """One root command: its role, taught point name, ArcTech MultiLayer weld-point variable,
    and its `ArcTech.ML.Id` (uuid5(seam_uuid, root_command_ordinal) - reconciliation D8)."""
    kind: str
    point: str
    weld_point_var: str
    ml_id: str
    vel: Optional[str] = None  # "0.5" style; ARCON defaults to "0.5", others to "0.025"
    via_point: Optional[str] = None
    via_weld_point_var: Optional[str] = None


def _seam_namespace(seam_uuid: str) -> uuid.UUID:
    """Use a real seam UUID directly; derive a stable namespace for E2's opaque seam IDs."""
    try:
        return uuid.UUID(seam_uuid)
    except (AttributeError, TypeError, ValueError):
        return uuid.uuid5(uuid.NAMESPACE_URL, "fastsuite-e2:kuka-aml:" + str(seam_uuid))


def build_root_weld_points(seam_uuid: str, motions: Sequence[MotionObservation]) -> tuple:
    """Extract ARCON/ARCSWI/ARCOFF commands from one operation's ordered motion stream.

    Motions outside the ArcOn/ArcOff envelope are caller-level approach/retract motions and are
    deliberately ignored. Unsupported or ambiguous weld shapes fail before output capture starts.
    """
    result = []
    started = False
    closed = False
    namespace = _seam_namespace(seam_uuid)

    for motion in motions:
        event_names = set(motion.event_names)
        has_arc_on = "ArcOnEvent" in event_names
        has_arc_off = "ArcOffEvent" in event_names
        if has_arc_on and has_arc_off:
            raise SeamShapeError("one motion cannot contain both ArcOnEvent and ArcOffEvent")

        kind = None
        if has_arc_on:
            if started or closed:
                raise SeamShapeError("root contains more than one ArcOnEvent")
            kind = ARCON
            started = True
        elif has_arc_off:
            if not started or closed:
                raise SeamShapeError("ArcOffEvent does not close one active root weld")
            kind = ARCOFF
            closed = True
        elif started and not closed:
            kind = ARCSWI

        if kind is None:
            continue
        if not motion.is_linear and not motion.via_point:
            raise SeamShapeError("AML root weld commands must use LIN or CIRC motions")
        if motion.via_point and kind != ARCSWI:
            raise SeamShapeError("AML CIRC is currently supported only for ARCSWI motions")
        if not (motion.point.startswith("P") and motion.point[1:].isdigit()):
            raise SeamShapeError("AML point names must use the P<number> form")
        if motion.via_point and not (
            motion.via_point.startswith("P") and motion.via_point[1:].isdigit()
        ):
            raise SeamShapeError("AML CIRC via-point names must use the P<number> form")

        ordinal = len(result) + 1
        result.append(WeldPoint(
            kind=kind,
            point=motion.point,
            weld_point_var="WP" + motion.point[1:],
            ml_id=str(uuid.uuid5(namespace, str(ordinal))),
            vel=motion.vel,
            via_point=motion.via_point,
            via_weld_point_var=("WP" + motion.via_point[1:]) if motion.via_point else None,
        ))

    if not started or not closed:
        raise SeamShapeError("root must contain one ArcOnEvent/ArcOffEvent envelope")
    return tuple(result)


@dataclass(frozen=True)
class FillerLayer:
    number: int          # 1-based, matches ArcTech.ML.LayerNumber / the CASE label
    frame_name: str       # e.g. "LayerOffset1"


@dataclass(frozen=True)
class LayerFrame:
    x: float
    y: float
    z: float
    a: float
    b: float
    c: float
    mapping_status: str = "provisional"


def build_layer_frame(geometry) -> LayerFrame:
    """Map neutral process-table geometry to KUKA TTS axes (multilayer spec section 13.5)."""
    if geometry.contour_start_offset:
        raise UnsupportedLayerGeometryError(
            "KUKA AML cannot represent a path-tangent contour-start offset"
        )
    return LayerFrame(
        x=0.0,
        y=geometry.contour_offset * 1000.0,
        z=geometry.normal_offset * 1000.0,
        a=0.0,
        b=geometry.absolute_travel_angle,
        c=geometry.work_angle_offset,
    )


def format_layer_frame_declaration(number: int, frame: LayerFrame) -> str:
    return (
        f"DECL FRAME LayerOffset{number}="
        f"{{X {frame.x:.6f},Y {frame.y:.6f},Z {frame.z:.6f},"
        f"A {frame.a:.6f},B {frame.b:.6f},C {frame.c:.6f}}}"
    )


def _split_top_level_fields(body: str) -> list:
    fields = []
    start = 0
    depth = 0
    for index, char in enumerate(body):
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth < 0:
                raise InvalidWdatError("unbalanced WDAT braces")
        elif char == "," and depth == 0:
            fields.append(body[start:index])
            start = index + 1
    if depth != 0:
        raise InvalidWdatError("unbalanced WDAT braces")
    fields.append(body[start:])
    return fields


def build_filler_wdat_declaration(native_declaration: str, layer: int) -> str:
    """Project one native pass WDAT to AML filler data (reconciliation D4/D6)."""
    prefix = "DECL stArcDat_T "
    if not native_declaration.startswith(prefix) or "={" not in native_declaration:
        raise InvalidWdatError("expected a DECL stArcDat_T WDAT... declaration")
    lhs, separator, remainder = native_declaration.partition("={")
    if not separator or not remainder.endswith("}"):
        raise InvalidWdatError("malformed native WDAT declaration")
    native_name = lhs[len(prefix):]
    if not native_name.startswith("WDAT"):
        raise InvalidWdatError("expected a WDAT variable")
    filler_name = f"L{layer}_{native_name}"
    if len(filler_name) > 24:
        raise InvalidWdatError(f"KRL identifier {filler_name!r} exceeds 24 characters")

    retained = []
    for field in _split_top_level_fields(remainder[:-1]):
        key = field.lstrip().split(None, 1)[0]
        if key not in ("WdatId[]", "Info", "Track"):
            retained.append(field)
    if not retained:
        raise InvalidWdatError("native WDAT has no reusable process data")
    return f"{prefix}{filler_name}={{" + ",".join(retained) + "}"


_WELD_POINT_MULTILAYER = (
    "MultiLayer {OP #ARC,SPos {X 0.0,Y 0.0,Z 0.0,A 0.0,B 0.0,C 0.0},"
    "SBase {C 0.0},EPos {C 0.0},CPos {C 0.0},ActPos {X 0.0,Y 0.0,Z 0.0,"
    "A 0.0,B 0.0,C 0.0,S 'B0010',T 'B00100010'}}"
)


def build_weld_point_declarations(
    root: Sequence[WeldPoint], seam_data_declaration: str, arctech_version: str
) -> list:
    """Build one AML weld-point state declaration per root command."""
    prefix = "DECL stArcDat_T "
    if not seam_data_declaration.startswith(prefix) or "={" not in seam_data_declaration:
        raise InvalidWdatError("expected a native WS seam-data declaration")
    lhs, _, remainder = seam_data_declaration.partition("={")
    seam_data_name = lhs[len(prefix):]
    if not seam_data_name.startswith("WS") or not remainder.endswith("}"):
        raise InvalidWdatError("malformed native WS seam-data declaration")

    declarations = []
    declared = set()
    for index, role in enumerate(root):
        if index == 0:
            body = remainder[:-1]
            fields = _split_top_level_fields(body)
            fields[0] = f'WdatId[] "{role.weld_point_var}"'
            fields.append(_WELD_POINT_MULTILAYER)
            declarations.append(
                f"{prefix}{role.weld_point_var}={{" + ",".join(fields) + "}"
            )
        else:
            declarations.append(
                f'{prefix}{role.weld_point_var}={{WdatId[] "{role.weld_point_var}",'
                f"Info {{Version {arctech_version}}},{_WELD_POINT_MULTILAYER}}}"
            )
        declared.add(role.weld_point_var)
        if role.via_weld_point_var and role.via_weld_point_var not in declared:
            declarations.append(
                f'{prefix}{role.via_weld_point_var}={{WdatId[] "{role.via_weld_point_var}",'
                f"Info {{Version {arctech_version}}},{_WELD_POINT_MULTILAYER}}}"
            )
            declared.add(role.via_weld_point_var)
    return declarations


def format_aml_info_declaration(filler_count: int) -> str:
    if filler_count < 0 or filler_count > 99:
        raise ValueError("AML filler count must be between 0 and 99")
    return f'DECL stAmlInfo_T AmlInfo={{Info[] " ",MaxLayer {filler_count}}}'


def _vel(role: WeldPoint) -> str:
    if role.vel is not None:
        return role.vel
    return "0.5" if role.kind == ARCON else "0.025"


def _wdat_indices(root: Sequence[WeldPoint], start_index: int):
    """Assign one WDAT index per layer-local weld: ARCON and ARCOFF share the ARCON's index;
    each ARCSWI gets its own fresh index (reconciliation §11.3, confirmed against the M1_2
    native ARCSWI capture). Returns {ordinal: index}."""
    indices = {}
    shared = None
    index = start_index
    for ordinal, role in enumerate(root, start=1):
        if role.kind == ARCON:
            shared = index
            indices[ordinal] = shared
            index += 1
        elif role.kind == ARCOFF:
            indices[ordinal] = shared
        else:
            indices[ordinal] = index
            index += 1
    return indices, index


def _wdat_var(layer: int, index: int, suffix: str) -> str:
    base = f"WDAT{index:02d}{suffix}"
    return base if layer == 0 else f"L{layer}_{base}"


def _cpdat(point: str) -> str:
    return f"CPDAT{point}"


def _ldat(point: str) -> str:
    return f"LCPDAT{point}"


def _fdat(point: str) -> str:
    return f"FP{point[1:]}"


def _xp(point: str) -> str:
    return f"XP{point[1:]}"


def _emit_role(layer: int, role: WeldPoint, wdat: str, tool_base: str) -> list:
    kind = role.kind
    point = role.point
    wp = role.weld_point_var
    src_point = point if layer == 0 else f"Shifted{point}"
    is_root = layer == 0
    is_circular = role.via_point is not None
    motion_type = "CIRC" if is_circular else "LIN"
    motion_target = _xp(point) if is_root else f"AmlGetPos({_xp(point)}, LayerOffset{layer}, {wp}, AmlInfo, )"
    if is_circular:
        via_target = _xp(role.via_point) if is_root else (
            f"AmlGetPos({_xp(role.via_point)}, LayerOffset{layer}, "
            f"{role.via_weld_point_var}, AmlInfo, )"
        )
        motion_target = f"{via_target}, {motion_target}"
    lines = []

    if kind == ARCON:
        header = f";FOLD {_ROLE_TOKEN[kind] if is_root else _ROLE_TOKEN_ML[kind]} {wdat} {motion_type} {src_point} Vel={_vel(role)} m/s {_cpdat(point)} {tool_base} ;%{{PE}}"
    elif kind == ARCOFF:
        header = f";FOLD {_ROLE_TOKEN[kind] if is_root else _ROLE_TOKEN_ML[kind]} {wdat} {motion_type} {src_point} Vel={_vel(role)} m/s {_cpdat(point)} {tool_base} ;%{{PE}}"
    else:  # ARCSWI: root shows "CONT Vel=..."; filler shows neither (reconciliation, H3 evidence)
        points = f"{role.via_point} {src_point}" if is_circular else src_point
        header = f";FOLD {_ROLE_TOKEN[kind] if is_root else _ROLE_TOKEN_ML[kind]} {wdat} {motion_type} {points}" + (f" CONT Vel={_vel(role)} m/s" if is_root else "") + f" {_cpdat(point)} {tool_base} ;%{{PE}}"

    lines.append(header)
    lines.append("  ;FOLD Parameters ;%{h}")
    ilf = _ROLE_ILF[kind][:-3] + "circ" if is_circular else _ROLE_ILF[kind]
    help_point = f" Kuka.HelpPointName={role.via_point};" if is_circular else ""
    lines.append(f"    ;Params IlfProvider=kukaroboter.arctech.{ilf}; Kuka.IsGlobalPoint=False; Kuka.PointName={point};{help_point} "
                  f"Kuka.BlendingEnabled=True; Kuka.MoveDataName={_cpdat(point)}; Kuka.VelocityPath=0.008; Kuka.CurrentCDSetIndex=0; "
                  f"Kuka.MovementParameterFieldEnabled=True; ArcTech.WdatVarName={wdat}; ArcTech.Basic=3.7.2.112; "
                  f"ArcTech.Advanced=3.7.1.9; ArcTech.Sense=3.7.1; ArcTech.Multilayer=3.7.1.4; ArcTech.ML.Id={role.ml_id}")
    lines.append("  ;ENDFOLD")
    lines.append("  $BWDSTART = FALSE")
    lines.append(f"  LDAT_ACT = {_ldat(point)}")
    lines.append(f"  FDAT_ACT = {_fdat(point)}")

    if kind == ARCON:
        lines.append(f"  BAS(#CP_PARAMS,{_vel(role)})")
    else:
        lines.append("  BAS(#CP_PARAMS, gArcBasVelDefinition)")
    lines.append("  SET_CD_PARAMS (0)")

    if kind == ARCON:
        lines.append(f"  TRIGGER WHEN DISTANCE = 1 DELAY = ArcGetDelay(#PreDefinition, {wdat}) DO ArcMainNG(#PreDefinition, {wdat}, {wp}) PRIO = -1")
        lines.append(f"  TRIGGER WHEN PATH = ArcGetPath(#OnTheFlyArcOn, {wdat}) DELAY = ArcGetDelay(#GasPreflow, {wdat}) DO ArcMainNG(#GasPreflow, {wdat}, {wp}) PRIO = -1")
        lines.append(f"  TRIGGER WHEN PATH = ArcGetPath(#OnTheFlyArcOn, {wdat}) DELAY = ArcGetDelay(#ArcPreOn, {wdat}) DO ArcMainNG(#ArcOnMoveStd, {wdat}, {wp}) PRIO = -1 ")
        lines.append(f"  ArcMainNG(#ArcOnBeforeMoveStd, {wdat}, {wp})")
        lines.append(f"  {motion_type} {motion_target}" + (" " if is_root else ""))
        lines.append(f"  ArcMainNG(#ArcOnAfterMoveStd, {wdat}, {wp})")
        if is_root:
            lines.append(f"  TRIGGER WHEN DISTANCE = 0 DELAY = ArcGetDelay(#MlDelayArcOn, {wdat}) DO AmlSetPos(#ArcOnMoveStd, {wdat}, {wp}, ) PRIO = -1")
    elif kind == ARCSWI:
        point_args = f"{wp}, {role.via_weld_point_var}" if is_circular else wp
        lines.append(f"  TRIGGER WHEN DISTANCE = 1 DELAY = 0 DO ArcMainNG(#ArcSwiMoveStd, {wdat}, {point_args}) PRIO = -1")
        if is_root:
            set_pos_tail = role.via_weld_point_var if is_circular else ""
            lines.append(f"  TRIGGER WHEN PATH = ArcGetPath(#MlPathArcSwi, {wdat}) DELAY = ArcGetDelay(#MlDelayArcSwi, {wdat}) DO AmlSetPos(#ArcSwiMoveStd, {wdat}, {wp}, {set_pos_tail}) PRIO = -1")
        lines.append(f"  ArcMainNG(#ArcSwiBeforeMoveStd, {wdat}, {point_args})")
        blend = " C_DIS C_DIS " if is_circular else " C_DIS "
        lines.append(f"  {motion_type} {motion_target}{blend}")
        lines.append(f"  ArcMainNG(#ArcSwiAfterMoveStd, {wdat}, {point_args})")
    else:  # ARCOFF
        lines.append(f"  TRIGGER WHEN PATH = ArcGetPath(#ArcOffBefore, {wdat}) DELAY = 0 DO ArcMainNG(#ArcOffBeforeOffStd, {wdat}, {wp}) PRIO = -1")
        lines.append(f"  TRIGGER WHEN PATH = ArcGetPath(#ArcOffBefore2, {wdat}) DELAY = 0 DO ArcMainNG(#ArcOffBeforeOffStd2, {wdat}, {wp}) PRIO = -1")
        lines.append(f"  TRIGGER WHEN PATH = ArcGetPath(#OnTheFlyArcOff, {wdat}) DELAY = 0 DO ArcMainNG(#ArcOffMoveStd, {wdat}, {wp}) PRIO = -1")
        if is_root:
            lines.append(f"  TRIGGER WHEN PATH = ArcGetPath(#MlPathArcOff, {wdat}) DELAY = ArcGetDelay(#MlDelayArcOff, {wdat}) DO AmlSetPos(#ArcOffMoveStd, {wdat}, {wp}, ) PRIO = -1")
        lines.append(f"  ArcMainNG(#ArcOffBeforeMoveStd, {wdat}, {wp})")
        lines.append(f"  {motion_type} {motion_target}" + (" " if is_root else ""))
        lines.append(f"  ArcMainNG(#ArcOffAfterMoveStd, {wdat}, {wp})")

    lines.append(";ENDFOLD")
    return lines


def _emit_layer(layer: int, root: Sequence[WeldPoint], tool_base: str, start_index: int, suffix: str):
    indices, next_index = _wdat_indices(root, start_index)
    lines = []
    for ordinal, role in enumerate(root, start=1):
        wdat = _wdat_var(layer, indices[ordinal], suffix)
        block = _emit_role(layer, role, wdat, tool_base)
        lines.extend(block)
        if role.kind != ARCOFF:
            lines.append("")
    return lines, next_index


def build_block_lines(
    root: Sequence[WeldPoint],
    fillers: Sequence[FillerLayer],
    tool_base: str,
    operation_labels: Optional[Sequence[str]] = None,
    wdat_suffix: str = "_01_050",
    wdat_start_index: int = 1,
) -> list:
    """Build the inline ";FOLD ArcTech Multilayer Block ... ;ENDFOLD End ArcTech Multilayer
    Block ;%{V}" lines for one seam, embedded directly in the caller's own program (no separate
    subprogram/DEF wrapper - H3 and the real `ML2`/`M1_2` native captures embed it inline in the
    same top-level program, they do not call out to a per-seam module).

    root: the root layer's weld commands, ARCON first, ARCOFF last (§11.2). ARCSWI entries in
    between are optional and may repeat.
    fillers: Direct-only filler layers (reconciliation F15; reverse is a separate, ungated path
    the caller must not reach while MultiLayerAmlCapability.REVERSE_DIRECTION_SUPPORTED is False).
    operation_labels: one "; Operation: ..." comment per layer (root first), or None to omit.
    Returns the line list; the caller is responsible for tracking the next free WDAT index.
    """
    if not root or root[0].kind != ARCON or root[-1].kind != ARCOFF:
        raise SeamShapeError("root must start with ARCON and end with ARCOFF")

    lines = []
    lines.append(";FOLD ArcTech Multilayer Block {AmlInfo.info[]} {gAmlActLayerStr[]} ;%{PO};%{PE} ;FOLD SPLINE MULTILAYER")
    lines.append(";FOLD  ;%{H}")
    lines.append(";FOLD Parameters ;%{h}")
    lines.append(";Params IlfProvider=KukaRoboter.ArcTech.Multilayer.Block; ArcTech.Basic=3.7.2.112; ArcTech.Multilayer=3.7.1.4")
    lines.append(";ENDFOLD")
    lines.append(";FOLD  ;%{h}")
    lines.append("AmlBlockBegin(gAmlSelectLayer, AmlInfo)")
    lines.append("SWITCH gAmlActLayer")
    lines.append("CASE 0")
    lines.append("AmlBlockCaseBegin(gAmlActLayer, AmlInfo)")
    lines.append(";ENDFOLD")
    lines.append(";ENDFOLD")
    lines.append(";FOLD Root Layer ;%{PO}")
    lines.append("")
    if operation_labels:
        lines.append(f"; Operation: {operation_labels[0]}")
        lines.append("")

    body, next_index = _emit_layer(0, root, tool_base, wdat_start_index, wdat_suffix)
    lines.extend(body)
    lines.append(";FOLD  ;%{h}")
    lines.append("  AmlBlockCaseEnd(gAmlActLayer, AmlInfo)")
    lines.append(";ENDFOLD")
    lines.append(";ENDFOLD End Root Layer ;%{V}")

    for i, filler in enumerate(fillers, start=1):
        n = filler.number
        lines.append(f";FOLD Layer {n} [-->] {{{filler.frame_name}}} ;%{{P}} ;FOLD SPLINE MULTILAYER")
        lines.append(";FOLD  ;%{H}")
        lines.append(";FOLD Parameters ;%{h}")
        lines.append(f";Params IlfProvider=KukaRoboter.ArcTech.Multilayer.Layer; ArcTech.ML.LayerDirection=Direct; "
                      f"ArcTech.ML.LayerNumber={n}; ArcTech.ML.LayerFrameShift={filler.frame_name}; "
                      f"ArcTech.Basic=3.7.2.112; ArcTech.Multilayer=3.7.1.4")
        lines.append(";ENDFOLD")
        lines.append(f"CASE {n}")
        lines.append("  AmlBlockCaseBegin(gAmlActLayer, AmlInfo)")
        lines.append(";ENDFOLD")
        lines.append("")
        if operation_labels and i < len(operation_labels):
            lines.append(f"; Operation: {operation_labels[i]}")
            lines.append("")
        body, next_index = _emit_layer(n, root, tool_base, next_index, wdat_suffix)
        lines.extend(body)
        lines.append(f";FOLD LayerEnd{n} ;%{{H}}")
        lines.append("  AmlBlockCaseEnd(gAmlActLayer, AmlInfo)")
        lines.append(f";ENDFOLD LayerEnd{n}")
        lines.append(f";ENDFOLD End Layer {n} ;%{{V}}")

    lines.append(";FOLD BlockEnd ;%{H}")
    lines.append("DEFAULT")
    lines.append("  AmlBlockDefault(gAmlActLayer, AmlInfo)")
    lines.append("ENDSWITCH")
    lines.append("AmlBlockEnd(gAmlActLayer, AmlInfo)")
    lines.append(";ENDFOLD End BlockEnd")
    lines.append(";ENDFOLD End ArcTech Multilayer Block ;%{V}")
    return lines


def build_seam_module(
    module_name: str,
    root: Sequence[WeldPoint],
    fillers: Sequence[FillerLayer],
    tool_base: str,
    operation_labels: Optional[Sequence[str]] = None,
    wdat_suffix: str = "_01_050",
    program_meta: Optional[dict] = None,
) -> str:
    """Build a full standalone-file rendering of build_block_lines, for the golden/unit-test
    fixtures only (AML01_S01/AML02_S01). The downloader itself never uses this: it embeds
    build_block_lines directly inline in the current program (see that function's docstring)."""
    meta = program_meta or {}
    lines = []
    lines.append("&ACCESS RVP")
    lines.append("&REL 10")
    lines.append("&PARAM EDITMASK = *")
    lines.append(f"DEF {module_name}( )")
    lines.append("; KRC4")
    lines.append(";FOLD BASISTECH INI")
    lines.append("  GLOBAL INTERRUPT DECL 3 WHEN $STOPMESS==TRUE DO IR_STOPM ( )")
    lines.append("  INTERRUPT ON 3 ")
    lines.append("  BAS (#INITMOV,0 )")
    lines.append(";ENDFOLD (BASISTECH INI)")
    lines.append("")
    lines.append(";***************************************************")
    lines.append(f"; PROGRAM         = {module_name}.src")
    lines.append("; MANUFACTURER    = Kuka")
    lines.append("; SERIES          = ")
    lines.append(f"; CREATE          = DATE {meta.get('create', '')} TIME {meta.get('create_time', '')}")
    lines.append(f"; MODIFIED        = DATE {meta.get('modified', '')} TIME {meta.get('modified_time', '')}")
    lines.append("; VERSION         = 1.2")
    lines.append("; Downloader      = KUKA_KRC5_Arc_Welding.py")
    lines.append(f"; User            = {meta.get('user', '')}")
    lines.append(";***************************************************")
    lines.append("; KSS Version     = 8.7")
    lines.append(";***************************************************")
    lines.append("; ArcTech Version       = 3.7.2.112")
    lines.append("; ArcTech Adv. Ver.     = 3.7.1.9")
    lines.append("; ArcTechSense Ver.     = 3.7.1")
    lines.append("; TouchSense Ver.       = 3.8.1.0")
    lines.append("; SeamTechFinding Ver.  = 3.5.0")
    lines.append("; SeamTechTracking Ver. = 3.5.0")
    lines.append(";***************************************************")
    lines.append("")
    lines.append("; Operation group:  GRP001")
    lines.append("")
    lines.extend(build_block_lines(root, fillers, tool_base, operation_labels, wdat_suffix))
    lines.append("END")

    return "\n".join(lines) + "\n"

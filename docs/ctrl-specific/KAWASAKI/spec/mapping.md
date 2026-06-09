# Kawasaki AS-Language — Event-to-Output Mapping

This document maps FASTSUITE E2 OLP events to their corresponding Kawasaki AS-language output.

## Motion Instructions

| E2 Context | AS Output |
|------------|-----------|
| Linear motion (normal) | `LMOVE posTarget` |
| Linear motion (weld, first after ArcOn) | `LWS posTarget ` |
| Linear motion (weld, continuous) | `LWC posTarget ,condNum` |
| Linear motion (weld, last = LWE) | `LWE posTarget ,condNum[,craterCondNum]` |
| Circular via-point (normal) | `C1MOVE viaTarget` |
| Circular endpoint (normal) | `C2MOVE posTarget` |
| Circular via-point (weld) | `C1WC viaTarget ,condNum` |
| Circular endpoint (weld) | `C2WC posTarget ,condNum` |
| Joint motion | `JMOVE #posTarget` |

### Position Target Wrapping

| Condition | Format |
|-----------|--------|
| Normal cartesian | `posName` |
| Rotary base active (`ROTBASE_ON=1`) | `TRSUB(posName)` |
| Touch offset active | `offset + posName` |
| Both rotary + touch | `TRSUB(offset + posName)` |
| Explicit mode, cartesian | `TRANS(x,y,z,o,a,t,e1,e2,...)` |
| Explicit mode, joint | `#[j1,j2,j3,j4,j5,j6]` |

---

## Built-In Events

### Speed

| E2 Attribute | AS Output |
|--------------|-----------|
| PathType=Contour, Value=v | `SPEED {v*1000} MM/S ALWAYS` |
| PathType=PointToPoint, Value=v | `SPEED {v} ALWAYS` |
| Suppressed when `arcOnActive=True` | *(no output)* |

### Accuracy

| E2 Attribute | AS Output |
|--------------|-----------|
| Criteria=Distance, Value>0 | `ACCURACY {v*1000} ALWAYS` |
| Criteria=On/Off → sets CP state | *(handled via CP)* |
| Suppressed when `arcOnActive=True` | *(no output)* |

### CP (Continuous Path)

| Rule | AS Output |
|------|-----------|
| First time state changes to OFF | `CP OFF` |
| Never emitted ON | *(no CP ON ever)* |
| Suppressed in touch/explicit mode | *(no output)* |

### Acceleration

| E2 Attribute | AS Output |
|--------------|-----------|
| Value=v | `ACCEL {v} ALWAYS` |
| Suppressed in touch sensing mode | *(no output)* |

### Dwell

*(Not currently mapped — extend if needed)*

---

## Signal Events

### LogicPort — CENE2SetSignal

| E2 Attributes | AS Output |
|---------------|-----------|
| SignalValue=True | `SIGNAL {address} ; {name}=On` |
| SignalValue=False | `SIGNAL -{address} ; {name}=Off` |

### LogicPort — CENE2WaitForSignal

| E2 Attributes | AS Output |
|---------------|-----------|
| SignalValue=True | `SWAIT {address} ; {name}=On` |
| SignalValue=False | `SWAIT -{address} ; {name}=Off` |

### SetResourcePort (multi-signal container)

Per signal in container:

| E2 Attributes | AS Output |
|---------------|-----------|
| SignalValue=True | `SIGNAL {address} ; {name}=On` |
| SignalValue=False | `SIGNAL -{address} ; {name}=Off` |

### WaitForResourcePort (multi-signal container)

Per signal in container:

| E2 Attributes | AS Output |
|---------------|-----------|
| SignalValue=True | `WAIT SIG({address}) ; {name}=On` |
| SignalValue=False | `WAIT SIG(-{address}) ; {name}=Off` |

---

## Arc Welding Events

### ArcOnEvent

Output order (all items conditional):

1. `SET_ARC_W1JOBNO {condNum} = {jobNum}`
2. `SETCONDW1 {condNum} = {speed},{wireFeed},{arcLen},{pulseDyn},{wireRetract},{weaveWidth},{weaveFreq},{weavePattern}`
3. *(if crater)* `SET_ARC_W2JOBNO {craterCondNum} = {craterJobNum}`
4. *(if crater)* `SETCONDW2 {craterCondNum} = {time},{current/wire},{voltage/arcLen},{pulseDyn},{wireRetract}`
5. *(if DLSSDown=Enabled)* `SETCONDW3 {preHeatTime},,,,,,{weaveWidth},{weaveFreq}, {weaveNum}`
6. *(if DLPatternNum>1)* `SSENSPTN {mappedPattern}`
7. *(if DLPatternNum>1)* `SSENS_SET {startDist}, {reliefDist}, {distInGroove}`
8. *(if DLPatternNum>1)* `SSENSING ON`
9. *(if DLRTPM=Enabled && DLWCRTPMNum=2)*:
   - `RTPM2_STARTGain ON/OFF, [gainTime, vertCur, horizCur, changeCur]`
   - `RT2DLYTIME {delayTime}`
   - `SET_ARC_RTPMREF {wireStick}`
   - `RT2Gain {vertGain}, {horizGain}`
   - `RT2BIAS {vertBias}, {horizBias}`
   - `RTPM ON`

### ArcWeldConditionEvent (mid-weld parameter change)

Output order (DIFFERENT from ArcOn):

1. *(if weave pattern)* `;WeavePattern: {name}` + `;WeaveNum: {num}`
2. *(if DLSSDown=Enabled)* `SETCONDW3 ...`
3. *(if RTPM)* RTPM block (same as ArcOn)
4. *(if sensing)* `SSENSPTN` + `SSENS_SET` + `SSENSING ON`
5. *(if DLSetArcWeldMode≠None)* `SET_ARC_WELDMODE {mode}`
6. `SET_ARC_W1JOBNO` + `SETCONDW1`
7. *(if crater)* `SET_ARC_W2JOBNO` + `SETCONDW2`

### ArcOffEvent

Triggers `arcOnLastProcessCurve=True` → next HandleMotion emits `LWE` instead of `LWC`.

After LWE:
- *(if sensing was active)* `SSENSING OFF`
- *(if RTPM was active)* `RTPM OFF`

### SETCONDW1 Parameter Mapping

| condMode=0 (Synergic) | condMode=1 (Manual) |
|------------------------|---------------------|
| WeldSpeed | WeldSpeed |
| WireFeedSpeed | WeldCurrent |
| ArcLengthCorr | WeldVoltage |
| PulseDynamicCorr | PulseDynamicCorr |
| WireRetractCorr | WireRetractCorr |
| + WeaveWidth, WeaveFreq, WeavePatternNum | + same |

---

## Laser Tracker / LT Events

### LT_Param_Event

| E2 Attribute | AS Output |
|--------------|-----------|
| DLJobNumberLaser | `LJT {jobNum}` |
| DLLTBiasX/Y/Z (m→mm) | `LTBIAS {x},{y},{z}` |
| DLLTOff=True | `LT OFF` |

### LTOnEvent / LTOffEvent

| Event | AS Output |
|-------|-----------|
| LTOnEvent | `LT ON` |
| LTOffEvent | `LT OFF` |

---

## SPS (Seam Pattern Sensing) Event

| E2 Attribute | AS Output |
|--------------|-----------|
| DLPatternNum, DLStartDist, DLReliefDist, DLDistInGroove | `SSENSPTN {pattern},{start},{relief},{dist}` |

---

## Text Event

| E2 Attributes | AS Output |
|---------------|-----------|
| IsComment=True | `; {text}` |
| IsComment=False | `{text}` (raw line) |

---

## Touch Sensing

### Collision Sequence (per touch point)

```
CALL kr_touch(refPos, offsetVar, rotbaseOn, sensingLen, sensingSpd, frameRefId)
BREAK
```

### Frame Calculation (Frame3pConnect only, after 3 points)

```
CALL kr_frame(FRAME_REF_PT_1, FRAME_REF_PT_2, FRAME_REF_PT_3, FRAME_PT_1, FRAME_PT_2, FRAME_PT_3, offsetVar)
```

### Subroutines

`kr_touch` and `kr_frame` are emitted after `.END` and before `.TRANS` when `hasTouchSensing=True`.

---

## Sensing Pattern Mapping

| DLPatternNum (E2) | AS Pattern Number |
|--------------------|-------------------|
| 2–7 | +99 (→ 101–106) |
| 8–12 | −7 (→ 1–5) |
| Other | direct |

---

## File Structure

```
.PROGRAM {name}()
  ; FASTSUITE_II – Kawasaki Translator
  TOOL {toolIdx}
  BASE {baseIdx} [/ ROTBASE_ON=1]
  [CP OFF]
  HOME
  ... body ...
  HOME
.END
[kr_touch subroutine]
[kr_frame subroutine]
.TRANS
  {name} {x} {y} {z} {o} {a} {t} [{e1} {e2} ...]
  ... (sorted alphabetically)
.JOINTS
  #{name} {j1} {j2} {j3} {j4} {j5} {j6} [{e1} {e2} ...]
  ... (sorted alphabetically)
```

---

## Unit Conversion Reference

| Quantity | E2 Unit | AS Unit | Conversion |
|----------|---------|---------|------------|
| Position XYZ | m | mm | ×1000 |
| Speed (Contour) | m/s | mm/s | ×1000 |
| Speed (PTP) | % | % | direct |
| Accuracy | m | mm | ×1000 |
| Weave Width | m | mm | ×1000 |
| LT Bias | m | mm | ×1000 |
| Euler angles | deg (XYZs) | deg (ZYZr) | ConvertEuler |
| Joint angles | deg | deg | direct |
| Ext. prismatic | m | mm | ×1000 |
| Ext. revolute | deg | deg | direct |

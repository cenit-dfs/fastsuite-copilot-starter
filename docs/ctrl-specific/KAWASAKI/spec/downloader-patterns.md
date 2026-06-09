# Kawasaki AS-Language Downloader — Patterns & Gotchas

Source: `OLPTranslators/KAWASAKI/KAWASAKI.py`
Golden files: `community/scenarios/ArcWeldingTechnology/KAWASAKI/Standard/golden/`
Reference dumps: `community/scenarios/ArcWeldingTechnology/KAWASAKI/Standard/reference/`

---

## Euler Convention

- E2 internal: `Euler_XYZs` (static XYZ)
- Kawasaki OAT: `Euler_ZYZr` (rotating ZYZ)
- Conversion: `ConvertEuler(rx, ry, rz, Euler_XYZs, Euler_ZYZr)` → (O, A, T)

## Unit Conversions (m → mm × 1000)

| What | Source | Target |
|------|--------|--------|
| Position XYZ | meters | mm |
| Speed (Contour) | m/s | mm/s |
| Accuracy value | meters | mm |
| WeaveWidth | meters | mm |
| LT bias X/Y/Z | meters | mm |
| Speed (PTP) | % | % (no conversion) |
| Joint axes | degrees | degrees (no conversion) |

## State Machine Flags

| Flag | Set When | Cleared When | Effect |
|------|----------|--------------|--------|
| `arcOnActive` | ArcOn event fires | LWE motion output | Suppresses SPEED, ACCURACY output |
| `arcOnIsFirstMotion` | ArcOn event fires | First motion after ArcOn | Emits `LWS` instead of `LMOVE` |
| `arcOnLastProcessCurve` | ArcOff event fires | LWE motion output | Emits `LWE` instead of `LMOVE` |
| `inWeldSection` | ArcOn fires | ArcOff fires | Broader weld-active flag |
| `explicitMode` | Resource attr `CENOlpDataOutputStyle=Explicit` | — | No CP, no TRSUB, inline positions |
| `rotbaseOn` | Base profile name starts with `ROT_BASE` | Next operation with non-ROT base | Wraps positions in `TRSUB()` |
| `hasTouchSensing` | TouchSensing workmethod detected | — | Triggers kr_touch/kr_frame emission |

## Buffered Motion Data

- `pendingSpeed`, `pendingAccel`, `pendingCp`, `pendingAccuracy` + `last*` tracking
- Flushed in `_flushPendingMotionData()` BEFORE each motion line
- SPEED suppressed when `arcOnActive=True`
- ACCURACY suppressed when `arcOnActive=True`
- CP: only `OFF`, only once (never `ON`, never toggled back)

## ArcOn Output Order

```
SET_ARC_W1JOBNO → SETCONDW1 (with weave)
→ SET_ARC_W2JOBNO + SETCONDW2 (crater, if enabled)
→ SETCONDW3 (software slowdown)
→ SSENSPTN + SSENS_SET + SSENSING (seam sensing)
→ RTPM block (real-time path modification)
```

## ArcWeldCondition Output Order (DIFFERENT from ArcOn)

```
weave comments → SETCONDW3 → RTPM
→ SSENSPTN + SSENS_SET + SSENSING
→ SET_ARC_WELDMODE
→ SET_ARC_W1JOBNO + SETCONDW1
→ SET_ARC_W2JOBNO + SETCONDW2
```

## Signal Types

| Event | EventType attribute | Output |
|-------|-------------------|--------|
| LogicPort | `CENE2SetSignal` | `SIGNAL {sign}{addr} ; {name}={On/Off}` |
| LogicPort | `CENE2WaitForSignal` | `SWAIT {sign}{addr} ; {name}={On/Off}` |
| SetResourcePort | — | `SIGNAL {sign}{addr} ; {name}={On/Off}` (per signal) |
| WaitForResourcePort | — | `WAIT SIG({sign}{addr}) ; {name}={On/Off}` (per signal) |

## LWE Crater Format

```
LWE posTarget ,condNum,craterCondNum
```

Note: space before comma is intentional in implicit mode.

## Main/Subprogram Output

- `SEPARATE_SUBPROGRAM_FILES = True` — class-level flag
- Container main emits only `.PROGRAM` + `CALL` statements + `.END`
- Subprograms get full output (header, motions, .TRANS, .JOINTS)
- kr_touch/kr_frame subroutines emitted **only in main program file** via pre-scan
- Per-program state fully reset in `ProgramStart` (TransBlock, JointsBlock, all flags)
- `.TRANS`/`.JOINTS` sections only emitted when buffers are non-empty

## Output Structure

```
# Container main program (P1MAIN.as):
.PROGRAM P1MAIN()
;Compensate track/rail/positioner
ROTBASE_ON = 0
CALL S1SUB1
CALL S1SUB2
.END
.PROGRAM kr_touch(...)    ; if any subprogram uses touch sensing
  ...
.END
.PROGRAM kr_frame(...)    ; if any subprogram uses touch sensing
  ...
.END

# Subprogram (S1SUB1.as):
.PROGRAM S1SUB1()
;Compensate track/rail/positioner
ROTBASE_ON = 0
BASE NULL
TOOL S1SUB1_TOOL1
RIGHTY
ABOVE
DWRIST
;Operation Group: GRP001
;Operation: WG2_Seam1
SPEED 50 ALWAYS
ACCEL 100 ALWAYS
JMOVE ...
...
.END
.TRANS
  {sorted position data}
.END
.JOINTS
  {sorted joint data}
.END
```

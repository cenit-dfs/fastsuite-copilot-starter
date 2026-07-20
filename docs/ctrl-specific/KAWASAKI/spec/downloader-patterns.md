# Kawasaki AS-Language Downloader — Patterns & Gotchas

Canonical source: `community/OLPTranslators/KAWASAKI/KAWASAKI_AS.py`
Golden files: `community/scenarios/ArcWeldingTechnology/KAWASAKI/Standard/golden/`
Reference dumps: `community/scenarios/ArcWeldingTechnology/KAWASAKI/Standard/reference/`

The starter repository keeps the agent workflow and controller-specific knowledge. The finished, general-purpose downloader lives in the `community` submodule and may later be promoted into an E2 product release after product qualification. Do not keep a second editable downloader copy under the starter's `OLPTranslators/KAWASAKI/` folder.

---

## Euler Convention

- E2 internal: `Euler_XYZs` (static XYZ)
- Kawasaki OAT: `Euler_ZYZr` (rotating ZYZ)
- Conversion: `ConvertEuler(rx, ry, rz, Euler_XYZs, Euler_ZYZr)` → (O, A, T)

## Boolean Attributes

`attribute.GetValue()` returns a Python `bool` for `BoolAttribute`, not the strings `"True"` or `"False"`. Prefer direct truth testing (`if attr.GetValue():`) when the type is known. If existing generic code normalizes mixed attribute types through text, compare `str(attr.GetValue()) == "True"`; never compare the raw boolean directly with a string.

This affects `IsComment`, `DLLTOff`, `DLSSDown`, `DLRTPM`, `ExactStop`, boolean `SignalValue`, and other boolean event or operation attributes.

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

## Numeric Formatting

Use `_fmtRound1(value)` for AS values that require one-decimal rounding without a redundant `.0`: `0.0` becomes `0`, `4.6` remains `4.6`, and `100.0` becomes `100`.

## ROT_BASE Program Header

- Base-profile names beginning with `ROT_BASE` (case-insensitive) enable `ROTBASE_ON = 1`.
- The first operation using such a profile emits `BASE {profileName}` in the `.PROGRAM` header.
- That base profile is emitted once in `.TRANS`, with XYZ converted from meters to millimeters and orientation converted from E2 XYZ to Kawasaki OAT.
- Missing base profiles and profiles not beginning with `ROT_BASE` emit `BASE NULL` and no base-frame `.TRANS` entry.

## Main/Subprogram Output

- `SEPARATE_SUBPROGRAM_FILES = True` — class-level flag
- Container main emits only `.PROGRAM` + `CALL` statements + `.END`
- Subprograms get full output (header, motions, .TRANS, .JOINTS)
- kr_touch/kr_frame subroutines emitted **only in main program file** via pre-scan
- Per-program state fully reset in `ProgramStart` (TransBlock, JointsBlock, all flags)
- `.TRANS`/`.JOINTS` sections only emitted when buffers are non-empty
- A nonzero program-level `GroupNumber` attribute emits `GROUP {value}` immediately after `.PROGRAM`; zero omits the line

## Output Structure

```
# Container main program (P1MAIN.as):
.PROGRAM P1MAIN()
GROUP 1                 ; only when GroupNumber is nonzero
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
GROUP 1                 ; only when GroupNumber is nonzero
;Compensate track/rail/positioner
ROTBASE_ON = 0
;Operation Group: GRP001
;Operation: WG2_Seam1
;Compensate track/rail/positioner
ROTBASE_ON = 1
BASE Rot_Base            ; for a ROT_BASE profile; otherwise BASE NULL
TOOL S1SUB1_TOOL1
RIGHTY
ABOVE
DWRIST
SPEED 50 ALWAYS
ACCEL 100 ALWAYS
JMOVE ...
...
.END
.TRANS
  Rot_Base {x} {y} {z} {o} {a} {t}  # only for a ROT_BASE profile
  {sorted position data}
.END
.JOINTS
  {sorted joint data}
.END
```

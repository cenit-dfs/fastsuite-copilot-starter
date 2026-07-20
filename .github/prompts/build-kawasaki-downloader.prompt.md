---
description: "Maintain or validate the community KAWASAKI AS-language OLP downloader from reference dumps, golden files, and the mapping document."
agent: "agent"
model: ["Claude Opus 4 (copilot)", "Claude Sonnet 4 (copilot)"]
tools: ["search", "editFiles", "runInTerminal"]
---

# Maintain the KAWASAKI AS Downloader

You are maintaining the community FASTSUITE E2 downloader that generates Kawasaki AS-language robot programs (`.as`) for arc welding with touch sensing. The canonical implementation already exists; do not scaffold a second long-lived copy in the starter.

## Step 0 — Read Required Context

Before writing any code, read these files **in full**:

1. **Downloader skill** — lifecycle, API reference, event handling, common mistakes, advanced patterns:
   [SKILL.md](../../skills/downloader/SKILL.md)

2. **Kawasaki-specific rules** — ownership, BoolAttribute trap, units, buffering, and state-machine invariants:
   [kawasaki.md](../../skills/downloader/references/kawasaki.md)

3. **Canonical downloader** — maintained implementation:
   [KAWASAKI_AS.py](../../community/OLPTranslators/KAWASAKI/KAWASAKI_AS.py)

4. **Mapping document** — the Rosetta Stone connecting API data to Kawasaki output (sections 1–26):
   [MAPPING.md](../../community/scenarios/ArcWeldingTechnology/KAWASAKI/Standard/MAPPING.md)

5. **Simplest golden file** — expected output for basic motions (no welding, no touch):
   [PG06_BASIC.as](../../community/scenarios/ArcWeldingTechnology/KAWASAKI/Standard/golden/PG06_BASIC.as)

6. **Simplest reference dump** — annotated API data that produced PG06_BASIC:
   [PG06_BASIC.txt](../../community/scenarios/ArcWeldingTechnology/KAWASAKI/Standard/reference/PG06_BASIC.txt)

7. **Base template** — structural comparison only; do not overwrite the canonical implementation:
   [base_downloader.py](../../skills/downloader/templates/base_downloader.py)

## Step 1 — Establish the Change Scope

Work from `community/OLPTranslators/KAWASAKI/KAWASAKI_AS.py` only when the user explicitly requests a community contribution. For exploratory development, a temporary starter copy may be created from that canonical file, but remove it after the accepted change is returned to community. Keep `DOWNLOAD_CLASS_NAME = "KAWASAKI_AS"` aligned with class `KAWASAKI_AS` and filename `KAWASAKI_AS.py`.

## Step 2 — Implement Basic Motion (PG06_BASIC)

Using MAPPING.md sections 1–6, 13, 23, implement:

- `.PROGRAM <name>()` header with `TOOL`, `BASE`, config flags
- Buffered motion data pattern: pending Speed/Accel/CP/Accuracy flushed before each motion
- `JMOVE` / `LMOVE` dispatch based on `MotionType`
- Speed events → `SPEED n MM/S ALWAYS` (contour) or `SPEED n ALWAYS` (PTP)
- Accuracy events → `CP OFF` (only OFF, never ON, emitted once) + `ACCURACY n ALWAYS`
- Acceleration → `ACCEL n ALWAYS`
- Position accumulation in `.TRANS` block (implicit mode), sorted alphabetically
- Euler angle conversion (E2 Rx,Ry,Rz → Kawasaki O,A,T) — validate against MAPPING.md §12
- Tool profile → `.TRANS` entry
- `.END` / `.TRANS` / `.JOINTS` / file footer

**Validate**: Compare your mental output for PG06_BASIC.txt against PG06_BASIC.as line by line.

## Step 3 — Add Arc Welding (PG01_OP)

Read the additional golden + reference files:
- [PG01_OP.as](../../community/scenarios/ArcWeldingTechnology/KAWASAKI/Standard/golden/PG01_OP.as)
- [PG01_OP.txt](../../community/scenarios/ArcWeldingTechnology/KAWASAKI/Standard/reference/PG01_OP.txt)

Using MAPPING.md §8 and §23, implement:

- Read-ahead pattern: scan `eventsAfter` for ArcOn/ArcOff BEFORE outputting the motion
- `ArcOnEvent` → `SET_ARC_W1JOBNO` + `SETCONDW1` (NO W1SET)
- Weld start motion → `LWS` instead of `LMOVE`
- Weld continuous → `LWC ... ,<condition>`
- Weld end motion → `LWE ... ,<condition>[,<crater_condition>]`
- SPEED suppressed during welding (arcOnActive=True)
- ACCURACY suppressed during welding (arcOnActive=True)
- Crater fill (SETCONDW2) from `DLWC2*` attributes

## Step 4 — Add Touch Sensing (PG01_OP, PG04_SD)

Read additional golden files:
- [PG04_SD.as](../../community/scenarios/ArcWeldingTechnology/KAWASAKI/Standard/golden/PG04_SD.as)

Using MAPPING.md §9 and §25, implement:

- `POINT <name> = NULL` declarations at group start
- `TouchPointCollisionEvent` → `CALL KR_TOUCH(...)` + `BREAK`
- `ConnectTouchProcessPointEvent` → offset `<TS_ID> + <point>` in weld motions
- Touch index tracking (0 for normal, 1/2/3 for 3-point frame)
- `kr_touch` and `kr_frame` subroutines emitted between `.END` and `.TRANS`

## Step 5 — Add Advanced Features (PG03_SE)

Read:
- [PG03_SE.as](../../community/scenarios/ArcWeldingTechnology/KAWASAKI/Standard/golden/PG03_SE.as)
- [PG03_SE.txt](../../community/scenarios/ArcWeldingTechnology/KAWASAKI/Standard/reference/PG03_SE.txt)

Using MAPPING.md §17–22, implement:

- **ROTBASE / TRSUB** (§19): detect base profile name, wrap positions in `TRSUB()`
- **Signal events** (§17): LogicPort → `SIGNAL`/`SWAIT`, ResourcePort → multi-signal
- **ArcWeldConditionEvent** (§18): mid-weld parameter change (different output order from ArcOn!)
- **LT events** (§20): `LJT`, `LTBIAS`, `LT ON/OFF`
- **SPS events** (§21): `SSENSPTN`
- **Text events** (§22): comment or raw line
- **Sensing/RTPM blocks** in ArcOn: SETCONDW3, SSENSPTN+SSENS_SET+SSENSING, RTPM block

## Step 6 — Add Explicit Mode (PG07_BASIC_EXP)

Read:
- [PG07_BASIC_EXP.as](../../community/scenarios/ArcWeldingTechnology/KAWASAKI/Standard/golden/PG07_BASIC_EXP.as)

Using MAPPING.md §4 explicit mode, implement:

- Check `CENOlpDataOutputStyle` resource attribute
- If `"Explicit"`: emit `JMOVE TRANS(x, y, z, o, a, t, ext1, ext2)` inline, no `.TRANS` block
- If `"Implicit"`: emit named points + `.TRANS` block (default)

## Step 7 — Validate All Programs

For each golden file, mentally trace the reference dump through your downloader and verify the output matches. Fix any discrepancies.

Programs in order of complexity:
1. PG06_BASIC — basic motions only
2. PG07_BASIC_EXP — explicit position mode
3. PG02_SE — start-end touch sensing
4. PG04_SD — seam-distance touch sensing
5. PG01_OP — touch + arc welding combined
6. PG05_3PFR — 3-point frame touch reference
7. PG03_SE — TRSUB, signals, ArcWeldCondition, sensing, RTPM, LT, crater

Run syntax check: `python -c "import ast; ast.parse(open(r'community/OLPTranslators/KAWASAKI/KAWASAKI_AS.py').read()); print('Syntax OK')"`

## Critical Rules

- Canonical source is `community/OLPTranslators/KAWASAKI/KAWASAKI_AS.py`; do not retain a duplicate starter implementation.
- Modify `community/` only when the user explicitly requests a community contribution. Keep skills and controller documentation in the starter repository.
- Never modify `typings/` merely to make downloader code pass.
- Never modify E2 installation files (downloadStarter.py, downloader.py)
- Use `operator.GetLogOperator().LogDebug()` for debug logging, not `print()`
- **BoolAttribute.GetValue() returns Python `bool`** — always use `str(attr.GetValue()) == 'True'`
- All position values from E2 are in **meters** — multiply by 1000 for mm
- All speed values (Contour) are in **m/s** — multiply by 1000 for mm/s
- Accuracy/WeaveWidth/LT bias values are in **meters** — multiply by 1000 for mm
- **CP OFF only** — never emit CP ON, emit CP OFF once when first needed
- **SPEED/ACCURACY suppressed** between LWS and LWE (arcOnActive=True)
- Follow the callback contract in MAPPING.md §15
- Review the gotchas in MAPPING.md §16 before finishing

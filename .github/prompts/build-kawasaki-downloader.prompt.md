---
description: "Build a KAWASAKI AS-language OLP downloader from reference dumps, golden files, and the mapping document. Use when: create KAWASAKI downloader, generate KAWASAKI translator, build KAWASAKI download script."
agent: "agent"
model: ["Claude Opus 4 (copilot)", "Claude Sonnet 4 (copilot)"]
tools: ["search", "editFiles", "runInTerminal"]
---

# Build KAWASAKI Downloader

You are building a FASTSUITE E2 OLP downloader that generates Kawasaki AS-language robot programs (.as files) for arc welding.

## Step 0 — Read Required Context

Before writing any code, read these files **in full**:

1. **Downloader skill** — lifecycle, API reference, event handling, common mistakes:
   [SKILL.md](../../skills/downloader/SKILL.md)

2. **Base template** — starter downloader with all callbacks stubbed:
   [base_downloader.py](../../skills/downloader/templates/base_downloader.py)

3. **Mapping document** — the Rosetta Stone connecting API data to Kawasaki output:
   [MAPPING.md](../../community/scenarios/ArcWeldingTechnology/KAWASAKI/Standard/MAPPING.md)

4. **Simplest golden file** — expected output for basic motions (no welding, no touch):
   [PG06_BASIC.as](../../community/scenarios/ArcWeldingTechnology/KAWASAKI/Standard/golden/PG06_BASIC.as)

5. **Simplest reference dump** — annotated API data that produced PG06_BASIC:
   [PG06_BASIC.txt](../../community/scenarios/ArcWeldingTechnology/KAWASAKI/Standard/reference/PG06_BASIC.txt)

6. **Download API** — use the `obsidian-e2` MCP server to search for `Download Callback Lifecycle` and the `DULPython*` class notes in `10_API_Reference/Download/`

7. **OlpCore API** — use the `obsidian-e2` MCP server to search for `OlpCore Attributes`, `OlpCore Enumerations`, and the `OlpCorePython*` class notes in `10_API_Reference/OlpCore/`

## Step 1 — Scaffold

Create `OLPTranslators/KAWASAKI/KAWASAKI.py` by copying the base template.
Rename the class to `KAWASAKI`, set `FILE_EXTENSION = '.as'`, update `DOWNLOAD_CLASS_NAME`.

## Step 2 — Implement Basic Motion (PG06_BASIC)

Using the MAPPING.md sections 1–6 and 13, implement:

- `.PROGRAM <name>()` header with `BASE NULL`, `TOOL`, config flags
- `JMOVE` / `LMOVE` dispatch based on `MotionType`
- Speed events → `SPEED n MM/S ALWAYS` (contour) or `SPEED n ALWAYS` (PTP)
- Accuracy events → `CP ON`/`CP OFF` + `ACCURACY n ALWAYS`
- Acceleration → `ACCEL n ALWAYS`
- Position accumulation in `.TRANS` block (implicit mode)
- Euler angle conversion (E2 Rx,Ry,Rz → Kawasaki O,A,T) — validate against the known pairs in MAPPING.md §12
- Tool profile → `.TRANS` entry
- `.END` / `.TRANS` / `.END` file footer

**Validate**: Compare your mental output for PG06_BASIC.txt against PG06_BASIC.as line by line.

## Step 3 — Add Arc Welding (PG01_OP)

Read the additional golden + reference files:
- [PG01_OP.as](../../community/scenarios/ArcWeldingTechnology/KAWASAKI/Standard/golden/PG01_OP.as)
- [PG01_OP.txt](../../community/scenarios/ArcWeldingTechnology/KAWASAKI/Standard/reference/PG01_OP.txt)

Using MAPPING.md §8, implement:

- `ArcOnEvent` → `SET_ARC_W1JOBNO` + `SETCONDW1` + `W1SET`
- Weld start motion → `LWS` instead of `LMOVE`
- Weld end motion → `LWE ... ,<condition>` instead of `LMOVE`
- Crater fill parameters from `DLWC2*` attributes

## Step 4 — Add Touch Sensing (PG01_OP, PG04_SD)

Read additional golden files:
- [PG04_SD.as](../../community/scenarios/ArcWeldingTechnology/KAWASAKI/Standard/golden/PG04_SD.as)

Using MAPPING.md §9, implement:

- `POINT <name> = NULL` declarations at group start
- `TouchPointStartAppEvent` → approach speed
- `TouchPointCollisionEvent` → `CALL KR_TOUCH(...)` + `STABLE 0.1`
- `TouchPointStartRetEvent` → retract speed
- `ConnectTouchProcessPointEvent` → offset `<TS_ID> + <point>` in weld motions
- Touch index tracking (0 for normal, 1/2/3 for 3-point frame)

## Step 5 — Add Explicit Mode (PG07_BASIC_EXP)

Read:
- [PG07_BASIC_EXP.as](../../community/scenarios/ArcWeldingTechnology/KAWASAKI/Standard/golden/PG07_BASIC_EXP.as)

Using MAPPING.md §4 explicit mode, implement:

- Check `CENOlpDataOutputStyle` resource attribute
- If `"Explicit"`: emit `JMOVE TRANS(x, y, z, o, a, t, ext1, ext2)` inline
- If `"Implicit"`: emit named points + `.TRANS` block (default)

## Step 6 — Validate All Programs

For each golden file, mentally trace the reference dump through your downloader and verify the output matches. Fix any discrepancies.

Programs in order of complexity:
1. PG06_BASIC — basic motions only
2. PG07_BASIC_EXP — explicit position mode
3. PG02_SE — start-end touch sensing
4. PG04_SD — seam-distance touch sensing
5. PG01_OP — touch + arc welding combined
6. PG05_3PFR — 3-point frame touch reference

## Rules

- Output file goes to `OLPTranslators/KAWASAKI/KAWASAKI.py`
- Never modify files in `skills/`, `community/`, `docs/`, or `typings/`
- Never modify E2 installation files (downloadStarter.py, downloader.py)
- Use `operator.GetLogOperator().LogDebug()` for debug logging, not `print()`
- All position values from E2 are in **meters** — multiply by 1000 for mm
- All speed values (Contour) are in **m/s** — multiply by 1000 for mm/s
- Accuracy values are in **meters** — multiply by 1000 for mm
- Follow the callback contract in MAPPING.md §15
- Review the gotchas in MAPPING.md §16 before finishing

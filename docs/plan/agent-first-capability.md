## Plan: Agent-First Capability — Full Re-plan

> **Status (2026-06-02):** Phases 0–1C done. Phase 3 (docstring guide) done.
> Phase 2 (stub generator) answered — stubs are auto-generated from C++ headers.
> Phases 4–8 superseded by the vault plan with revised priorities below.
>
> **Consolidated plan:** See "Priority Actions" at the bottom of this file.
> The vault's `Implementation_Plan.md` is the canonical rollout plan.
> This file retained as historical context + revised priority list.

**Key Learning (2026-06-02 Kawasaki Downloader Session):**
The agent produced a 1000-line production downloader with zero Python errors in a single session using:
- `typings/` stubs (95% of API reference needs)
- `community/scenarios/` golden files + reference dumps (ground truth)
- `skills/downloader/SKILL.md` (lifecycle + patterns)
- `.instructions.md` scoped rules (auto-injected context)

The MCP vault was used ~5% — only for lifecycle callback conceptual docs.
This fundamentally shifts priorities: **patterns > API signatures > docstrings**.

---

### Phase 0 — Foundation ✅ Done
Stubs in `typings/`, Pylance wired, skills inlined.

---

### Phase 1 — Reference Corpus *(start now, parallel with Phase 3)*

Commit all vendor translators, uploaders, technology scripts, and representative test scenarios to the community repo. They serve three purposes simultaneously: agent pattern library, docstring source corpus, and public reference for all E2 users.

#### 1A — Translators & Uploaders

Source: `c:\Programs\...\E2Plugin\OLPTranslators\`

**Steps:**
1. Audit each translator for customer-specific data (controller IPs, workcell names, project paths) — classify as CLEAN / NEEDS-SCRUB / SKIP
2. Commit CLEAN + scrubbed translators to `community/OLPTranslators/<VENDOR>/`, including `Simple_Python_Translator_ul.py` and the DAIHEN + PRIMA uploaders
3. Add a short README per vendor folder

**Vendors on hand:** ABB, CLOOS, DAIHEN, DENSO, DÜRR, EPSON, FANUC, HAITIAN, JARI, KAWASAKI, KOBELCO, KUKA, LASERDYNE, MITSUBISHI, MOTOMAN, NACHI, NEURA, NUKON, PANASONIC, PRIMA, REIS, SIASUN, STÄUBLI, TRUMPF, UNIVERSAL (25 total)

#### 1B — Technology Scripts (read-only reference for downloaders)

Source: `c:\Programs\...\E2Plugin\Technologies\`

Technology scripts define which events fire, what attributes they carry, and when they appear in the motion stream. The agent needs them as context when writing downloaders — especially for arc welding and laser cutting.

**What to commit:**

| Technology | Scope | Location in community repo |
|------------|-------|---------------------------|
| **ArcWeldingTechnology/Standard** | Shared scripts: `ArcWeldingTechnology.py`, seam finding, touch sensing workmethod scripts (13 files) | `community/Technologies/ArcWeldingTechnology/Standard/Scripts/` |
| **ArcWeldingTechnology/Vendor** | Vendor-specific: ABB, CLOOS, DAIHEN, FANUC, KAWASAKI, KUKA, Motoman, NEURA, PANASONIC (9 vendors, ~10-28 scripts each) | `community/Technologies/ArcWeldingTechnology/Vendor/Standard/Scripts/` |
| **LaserCuttingTechnology/Vendor** | Vendor-specific configs: FANUC, HAITIAN, LASERDYNE, MITSUBISHI, NTC, PRIMA, Siemens, TRUMPF, UniversalLC, Generic (controller settings, tech tabs — no shared scripts) | `community/Technologies/LaserCuttingTechnology/<Vendor>/` |
| **TechnologyCommon** | Auxiliary commands: `ToolpathReport.py`, `CycleTimeDelayCalculation.py`, `DesignChangeProcessGeometriesReportScript.py` | `community/Technologies/TechnologyCommon/Standard/AuxiliaryCommands/` |

**Not committed (no customization scripts):** CavityConservation, Deburring, Drilling, FrictionWelding, Generic, Handling, Inspection, LaserWelding, NailShooting, PlasmaCutting, RemoteLaserWelding, Riveting, Rollerhemming, Routing, Screwing, Sealing, SpotWelding, Spraying, StudWelding, UltrasonicCutting, UltrasonicNdt, WaterjetCutting — these ship with no Python customization.

**Note:** Technology scripts are committed as **read-only reference** for the downloader agent. Full "agent writes technology scripts" capability is deferred to Phase 8.

#### 1C — Representative Test Scenarios

Test scenarios provide the ground truth for docstrings (what the object tree actually looks like at runtime) and the harness for agent validation (diff output vs. golden = pass/fail).

**6–7 representative scenarios** covering the diversity of robot languages, technology types, and complexity levels:

| Scenario | Vendor | Technology | What it covers | Status |
|----------|--------|------------|----------------|--------|
| Basic multi-motion | KAWASAKI | Handling | PTP/LIN/CIRC, signals, implicit + explicit mode | ✅ Already done (7 goldens + 7 dumps) |
| Most popular robot | FANUC | Handling or ArcWelding | R[]/PR[] syntax, multi-group, different motion format | |
| Arc welding | PANASONIC or DAIHEN | ArcWelding | Process start/stop events, weld condition attributes | |
| Laser cutting | PRIMA or TRUMPF | LaserCutting | Laser power events, XML/special output format | |
| Multi-plugin complex | ABB IRC5 | Handling + ArcWelding | RAPID modules, multi-plugin architecture | |
| Simple baseline | EPSON or DENSO | Handling | Minimal event set, straight PTP — shows simplest tree | |
| Multi-robot sync | *(if available)* | Handling | SyncRobots events, handshake | |

**Per scenario, committed to `community/scenarios/<VENDOR>_<Tech>/`:**
```
<VENDOR>_<Tech>/
├── <Name>.cendoc              # E2 workcell (LFS)
├── reference/                 # Simple_Python_Translator .txt tree dumps
│   └── PG01_*.txt, PG02_*.txt...
├── golden/                    # Correct translator output files
│   └── PG01_*.ls, PG02_*.as...
└── README.md                  # What this scenario tests, how to run it
```

**Why this matters:**
- `.txt` tree dumps are the **single best docstring source** — they show exactly what `event.GetAttributes()` returns at runtime for every event type in that scenario
- Golden files enable **automated scoring** in Phase 6 validation — diff agent output vs. golden = pass/fail
- Each scenario doubles as a **workshop exercise** or onboarding task

---

### Phase 2 — E2 Source Investigation *(needs Azure DevOps access)*

**Single critical question:** Are the `.pyi` stubs auto-generated (from C++ headers / a script) or hand-written?

This determines the entire contribution architecture:

| Finding | Architecture |
|---------|-------------|
| Auto-generated | Contribute to the generation template — docstrings ship in every future release automatically |
| Auto-generated, template inaccessible | Maintain a `scripts/apply-docstring-patch.py` that re-applies after each E2 update |
| Hand-written | Direct PR to E2 source stubs |

This is a **decision gate** for Phase 5 only — Phases 3 and 4 proceed regardless (we write docstrings in our typings copy first).

---

### Phase 3 — Docstring Style Guide *(start now, parallel with Phase 1)*

Define the standard before writing a single docstring. Recommendation: **Google style** (Args / Returns / Raises) — renders perfectly in Pylance hover, supported by all doc generators, familiar to Python engineers.

Key conventions to codify:
- Always state units explicitly — never "a float", always "float, in **meters**"
- Every gotcha gets a `Note:` section (multi-signal containers, large index = unmapped, sort-before-use)
- Enum members each get a one-line doc + "observed when:" note
- Methods that must be paired get a cross-reference ("See also: `CloseOutputFile`")

**Deliverable:** `docs/standards/docstring-guide.md` — style guide + per-category templates (class, method, property, enum). E2 team approves this before Phase 4 starts.

---

### Phase 4 — Docstring Generation *(depends on Phase 1 corpus + Phase 3 style)*

**Process per class:** read stub → search corpus for all usages → read API markdown → generate docstring → human review → commit. Agent generates, human approves.

**Priority batches:**

**Batch 1** — Used in every downloader:
`DULPythonPosition`, `DULPythonMotion`, `DULPythonEvent`, `DULPythonDownloadOperator`

**Batch 2** — Common downloader + core:
`DULPythonController`, `DULPythonJoint`, `DULPythonProgram`, profiles, `EventType` enum, `OlpCorePythonResource`, `OlpCorePythonTechnology`

**Batch 3** — Upload domain:
`Uploader` base + all `cenpyupload` stubs

**Batch 4** — Utilities:
`cenpylib`: `FileUtility`, `attribute`, `arcreport`, `report`

**Acceptance per batch:** Agent generates a from-scratch translator for a known scenario and produces correct code — correct units, correct signal handling, correct file output — without extra prompting.

---

### Phase 5 — Contribution Back to E2 *(depends on Phase 2 + Phase 4)*

Ship the docstrings into the E2 product. Architecture chosen in Phase 2. Additionally: submit `docs/standards/docstring-guide.md` to the E2 team so new APIs ship documented from day one.

---

### Phase 6 — Quick-Ref and Validation *(depends on Phase 4)*

Auto-generate a quick-ref table from the docstrings (script: first docstring line per method → flat Markdown table ordered by lifecycle phase). Define 5 canonical validation tasks — one per domain (basic downloader, arc welding, uploader, technology script, report) — and score agent output using the scenarios from Phase 1C.

**Validation protocol:**
1. For each Phase 1C scenario: ask the agent to generate a translator from scratch given only the controller manual, the `.txt` tree dump, and a golden file as reference
2. Score: correct method names, correct units, correct signal handling, correct file output
3. Diff agent output vs. golden — automated pass/fail
4. Iterate on docstrings if score < threshold

---

### Phase 7 — Azure AI Search MCP *(depends on Phase 6)*

Wire `documentation.fastsuite.com`'s search index into VS Code as a Copilot tool via `@azure/mcp`. Now backed by high-quality docstrings, this becomes a genuinely powerful retrieval layer.

---

### Phase 8 — Technology Scripting Agent-First *(after Phase 6 validates translator quality)*

Full "agent writes technology scripts" capability — a separate domain from downloaders with different users (technology engineer vs. translator engineer) and different API surfaces.

**Scope:**
- Technology callback scripts: `PostTechInitAttributes`, `PostWmSyncPgAttributes`, event handlers
- Workmethod scripts: e.g., `ArcWeldingMethod.py`, `SeamFindingWorkMethod.py`
- Event scripts: `ArcOnEvent.py`, `TouchSensingEvent.py`, etc.

**Steps:**
1. Create `skills/technology/SKILL.md` — full technology scripting skill (callback lifecycle, API reference, attribute creation, event rule patterns)
2. Docstring Batch 5 — Technology-specific stubs: `CENPyOlpEventHandler`, `CENPyOlpAttribCreator`, `CENPyOlpEventOperator`, `CENPyOlpComputeHandler`, etc.
3. Inline technology skill into `Technologies/.instructions.md`
4. Validation: agent generates a new technology event script (e.g., a custom welding event) from spec — correct callback signatures, correct attribute creation, correct event rule setup

**Depends on:** Phase 1B technology corpus (already committed), Phase 4 Batch 2 `cenpyolpcore` docstrings (shared API surface), Phase 6 validation protocol established.

---

**Immediate next steps (can start today):**
1. **Phase 1A:** Audit the 25 vendor translator folders — classify CLEAN/SCRUB/SKIP
2. **Phase 1C:** Generate test scenarios (user doing this in E2 now)
3. **Phase 3:** Draft the docstring style guide for review
4. **Phase 2:** Request E2 source read access on Azure DevOps

---

## Consolidated Priority List (revised 2026-06-02)

Prioritized by **impact on agentic customization quality**, informed by the Kawasaki session.

### Tier 1 — Highest Impact (do next)

| # | Action | Impact | Location |
|---|--------|--------|----------|
| 1 | **More vendor scenarios** (FANUC, KUKA, ABB) | Each new scenario = training data + validation harness. The single most impactful thing for new downloaders. | `community/scenarios/` |
| 2 | **Technology stubs** — create `.pyi` for tech operator APIs | Unblocks agent-assisted technology scripting. Currently zero IDE support. | `typings/cenpyolpcore/stubs/` (new files) |
| 3 | **Expand `skills/technology/SKILL.md`** | Technology scripting has no patterns/lifecycle equivalent to downloader SKILL.md | `skills/technology/` |

### Tier 2 — High Impact (soon after)

| # | Action | Impact | Location |
|---|--------|--------|----------|
| 4 | **Vault patterns for technology** | Enable MCP-served tech knowledge | Vault `20_Patterns/Technology/` |
| 5 | **Uploader SKILL.md expansion** | Upload is thin — lifecycle + patterns needed | `skills/uploader/SKILL.md` |
| 6 | **MAPPING.md template** | Templatize the Kawasaki mapping for other vendors | `community/scenarios/README.md` or `skills/downloader/templates/` |

### Tier 3 — Medium Impact (when capacity allows)

| # | Action | Impact | Location |
|---|--------|--------|----------|
| 7 | **Docstring enrichment** in stubs | Better hover docs in IDE — nice but not blocking | `typings/` `.pyi` files |
| 8 | **Stub generator contribution** (C++ XML docs) | Ships docstrings in every E2 release | E2 source (Azure DevOps) |
| 9 | **Remove redundant vault API class docs** | Reduces maintenance, avoids drift | Vault `10_API_Reference/Download/*.md` |
| 10 | **Remote MCP serving** | Only needed for external users | Vault §17 |

### Tier 4 — Low Priority (deferred)

| # | Action | Reason to defer |
|---|--------|----------------|
| 11 | Azure AI Search MCP | Local vault sufficient; no external users yet |
| 12 | Docstring batches 3–4 (cenpylib, cenpyunits) | Utility packages rarely cause agent errors |
| 13 | Scheduled agent workflows | Need stable vault content first |

### What NOT to do (learned from session)

- **Don't maintain per-class API docs in the vault** that duplicate `.pyi` stubs. They drift and the agent doesn't use them.
- **Don't invest in docstrings before scenarios** — scenarios (golden + reference) provide more value per hour than docstring writing.
- **Don't build remote serving** until there's an external user requesting it.
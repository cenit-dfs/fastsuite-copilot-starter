---
title: "Plan: API Availability for Coding Agents"
version: 2.0
date_created: 2026-05-18
last_updated: 2026-06-02
status: "Milestone 1 complete — Milestone 2 revised — see below"
tags: [copilot, stubs, pylance, api, mcp]
---

# Plan: API Availability for Coding Agents

**Goal:** Make the full FASTSUITE E2 Python API available to the coding agent so it generates correct method calls, understands types, and can find the right API for any task.

---

## Milestone 1 — Commit stubs to the repo ✅

**Status:** Complete (2026-05-18)

The E2 API packages ship `.pyi` stub files. All six packages committed to `typings/` and wired into Pylance/pyright. See below for details.

### Package inventory

| Package | Type | Contents |
|---------|------|---------|
| `cenpydownload` | `.py` + `.pyi` stubs | Download API: `Downloader`, `DULPython*`, `EventType`, enums |
| `cenpyolpcore` | `.py` + `.pyi` stubs | OLP core: `OlpCorePython*`, `EventType`, `ControllerTypes` |
| `cenpylib` | Full `.py` + stubs | Utilities: `FileUtility`, `attribute`, `report`, `arcreport` |
| `cenpyunits` | Full `.py` + stubs | Unit conversion helpers |
| `cenpymath` | `.py` + `.pyi` stubs | Euler conversion, geometry math |
| `cenpyupload` | `.py` + `.pyi` stubs | Upload API: `Uploader`, `ULPython*` |

### Update plan for future E2 releases
```powershell
$src = "c:\Programs\FASTSUITE_Edition_2_<VERSION>\Lib\site-packages"
$dst = "typings"
foreach ($pkg in @("cenpydownload","cenpyolpcore","cenpylib","cenpyunits","cenpymath","cenpyupload")) {
   robocopy "$src\$pkg" "$dst\$pkg" /E /MIR /XD __pycache__ images languages /XF *.pyc *.png *.jpg *.ico *.ttf *.lng
}
```

---

## Milestone 2 — Behavioral Knowledge via Obsidian MCP ✅ (revised scope)

**Status:** Partially complete (2026-06-02)

**Key learning (2026-06-02 Kawasaki session):** The agent used typings ~95% and MCP vault ~5%. The vault's per-class API docs (method signatures) are redundant with `.pyi` stubs and won't be maintained further.

### What the vault IS good for (keep + invest):

| Vault Content | Value | Stubs Equivalent |
|---------------|-------|------------------|
| Lifecycle callback order | Explains WHEN/WHY | None |
| Patterns (`20_Patterns/Downloader/`) | Behavioral knowledge | None |
| Technology operator APIs | Only source (no stubs) | **Gap** |
| Gotchas (BoolAttribute, units) | Not expressible in types | None |

### What's redundant (stop maintaining):

- `10_API_Reference/Download/DULPython*.md` class method docs → stubs cover this
- `10_API_Reference/Upload/ULPython*.md` class method docs → stubs cover this
- `10_API_Reference/OlpCore/OlpCorePython*.md` class method docs → stubs cover this

### What's needed (gap to fill):

- `10_API_Reference/Technology/` operator APIs — **no stubs exist** for `AttribCreator`, `EventOperator`, etc.
- Technology stubs in `typings/` — would enable IDE support for tech scripts
- Enhanced stub docstrings (Phase 5 of agent-first-capability plan) — via C++ XML docs

---

## Milestone 3 — Remote Serving ⤳ DEFERRED

**Status:** Deferred to post-demo. Options documented in vault Implementation Plan §17.

Decision: Local MCP (Obsidian on `127.0.0.1:27200`) is sufficient for internal use. Remote serving (pgvector or Azure AI Search) only needed when external customers/partners need access without running Obsidian.

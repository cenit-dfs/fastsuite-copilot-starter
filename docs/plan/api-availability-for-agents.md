---
title: "Plan: API Availability for Coding Agents"
version: 1.0
date_created: 2026-05-18
last_updated: 2026-05-18
status: "In progress"
tags: [copilot, stubs, pylance, api, mcp]
---

# Plan: API Availability for Coding Agents

**Goal:** Make the full FASTSUITE E2 Python API available to the coding agent so it generates correct method calls, understands types, and can find the right API for any task.

---

## Milestone 1 — Commit stubs to the repo ✅

**Goal:** Fix "agent writes wrong method names/args."
**Status:** ![Complete](https://img.shields.io/badge/status-Complete-brightgreen)

The E2 API packages ship `.pyi` stub files inside each package's `stubs/` subfolder. All six packages are now committed to `typings/` and wired into Pylance and pyright.

### What was done

| Task | Status | Date |
|------|--------|------|
| Copy `cenpydownload` stubs + `.py` files to `typings/` | ✅ | 2026-05-18 |
| Copy `cenpyolpcore` stubs to `typings/` | ✅ | 2026-05-18 |
| Copy `cenpylib` full `.py` + stubs to `typings/` | ✅ | 2026-05-18 |
| Copy `cenpyunits` full `.py` + stubs to `typings/` | ✅ | 2026-05-18 |
| Copy `cenpymath` stubs to `typings/` | ✅ | 2026-05-18 |
| Copy `cenpyupload` stubs to `typings/` | ✅ | 2026-05-18 |
| Add `typings/` first in `python.analysis.extraPaths` | ✅ | 2026-05-18 |
| Add `typings/` first in `python.autoComplete.extraPaths` | ✅ | 2026-05-18 |
| Create `pyrightconfig.json` with `extraPaths: ["typings"]` | ✅ | 2026-05-18 |
| Set `reportMissingTypeStubs: warning` (stubs now exist) | ✅ | 2026-05-18 |

### Package inventory

| Package | Type | Contents |
|---------|------|---------|
| `cenpydownload` | `.py` + `.pyi` stubs | Download API: `Downloader`, `DULPythonMotion`, `DULPythonPosition`, `EventType`, enums… |
| `cenpyolpcore` | `.py` + `.pyi` stubs | OLP core: `OlpCorePythonController`, `OlpCorePythonResource`, `EventType`, `ControllerTypes`… |
| `cenpylib` | Full `.py` + stubs | Utilities: `FileUtility`, `attribute`, `report`, `arcreport`, `network`, `ui`… |
| `cenpyunits` | Full `.py` + stubs | Unit conversion helpers |
| `cenpymath` | `.py` + `.pyi` stubs | Math helpers |
| `cenpyupload` | `.py` + `.pyi` stubs | Upload API |

### Result
- Hover types, autocomplete, and go-to-definition work for all E2 API classes
- Works on any machine — no local E2 installation required
- 230 `.py` + 174 `.pyi` files in `typings/`

### Update plan for future E2 releases
When a new E2 version ships, re-run the copy:
```powershell
$src = "c:\Programs\FASTSUITE_Edition_2_<VERSION>\Lib\site-packages"
$dst = "typings"
foreach ($pkg in @("cenpydownload","cenpyolpcore","cenpylib","cenpyunits","cenpymath","cenpyupload")) {
   robocopy "$src\$pkg" "$dst\$pkg" /E /MIR /XD __pycache__ images languages /XF *.pyc *.png *.jpg *.ico *.ttf *.lng
}
```

---

## Milestone 2 — Richer agent-readable API docs

**Goal:** Fix "agent doesn't know WHICH API to use for a given task."
**Status:** ![Planned](https://img.shields.io/badge/status-Planned-blue)

| Task | Description | Status |
|------|-------------|--------|
| TASK-M2-01 | Add `typings/README.md` — one-liner per package | |
| TASK-M2-02 | Create `docs/API_Python/quick-ref.md` — single flat file, all key signatures ordered by lifecycle phase | |
| TASK-M2-03 | Review `E2_API_Download.md` — add cross-references to golden files and tree dumps | |

**Acceptance:** Opening `quick-ref.md` gives the agent a complete method/signature reference in one retrieval.

---

## Milestone 3 — Azure AI Search MCP server

**Goal:** Fix "agent can't find the right API at generation time."
**Status:** ![Planned](https://img.shields.io/badge/status-Planned-blue)

Expose `documentation.fastsuite.com`'s Azure AI Search index as a queryable VS Code Copilot tool using the `@azure/mcp` MCP server.

| Task | Description | Status |
|------|-------------|--------|
| TASK-M3-01 | Find Azure AI Search resource name + index name | |
| TASK-M3-02 | Create read-only query key | |
| TASK-M3-03 | Configure `.vscode/mcp.json` with `@azure/mcp` pointing to the search endpoint | |
| TASK-M3-04 | Test: Copilot can call the search tool to answer "which method do I use to get external axes?" | |

**Decisions pending:**
- Azure AI Search endpoint URL and index name
- Whether to use `@azure/mcp` directly or create a thin proxy (for key management)

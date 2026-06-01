# Copilot Instructions (FASTSUITE E2 Customization)

## Goals
- Keep changes small, reviewable, and well-documented.
- Preserve existing behavior unless a change is explicitly requested.
- Prefer architecture that is easy for project engineers to customize.

## Repository Structure
- **Your code**: `OLPTranslators/<VENDOR>/` and `Technologies/<VENDOR>/`
- **Community examples**: `community/` (git submodule — read-only reference)
- **Skills**: `skills/`
- **Agent modes**: `AGENTS.md`
- **API docs**: Obsidian vault via `obsidian-e2` MCP server (see `.vscode/mcp.json`)

## Repository Hygiene
- Do not introduce new third-party dependencies unless necessary.
- Keep vendor-specific logic under the vendor folder (e.g., `OLPTranslators/MyVendor`).
- Put specs and change notes in vendor docs:
  - Spec: `docs/<VENDOR>/spec/*.md`
  - Change log / working notes: `docs/<VENDOR>/current.md`

## API Documentation Context
Use the `obsidian-e2` MCP server to look up E2 Python API docs. Search the vault for the relevant classes and callbacks.

### Downloader Work (`OLPTranslators\*\*.py`)
- **Primary context:** vault folder `10_API_Reference/Download/` (Download Callback Lifecycle, DULPython* classes)
- **Core objects:** vault folder `10_API_Reference/OlpCore/` (OlpCorePython* classes, Attributes, Enumerations)
- Use when working on: vendor-specific download scripts
- **DO NOT MODIFY:** downloadStarter.py, downloader.py (E2 installation files)

### Uploader Work (`OLPTranslators\*\*.py`)
- **Primary context:** vault folder `10_API_Reference/Upload/` (Upload Callback Lifecycle, ULPython* classes)
- **Core objects:** vault folder `10_API_Reference/OlpCore/`
- Use when working on: vendor-specific upload scripts
- **DO NOT MODIFY:** uploadStarter.py, uploader.py (E2 installation files)

### Technology Work (`Technologies\*\...\Scripts\*.py`)
- **Primary context:** vault folder `10_API_Reference/Technology/` (Technology Callback Lifecycle, Workmethod Callback Lifecycle)
- **Core objects:** vault folder `10_API_Reference/OlpCore/`
- Use when working on: callback scripts (PostTechInitAttributes, PostWmSyncPgAttributes, etc.), event scripts, workmethod scripts

### Report Generation
- **Primary context:** vault note `10_API_Reference/Reporting/ReportUtility`
- Use when working on: PDF report generation, ReportUtility customization

## Documentation Rules
- If you change downloader behavior or output format, update:
  - `docs/<VENDOR>/current.md`
  - and the relevant spec under `docs/<VENDOR>/spec/`.
- Avoid large "wall of text" docs; keep specs actionable and scoped.

## Coding Rules
- Separate orchestration from syntax emission:
  - Baseline downloader handles E2 lifecycle/traversal, generic motion, file structure.
  - Technology plugins handle tech events and tech-specific syntax.
- Keep the customization surface small:
  - Prefer simple mapping tables / helper functions over deep inheritance.
  - Avoid changing traversal logic to support customer-specific syntax.
- Do not add debugging prints; use E2 logger when needed.

## Testing / Determinism
- Generated output should be deterministic for tests:
  - Avoid embedding timestamps/usernames unless guarded by a test flag.
- Prefer golden-file comparisons for translators.

## Safety
- **Do not modify files outside this repository** (e.g., E2 installation files).
- **Do not modify E2 core files:** downloadStarter.py, downloader.py, uploadStarter.py, uploader.py are in the E2 installation side-package folder.
- **Do not modify E2 site-packages** under the FASTSUITE installation `Lib/site-packages/` (cenpydownload, cenpyolpcore, cenpylib, cenpyupload, etc.).
- Do not install new Python packages unless explicitly approved.
- Do not modify files outside the translator/technology scope unless requested.
- Do not commit or push unless explicitly asked.

## Skills & Agent Modes
- **Downloader skill**: `skills/downloader/SKILL.md` — comprehensive guide for creating/modifying OLP downloaders (lifecycle, API reference, event handling, position output, common mistakes). Use when working on any `OLPTranslators/**/*.py` file.
- **Base template**: `skills/downloader/templates/base_downloader.py` — minimal working starter downloader with all callbacks stubbed.
- **Technology skill**: `skills/technology/SKILL.md` — guide for technology UI customization (planned).
- **Agent modes**: `AGENTS.md` — defines E2Downloader, E2Technology, E2Uploader modes with scoped instructions.
- **OLP translator rules**: `OLPTranslators/.instructions.md` — scoped coding rules applied automatically when editing translator files.

## Reference Code (Community Submodule)
- `community/OLPTranslators/KUKA/KUKA_KRC5.py` — canonical base downloader pattern
- `community/OLPTranslators/ABB/ABB_IRC5.py` — advanced multi-plugin reference
- `community/OLPTranslators/Simple_Python_Translator.py` — OLP tree dumper for analysis

## Environment
- Python 3.12 (bundled with FASTSUITE E2) — interpreter path configured in `.vscode/settings.json`.
- E2 API packages: `cenpydownload`, `cenpyolpcore`, `cenpylib`, `cenpyupload`, `cenpymath`, `cenpyunits` — read-only, in installation `Lib/site-packages/`.
- E2 bootstrap modules: `centypes.py`, `cenpyDef*.py`, `defDownload.py`, `defUpload.py` — at installation root, read-only.
- Workspace is single-root at the repo root. All paths are relative to that root.

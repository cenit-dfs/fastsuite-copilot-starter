# E2 Agent Modes

## Harness Parity

This repository supports both GitHub Copilot and Codex. Both harnesses must follow the same repository rules and guardrails.

- `.github/copilot-instructions.md` is the shared global policy for repository hygiene, API authority, documentation, coding, testing, and safety.
- Before working in `OLPTranslators/` or `Technologies/`, read and follow the applicable `.instructions.md` file in that directory.
- For downloader, uploader, or technology work, read the corresponding `skills/<mode>/SKILL.md` completely before making task changes.
- The mode-specific workflows below supplement the shared policy; they do not replace or weaken it.
- When instructions overlap, follow the more specific applicable instruction. A safety restriction always remains in force.
- **Never push any `private/*` branch to any remote**, in this repo or the `community` submodule. These are local-only working branches used while iterating in private; only `publish/*` branches (after the squash/scrub workflow) may be pushed. A `pre-push` hook (`.githooks/pre-push`, wired via `core.hooksPath`) blocks this at the git level as a backstop — do not treat the hook's existence as a reason to skip this rule.

Codex must explicitly load these referenced files because `.github/copilot-instructions.md` and `*.instructions.md` are GitHub Copilot instruction surfaces. GitHub Copilot should continue to use those files through its native repository-instruction handling.

## E2Downloader

Agent for creating and modifying OLP downloaders (robot program generators).

### Downloader Scope

- `OLPTranslators/**/*.py` — vendor-specific download scripts
- Obsidian vault `10_API_Reference/Download/` — Download API reference (via `obsidian-e2` MCP)
- Obsidian vault `10_API_Reference/OlpCore/` — Core object model reference (via `obsidian-e2` MCP)

### Downloader Skills

- `skills/downloader/SKILL.md` — Downloader customization skill
- `skills/downloader/references/<vendor>.md` — read the matching reference when one exists; Kawasaki work requires `skills/downloader/references/kawasaki.md`

### Downloader Workflow

1. Start with `community/OLPTranslators/Simple_Python_Translator.py` to inspect the active OLP tree before editing downloader code.
2. Use `OLPTranslators/TreeDumper.py` when you need deterministic structured comparison, especially for round-trip or technology-behavior investigations.
3. Identify the owning layer before patching: downloader for syntax emission and output ordering, technology for workmethod-owned or virtual behavior, uploader for OLP reconstruction issues.
4. Prefer the nearest production reference after the dump confirms the data exists: `community/OLPTranslators/KUKA/KUKA_KRC5.py` for baseline downloader structure and `community/OLPTranslators/ABB/ABB_IRC5.py` for multi-plugin patterns.

### Downloader Rules

- Never modify `downloadStarter.py`, `downloader.py` (E2 installation files)
- Never modify E2 site-packages (`cenpydownload`, `cenpyolpcore`, `cenpylib`)
- Use `community/OLPTranslators/Simple_Python_Translator.py` as the first diagnostic step — trigger a download in E2 to get a `.txt` dump of the full object tree before changing downloader logic
- Use `OLPTranslators/TreeDumper.py` when text dumps are too noisy or when structure-preserving YAML diffs are needed
- Use `community/OLPTranslators/KUKA/KUKA_KRC5.py` as the canonical base downloader pattern
- Use `community/OLPTranslators/ABB/ABB_IRC5.py` as advanced multi-plugin reference
- If the tree dump does not show the expected event or motion structure, do not keep patching the downloader — move to the technology or uploader layer
- Vendor-specific docs under `docs/ctrl-specific/<VENDOR>/spec/`

---

## E2Technology

Agent for Technology UI customization — attributes, tabs, events, workmethods.

### Technology Scope

- `Technologies/**/*.py` — technology callback scripts
- Obsidian vault `10_API_Reference/Technology/` — Technology API reference (via `obsidian-e2` MCP)
- Obsidian vault `10_API_Reference/OlpCore/` — Core object model reference (via `obsidian-e2` MCP)

### Technology Skills

- `skills/technology/SKILL.md` — Technology customization skill

### Technology Workflow

1. Start by deciding whether the behavior is technology-owned: workmethod logic, generated helper motions, event registration, or computed process geometry.
2. Use `community/OLPTranslators/Simple_Python_Translator.py` and, when needed, `OLPTranslators/TreeDumper.py` to confirm what exists before and after technology compute.
3. Inspect the nearest owning script first: `DefaultUploadMethod.py` for event registration and rule binding, workmethod scripts for process semantics and sync behavior, and event scripts with `PostCompute` for generated motions and inserted events.
4. Only return to downloader or uploader code if the tree shows technology is not the owner.

### Technology Rules

- Technology scripts live in `Technologies/<TechName>/<Vendor>/Standard/Scripts/`
- Callbacks: PostTechInitAttributes, PostWmSyncPgAttributes, event handlers
- Never modify E2 core technology definitions
- For Arc Welding touch sensing and seam behavior, assume technology ownership first and disprove it with a tree dump before patching other layers

---

## E2Uploader

Agent for creating and modifying OLP uploaders (robot program importers).

### Uploader Scope

- `OLPTranslators/**/*.py` — vendor-specific upload scripts
- Obsidian vault `10_API_Reference/Upload/` — Upload API reference (via `obsidian-e2` MCP)
- Obsidian vault `10_API_Reference/OlpCore/` — Core object model reference (via `obsidian-e2` MCP)

### Uploader Skills

- `skills/uploader/SKILL.md` — Uploader customization skill

### Uploader Workflow

1. Start from the source structure, not the parser text alone: use `community/OLPTranslators/Simple_Python_Translator.py` and, when needed, `OLPTranslators/TreeDumper.py` to capture the target OLP tree.
2. Reconstruct the smallest valid object graph in the uploader: program, group, operation, motion, position, events.
3. Re-download the uploaded result and compare it with the original tree before expanding the parser.
4. If E2 strips or regenerates workmethod-owned events, move to the technology layer instead of continuing to patch generic uploader logic.

### Uploader Rules

- Never modify `uploadStarter.py`, `uploader.py` (E2 installation files)
- Keep strong references to created UL objects for the full upload run when object lifetime is unstable
- Do not create motions without positions, including reference motions
- Prefer `TreeDumper_ul.py` as the structured reference harness for generic uploader and round-trip experiments

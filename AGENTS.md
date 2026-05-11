# E2 Agent Modes

## E2Downloader

Agent for creating and modifying OLP downloaders (robot program generators).

### Scope
- `OLPTranslators/**/*.py` — vendor-specific download scripts
- `docs/API_Python/E2_API_Download.md` — Download API reference
- `docs/API_Python/E2_API_OlpCore.md` — Core object model reference

### Skills
- `skills/downloader/SKILL.md` — Downloader customization skill

### Key Rules
- Never modify `downloadStarter.py`, `downloader.py` (E2 installation files)
- Never modify E2 site-packages (`cenpydownload`, `cenpyolpcore`, `cenpylib`)
- Use `community/OLPTranslators/Simple_Python_Translator.py` as OLP tree reference — trigger a download in E2 to get a `.txt` dump of the full object tree for analysis
- Use `community/OLPTranslators/KUKA/KUKA_KRC5.py` as the canonical base downloader pattern
- Use `community/OLPTranslators/ABB/ABB_IRC5.py` as advanced multi-plugin reference
- Vendor-specific docs under `docs/<VENDOR>/spec/`

---

## E2Technology

Agent for Technology UI customization — attributes, tabs, events, workmethods.

### Scope
- `Technologies/**/*.py` — technology callback scripts
- `docs/API_Python/E2_API_Offline_Programming.md` — Technology API reference
- `docs/API_Python/E2_API_OlpCore.md` — Core object model reference

### Skills
- `skills/technology/SKILL.md` — Technology customization skill

### Key Rules
- Technology scripts live in `Technologies/<TechName>/<Vendor>/Standard/Scripts/`
- Callbacks: PostTechInitAttributes, PostWmSyncPgAttributes, event handlers
- Never modify E2 core technology definitions

---

## E2Uploader

Agent for creating and modifying OLP uploaders (robot program importers).

### Scope
- `OLPTranslators/**/*.py` — vendor-specific upload scripts
- `docs/API_Python/E2_API_Upload.md` — Upload API reference
- `docs/API_Python/E2_API_OlpCore.md` — Core object model reference

### Skills
- `skills/uploader/SKILL.md` — Uploader customization skill (planned)

### Key Rules
- Never modify `uploadStarter.py`, `uploader.py` (E2 installation files)

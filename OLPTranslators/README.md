# OLP Translators

Place your vendor-specific downloaders and uploaders here.

## Structure

```
OLPTranslators/
├── <VENDOR>/
│   ├── <VENDOR>_<CONTROLLER>.py      # Downloader
│   ├── <VENDOR>_<CONTROLLER>_ul.py   # Uploader (optional)
│   ├── <VENDOR>_<CONTROLLER>.xml     # E2 translator registration
│   └── tests/
│       ├── scenarios/                 # E2 scenario files (.cendoc) — see below
│       │   └── basic_motion.cendoc
│       ├── golden/                    # Expected output (committed to Git)
│       │   ├── basic_motion.src
│       │   └── basic_motion.dat
│       └── output/                    # Actual download results (.gitignore'd)
│           ├── basic_motion.src
│           └── basic_motion.dat
└── .instructions.md                   # Auto-applied coding rules
```

## Getting Started

1. Copy `skills/downloader/templates/base_downloader.py` to `OLPTranslators/<VENDOR>/`
2. Rename the class and `DOWNLOAD_CLASS_NAME` to match your vendor
3. Reference `community/OLPTranslators/KUKA/KUKA_KRC5.py` for a working example
4. Use `community/OLPTranslators/Simple_Python_Translator.py` to dump the OLP tree for analysis

## Testing with Golden Files

Golden-file comparison is the primary way to verify downloaders produce correct output.

### Setup

1. Create `tests/scenarios/` — place your `.cendoc` E2 scenario file(s) here
2. Create `tests/golden/` — place the known-good output files here (committed to Git)
3. Create `tests/output/` — this is where E2 writes actual download results (ignored by Git)

### Workflow

1. Open the `.cendoc` scenario in E2
2. Run the download — configure E2 to write output into `tests/output/`
3. Compare output against golden:
   - **VS Code task:** `Ctrl+Shift+P` → "Tasks: Run Task" → "Compare Output vs Golden"
   - **Manual:** Right-click a file → "Select for Compare", then right-click the golden → "Compare with Selected"
4. If the output is correct and intentionally different from golden, overwrite the golden files and commit

### About `.cendoc` Files

`.cendoc` files are **binary ZIP archives** containing a complete E2 project (resources, layout, OLP programs). They are:
- **Not text-readable** — Copilot and other agents cannot read or analyze them
- **Large** — even minimal scenarios are typically 10 MB or more
- **Tracked via Git LFS** — the `.gitattributes` file is pre-configured to handle them; run `git lfs install` once before committing `.cendoc` files
- **Essential for reproducible testing** — they define the exact scenario your downloader will process

> **Git LFS prerequisite:** Install [Git LFS](https://git-lfs.com/) and run `git lfs install` once before your first commit containing `.cendoc` files. GitHub Free includes 1 GB LFS storage; check your plan if you store many scenarios.

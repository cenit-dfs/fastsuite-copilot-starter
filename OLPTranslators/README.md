# OLP Translators

Place your vendor-specific downloaders and uploaders here.

## Structure

```
OLPTranslators/
├── <VENDOR>/
│   ├── <VENDOR>_<CONTROLLER>.py      # Downloader
│   ├── <VENDOR>_<CONTROLLER>_ul.py   # Uploader (optional)
│   └── <VENDOR>_<CONTROLLER>.xml     # E2 translator registration
└── .instructions.md                   # Auto-applied coding rules
```

## Getting Started

1. Copy `skills/downloader/templates/base_downloader.py` to `OLPTranslators/<VENDOR>/`
2. Rename the class and `DOWNLOAD_CLASS_NAME` to match your vendor
3. Reference `community/OLPTranslators/KUKA/KUKA_KRC5.py` for a working example
4. Use `community/OLPTranslators/Simple_Python_Translator.py` to dump the OLP tree for analysis

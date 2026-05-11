---
description: Guide for creating and modifying FASTSUITE E2 OLP uploaders (robot program importers). Use when working on uploader files under OLPTranslators/.
applyTo: OLPTranslators/**/*ul*.py
---

# E2 OLP Uploader Skill

## What is an Uploader?

An uploader imports vendor-specific robot programs back into the FASTSUITE E2 OLP environment. It parses robot code files and creates the corresponding E2 program structure (operations, motions, events, positions).

## API Reference

- **Primary context**: `docs/API_Python/E2_API_Upload.md`
- **Core objects**: `docs/API_Python/E2_API_OlpCore.md`

## Key Rules
- Never modify `uploadStarter.py`, `uploader.py` (E2 installation files)
- Never modify E2 site-packages (`cenpydownload`, `cenpyolpcore`, `cenpylib`, `cenpyupload`)
- Logger is always a local variable: `logger = operator.GetLogOperator()`

*This skill will be expanded with lifecycle documentation, patterns, and examples. See `docs/API_Python/E2_API_Upload.md` for the full API reference.*

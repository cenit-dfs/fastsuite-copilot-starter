---
description: Guide for creating and modifying FASTSUITE E2 OLP uploaders (robot program importers). Use when working on uploader files under OLPTranslators/.
applyTo: OLPTranslators/**/*ul*.py
---

# E2 OLP Uploader Skill

## What is an Uploader?

An uploader imports vendor-specific robot programs back into the FASTSUITE E2 OLP environment. It parses robot code files and creates the corresponding E2 program structure (operations, motions, events, positions).

## API Reference

- **Primary context**: Obsidian vault `10_API_Reference/Upload/` (via `obsidian-e2` MCP)
- **Core objects**: Obsidian vault `10_API_Reference/OlpCore/` (via `obsidian-e2` MCP)

## Key Rules
- Never modify `uploadStarter.py`, `uploader.py` (E2 installation files)
- Never modify E2 site-packages (`cenpydownload`, `cenpyolpcore`, `cenpylib`, `cenpyupload`)
- Logger is always a local variable: `logger = operator.GetLogOperator()`

*This skill will be expanded with lifecycle documentation, patterns, and examples. Use the `obsidian-e2` MCP server to look up `Upload Callback Lifecycle` for the full API reference.*

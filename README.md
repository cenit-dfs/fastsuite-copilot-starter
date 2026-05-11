# FASTSUITE E2 — Copilot Starter

Agent-first development environment for FASTSUITE E2 OLP customization. This template provides VS Code Copilot skills, agent modes, coding rules, and API documentation so Copilot understands the E2 ecosystem and can help you build downloaders, uploaders, and technology plugins.

## Prerequisites

- **FASTSUITE E2 R2026.1** (or later) installed
- **VS Code** with [GitHub Copilot](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot) extension
- **Python 3.12** (bundled with E2 — no separate install needed)
- **Git** for submodule support

## Quick Start

### 1. Create Your Repository

Click **"Use this template"** on GitHub to create your own repository from this starter.

### 2. Clone and Initialize

```bash
git clone https://github.com/<your-org>/<your-repo>.git
cd <your-repo>
git submodule update --init
```

The `community/` folder will be populated with reference downloaders and examples.

### 3. Configure E2 Path

Edit `.vscode/settings.json` and update the E2 installation path:
```json
"python.defaultInterpreterPath": "c:\\Programs\\FASTSUITE_Edition_2_R2026.1\\python.exe"
```
Update all `TODO` comments in that file to match your installation.

### 4. Open in VS Code

```bash
code .
```

VS Code will recommend installing Python and Copilot extensions. Accept all recommendations.

### 5. Start Building

Ask Copilot to create a downloader:
> *"Create a new FANUC downloader based on the base template"*

Or switch to the **E2Downloader** agent mode for focused downloader work.

## Repository Structure

```
├── .github/copilot-instructions.md   # Global Copilot context
├── .vscode/                           # VS Code settings, launch config
├── AGENTS.md                          # Agent modes (E2Downloader, E2Technology, E2Uploader)
├── skills/
│   ├── downloader/
│   │   ├── SKILL.md                   # Comprehensive downloader guide
│   │   └── templates/
│   │       └── base_downloader.py     # Minimal starter template
│   ├── technology/
│   │   └── SKILL.md                   # Technology customization guide
│   └── uploader/
│       └── SKILL.md                   # Uploader guide (planned)
├── docs/API_Python/                   # E2 Python API documentation
├── OLPTranslators/                    # YOUR vendor-specific downloaders/uploaders
│   └── .instructions.md              # Auto-applied coding rules
├── Technologies/                      # YOUR technology plugins
│   └── .instructions.md              # Auto-applied coding rules
└── community/                         # Git submodule — reference code (read-only)
    ├── OLPTranslators/
    │   ├── KUKA/KUKA_KRC5.py          # Canonical base downloader
    │   ├── ABB/ABB_IRC5.py            # Advanced multi-plugin reference
    │   └── Simple_Python_Translator.py # OLP tree dumper
    └── examples/                      # Tree dumps, golden files
```

## How It Works

### Copilot Skills
When you edit a file under `OLPTranslators/`, Copilot automatically loads:
- The **downloader skill** (`skills/downloader/SKILL.md`) — lifecycle, API reference, event handling, common mistakes
- The **OLP translator rules** (`OLPTranslators/.instructions.md`) — coding conventions, safety rules

### Agent Modes
Switch between focused modes in VS Code Copilot Chat:
- **E2Downloader** — for creating/modifying downloaders
- **E2Technology** — for technology UI customization
- **E2Uploader** — for creating/modifying uploaders

### Reference Code
The `community/` submodule contains working reference downloaders. Copilot uses these as context when helping you build new ones. To update:

```bash
git submodule update --remote
```

## Workflow

1. **Analyze**: Use `Simple_Python_Translator.py` in E2 to dump the OLP tree as `.txt`
2. **Build**: Create your downloader in `OLPTranslators/<VENDOR>/`
3. **Test**: Download in E2, compare output with golden files
4. **Debug**: Attach VS Code debugger (port 5254) to E2

## Adding Your Own Vendor Docs

```
docs/<VENDOR>/
├── spec/           # Specifications
│   └── *.md
└── current.md      # Change log / working notes
```

## Contributing to Community

To contribute downloaders, examples, or fixes back to the community:

1. **Fork** the [fastsuite-e2-community](https://github.com/cenit-dfs/fastsuite-e2-community) repository
2. Add or modify files in your fork
3. Open a Pull Request

To contribute skills or docs back to the starter template:

1. **Fork** this repository
2. Make your changes
3. Open a Pull Request

## License

See [LICENSE](LICENSE) for details.

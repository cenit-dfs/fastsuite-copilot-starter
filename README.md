# FASTSUITE E2 — AI Agent Starter

Agent-first development environment for FASTSUITE E2 OLP customization. This template supports both **GitHub Copilot** and **OpenAI Codex**, so each developer can choose their preferred harness while using the same E2 workflows, coding rules, safety guardrails, and API references.

## Prerequisites

- **FASTSUITE E2 R2026.1** (or later) installed
- An agent harness:
  - **GitHub Copilot** in VS Code, or
  - **[OpenAI Codex](https://developers.openai.com/codex/)** in its CLI, IDE extension, or app
- **Python 3.12** (bundled with E2 — no separate install needed)
- **Git** for submodule support
- The subscription or account required by your chosen harness

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

Enable the repo's safety pre-push hook, which blocks accidentally pushing `private/*` branches (see [Git Essentials](docs/workshop/git-essentials.md#private-branch-push-guardrail)):

```bash
git config core.hooksPath .githooks
cd community
git config core.hooksPath "$(cd .. && pwd)/.githooks"
cd ..
```

### 3. Configure E2 Path

Edit `.vscode/settings.json` and update the E2 installation path:
```json
"python.defaultInterpreterPath": "c:\\Programs\\FASTSUITE_Edition_2_R2026.1\\python.exe"
```
Update all `TODO` comments in that file to match your installation.

### 4. Open the Repository in Your Agent Harness

For GitHub Copilot in VS Code:

```bash
code .
```

VS Code will recommend the configured Python and Copilot extensions. Accept the recommendations you need.

For Codex, open the repository in the Codex IDE extension or app, or start the CLI from the repository root:

```bash
codex
```

Always start the harness at the repository root so it discovers the repository instructions and relative references correctly.

### 5. Start Building

Ask your chosen agent to create a downloader:
> *"Create a new FANUC downloader based on the base template"*

For focused work, name the appropriate role in your request: **E2Downloader**, **E2Technology**, or **E2Uploader**.

## Repository Structure

```
├── .github/copilot-instructions.md   # Shared global policy; native Copilot instructions
├── .vscode/                           # VS Code settings, launch config
├── AGENTS.md                          # Codex entry point and shared E2 agent modes
├── skills/
│   ├── downloader/
│   │   ├── SKILL.md                   # Comprehensive downloader guide
│   │   ├── references/                # Vendor-specific agent decision tables
│   │   └── templates/
│   │       └── base_downloader.py     # Minimal starter template
│   ├── technology/
│   │   ├── SKILL.md                   # Technology customization workflow
│   │   └── references/                # Focused agent decision tables
│   └── uploader/
│       └── SKILL.md                   # Uploader guide
├── docs/
│   ├── technology/                    # E2 Technology guides and validation
│   └── ctrl-specific/                 # Vendor/controller documentation
├── examples/technology/               # Curated R2026.1 teaching overlays
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

## Choose Your Harness

The harness changes how instructions are discovered, not the engineering rules that apply.

| Concern | GitHub Copilot | Codex |
|---|---|---|
| Repository-wide policy | Loads `.github/copilot-instructions.md` | Loads `AGENTS.md`, which requires the same global policy |
| Path-specific rules | Loads `OLPTranslators/.instructions.md` or `Technologies/.instructions.md` | `AGENTS.md` requires the applicable scoped file to be read |
| Task workflow | Uses the relevant file under `skills/` | `AGENTS.md` requires the relevant skill to be read completely |
| E2 role | Use the matching Copilot agent/mode or state it in the prompt | State `E2Downloader`, `E2Technology`, or `E2Uploader` in the prompt |

This arrangement avoids maintaining two independent sets of E2 rules. The detailed shared policy remains in `.github/copilot-instructions.md`; `AGENTS.md` supplies Codex discovery and the role-specific workflow. When instructions overlap, the more specific applicable rule wins and safety restrictions remain in force.

## Shared Rules and Guardrails

Both harnesses must:

- Treat `typings/` as authoritative for available Python API names and signatures.
- Use the `obsidian-e2` MCP documentation for lifecycle behavior, callback semantics, patterns, and APIs not yet represented in `typings/`.
- Use runtime behavior and OLP tree dumps to resolve remaining uncertainty.
- Keep `community/` read-only and use it as reference code.
- Never modify E2 installation files or E2 site-packages.
- Never install Python packages, commit, or push unless explicitly approved or requested.
- Keep changes small, deterministic, documented, and within the requested translator or technology scope.

For the complete rules, see [`.github/copilot-instructions.md`](.github/copilot-instructions.md), [`AGENTS.md`](AGENTS.md), and the applicable scoped instruction and skill files.

## How It Works

### Task Skills

The repository includes focused guides for downloader, uploader, and technology work. The selected agent reads the relevant `skills/<mode>/SKILL.md` along with the applicable scoped rules before changing implementation files.

### Agent Modes

Use these focused roles with either harness:

- **E2Downloader** — for creating/modifying downloaders
- **E2Technology** — for technology UI customization
- **E2Uploader** — for creating/modifying uploaders

### Reference Code

The `community/` submodule contains working reference downloaders and technology examples. Agents use these as read-only context. To update the submodule intentionally:

```bash
git submodule update --remote
```

### Technology Customization

For attributes, UI layout, localization, dynamic visibility, event/rule ownership, compute-time motion generation, and process-geometry import, start with the [Technology documentation](docs/technology/README.md). The [teaching overlays](examples/technology/README.md) are small mergeable examples; they do not replace the R2026.1 baselines in `community/Technologies/`.

## Workflow

1. **Analyze**: Use `Simple_Python_Translator.py` in E2 to dump the OLP tree as `.txt`
2. **Build**: Create your downloader in `OLPTranslators/<VENDOR>/`
3. **Test**: Download in E2, compare output with golden files
4. **Debug**: Attach VS Code debugger (port 5254) to E2

## Adding Your Own Vendor Docs

```
docs/ctrl-specific/<VENDOR>/
├── spec/           # Specifications
│   └── *.md
└── current.md      # Change log / working notes
```

## Workshop Documentation

New to E2 customization or Git? Start here:

| Guide | Description |
|-------|-------------|
| [Getting Started](docs/workshop/getting-started.md) | Install everything, create your repo, first-time setup |
| [Daily Workflow](docs/workshop/daily-workflow.md) | Create downloaders, test, commit — your everyday loop |
| [Loop Engineering Case Study](docs/workshop/loop-engineering-case-study.mdx) | Design faster, production-faithful feedback loops and reusable development tools |
| [Git Essentials](docs/workshop/git-essentials.md) | Only the Git commands you actually need |
| [Contributing](docs/workshop/contributing.md) | Share your work back to the community |

## Contributing to Community

To contribute downloaders, examples, or fixes back to the community:

1. **Fork** the [fastsuite-e2-community](https://github.com/cenit-dfs/fastsuite-e2-community) repository
2. Add or modify files in your fork
3. Open a Pull Request — see the [Contributing Guide](docs/workshop/contributing.md) for detailed steps

To contribute skills or docs back to the starter template:

1. **Fork** this repository
2. Make your changes
3. Open a Pull Request

## License

This starter currently does not include a license file. Add the approved license before redistributing a derived repository.

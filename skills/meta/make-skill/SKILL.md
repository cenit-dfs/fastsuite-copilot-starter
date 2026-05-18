---
name: make-skill
description: 'Create new Agent Skills for GitHub Copilot. Use when asked to "create a skill", "make a new skill", "scaffold a skill", create a controller skill, or when building specialized AI capabilities with bundled resources. Generates SKILL.md files with proper frontmatter, directory structure, and optional references/templates folders.'
---

# Make Skill Template

A meta-skill for creating new Agent Skills. Use this skill when you need to scaffold a new skill folder, generate a SKILL.md file, or help users structure a skill with bundled resources.

## When to Use This Skill

- User asks to "create a skill", "make a new skill", or "scaffold a skill"
- User wants to add a specialized capability (e.g., a new controller language skill)
- User needs help structuring a skill with bundled references or templates

## Prerequisites

- Understanding of what the skill should accomplish
- A clear, keyword-rich description of capabilities and triggers
- Knowledge of any bundled resources needed (references, templates)

## Creating a New Skill

### Step 1: Create the Skill Directory

Create a new folder with a lowercase, hyphenated name:

```
skills/<skill-name>/
└── SKILL.md          # Required
```

For this repo, domain skills live at the top level (`skills/kawasaki/`, `skills/downloader/`), meta skills live under `skills/meta/`.

### Step 2: Generate SKILL.md with Frontmatter

Every skill requires YAML frontmatter with `name` and `description`:

```yaml
---
name: <skill-name>
description: '<What it does>. Use when <specific triggers, scenarios, keywords users might say>.'
---
```

#### Frontmatter Fields

| Field | Required | Constraints |
|-------|----------|-------------|
| `name` | **Yes** | 1-64 chars, lowercase letters/numbers/hyphens only, must match folder name |
| `description` | **Yes** | 1-1024 chars, must describe WHAT it does AND WHEN to use it |

#### Description Best Practices

**CRITICAL**: The `description` is the PRIMARY mechanism for automatic skill discovery. Include:

1. **WHAT** the skill does (capabilities)
2. **WHEN** to use it (triggers, scenarios, file types)
3. **Keywords** users might mention in prompts

**Good example:**
```yaml
description: 'Kawasaki AS language reference for E2 downloader development. Use when generating JMOVE/LMOVE motion commands, .TRANS blocks, arc welding syntax (LWS/LWE, KR_TOUCH), or any Kawasaki E-Series robot program output.'
```

**Poor example:**
```yaml
description: 'Kawasaki robot stuff'
```

### Step 3: Write the Skill Body

After the frontmatter, add markdown instructions. Recommended sections:

| Section | Purpose |
|---------|---------|
| `# Title` | Brief overview |
| `## When to Use This Skill` | Reinforces description triggers |
| `## Prerequisites` | Required tools, dependencies |
| `## Step-by-Step Workflows` | Numbered steps for tasks |
| `## References` | Links to bundled docs |

### Step 4: Add Optional Directories (If Needed)

| Folder | Purpose | When to Use |
|--------|---------|-------------|
| `references/` | Documentation agent reads | API references, language manuals |
| `templates/` | Starter code agent modifies | Scaffolds to extend |

## Example: Controller Skill Structure

```
skills/kawasaki/
├── SKILL.md                    # AS language reference + E2 mapping
├── references/
│   └── as-language-summary.md  # Condensed syntax reference
└── templates/
    └── base_kawasaki.py        # Starter downloader scaffold
```

## Validation Checklist

- [ ] Folder name is lowercase with hyphens
- [ ] `name` field matches folder name exactly
- [ ] `description` is 10-1024 characters
- [ ] `description` explains WHAT and WHEN
- [ ] `description` is wrapped in single quotes
- [ ] Body content is actionable and concise

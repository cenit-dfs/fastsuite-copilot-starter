---
name: create-plan
description: 'Create a new implementation plan for multi-phase plugin development, feature roadmaps, or upgrade projects. Use when planning a new downloader, adding a complex feature like arc welding, or defining a workshop/training roadmap.'
---

# Create Implementation Plan

Create a phased implementation plan with discrete, trackable tasks. Plans are structured for both human engineers and AI agents to execute.

## When to Use This Skill

- Planning a new translator from scratch (multi-phase: basic → events → technology plugin)
- Adding a complex feature that spans multiple sessions (arc welding, touch sensing)
- Creating a training/workshop roadmap with milestones
- Breaking down a large refactoring effort

## Output Location

Save implementation plans to:
```
docs/ctrl-specific/<VENDOR>/plan/<name>.md
```

Naming convention: `<purpose>-<component>.md`
- Examples: `feature-kawasaki-downloader.md`, `upgrade-arcwelding-v2.md`, `roadmap-workshop-prep.md`

## Required Template

```md
---
goal: [Concise goal statement]
version: 1.0
date_created: [YYYY-MM-DD]
last_updated: [YYYY-MM-DD]
owner: [Person/team responsible]
status: 'Planned'
tags: [feature, upgrade, roadmap, etc.]
---

# Introduction

![Status: Planned](https://img.shields.io/badge/status-Planned-blue)

[Short description of what this plan achieves.]

## 1. Requirements & Constraints

- **REQ-001**: [Requirement]
- **CON-001**: [Constraint — e.g., "Must not break existing PG06_BASIC output"]

## 2. Implementation Phases

### Phase 1: [Phase Name]

- GOAL-001: [Measurable goal for this phase]

| Task | Description | Status | Date |
|------|-------------|--------|------|
| TASK-001 | [Specific task with file paths] | | |
| TASK-002 | [Specific task] | | |

**Acceptance**: [How to verify this phase is complete — e.g., "golden file PG06_BASIC.as matches"]

### Phase 2: [Phase Name]

- GOAL-002: [Measurable goal]

| Task | Description | Status | Date |
|------|-------------|--------|------|
| TASK-003 | [Specific task] | | |
| TASK-004 | [Specific task] | | |

**Acceptance**: [Verification criteria]

## 3. Alternatives Considered

- **ALT-001**: [Alternative approach and why it was rejected]

## 4. Dependencies

- **DEP-001**: [E.g., "Requires completed Phase 1 basic downloader"]
- **DEP-002**: [E.g., "Golden files for PG01_OP must be available"]

## 5. Files Affected

- **FILE-001**: `OLPTranslators/<VENDOR>/<file>.py` — [what changes]
- **FILE-002**: `docs/ctrl-specific/<VENDOR>/spec/<spec>.md` — [spec to create/update]

## 6. Testing

- **TEST-001**: Compare output vs `golden/<file>` for each phase
- **TEST-002**: Regression test — all previous golden files still pass

## 7. Risks & Assumptions

- **RISK-001**: [Risk and mitigation]
- **ASSUMPTION-001**: [Assumption that must hold]
```

## Status Values

| Status | Badge Color | Meaning |
|--------|-------------|---------|
| `Planned` | blue | Not started |
| `In progress` | yellow | Active work |
| `Completed` | green | All phases done |
| `On Hold` | orange | Blocked or paused |
| `Deprecated` | red | Superseded by another plan |

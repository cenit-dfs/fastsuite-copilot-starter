---
name: create-spec
description: 'Create a new specification file for a downloader, uploader, or technology plugin, optimized for Generative AI consumption. Use when writing specs, defining requirements for a new translator feature, or documenting expected behavior before implementation.'
---

# Create Specification

Create a new specification file that defines requirements, constraints, and interfaces for E2 plugin components. Specs are structured for effective use by Copilot when generating code.

## When to Use This Skill

- Before implementing a new downloader feature (e.g., arc welding plugin, explicit coordinates)
- Before creating a new translator from scratch
- When documenting expected output format from reference/golden files
- When defining attribute mappings between E2 objects and robot language constructs

## Output Location

Save specification files to:
```
docs/<VENDOR>/spec/<name>.md
```

Naming convention: `<scope>-<component>.md`
- Examples: `basic-downloader.md`, `arcwelding-plugin.md`, `explicit-coordinates.md`, `touch-sensing.md`

## Best Practices for AI-Ready Specifications

- Use precise, explicit, and unambiguous language
- Clearly distinguish between requirements, constraints, and recommendations
- Use structured formatting (headings, lists, tables) for easy parsing
- Define all acronyms and domain-specific terms (E2 API names, robot language keywords)
- Include examples from golden files where applicable
- Ensure the document is self-contained

## Required Template

```md
---
title: [Concise Title]
version: 1.0
date_created: [YYYY-MM-DD]
last_updated: [YYYY-MM-DD]
vendor: [VENDOR name, e.g., KAWASAKI]
tags: [downloader, uploader, technology, arc-welding, etc.]
---

# Introduction

[Short description of what this spec defines and the goal it achieves.]

## 1. Purpose & Scope

[What this feature/component does. What programs it applies to. What it does NOT cover.]

## 2. Definitions

[E2 API terms, robot language keywords, attribute names used in this spec.]

| Term | Definition |
|------|-----------|
| ... | ... |

## 3. Requirements & Constraints

[Explicitly list all requirements and constraints.]

- **REQ-001**: [Requirement]
- **CON-001**: [Constraint]

## 4. E2 Object Mapping

[How E2 objects/attributes map to robot language output. Tables are ideal here.]

| E2 Source | Robot Output | Notes |
|-----------|-------------|-------|
| ... | ... | ... |

## 5. Output Format

[Expected output structure with annotated examples from golden files.]

```robot
; Example output with annotations
```

## 6. Acceptance Criteria

[How to verify the implementation is correct — golden file comparison.]

- **AC-001**: Output matches `golden/<FILE>.as` for program X
- **AC-002**: [Additional criteria]

## 7. Edge Cases & Notes

[Known edge cases, special attribute values, mode switches.]

## 8. Related Specs

[Links to related specs or reference files.]
```

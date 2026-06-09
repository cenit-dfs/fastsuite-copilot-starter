---
name: update-spec
description: 'Update an existing specification file based on new requirements, code changes, or discovered edge cases. Use when iterating on a spec after testing reveals gaps, or when adding new features to an existing spec.'
---

# Update Specification

Update an existing specification file based on new requirements or changes discovered during implementation and testing.

## When to Use This Skill

- After testing reveals the spec is incomplete or incorrect
- When adding a new feature to an existing spec (e.g., adding explicit mode to the basic downloader spec)
- When golden files change and the spec needs to reflect new output patterns
- When E2 attribute mappings are corrected after tree dump analysis

## Workflow

1. **Read the existing spec** at `docs/ctrl-specific/<VENDOR>/spec/<name>.md`
2. **Identify what changed** — new requirements, corrected mappings, additional edge cases
3. **Update in place** — preserve existing structure, add/modify sections as needed
4. **Update `last_updated`** in frontmatter
5. **Bump `version`** if the change is significant

## Update Rules

- **Preserve** all existing requirement IDs (REQ-001, CON-001, etc.)
- **Append** new requirements with the next sequential ID
- **Strike through** removed requirements rather than deleting: `~~REQ-003: Old requirement~~`
- **Add a changelog section** at the bottom if the spec has been updated more than twice
- **Keep examples current** — update code snippets to match latest golden files

## Template for Changelog Section

If adding a changelog:

```md
## Changelog

| Version | Date | Change |
|---------|------|--------|
| 1.1 | YYYY-MM-DD | Added explicit coordinate support (REQ-005) |
| 1.0 | YYYY-MM-DD | Initial spec |
```

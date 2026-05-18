---
name: create-adr
description: 'Create an Architectural Decision Record (ADR) documenting a design choice. Use when recording why a particular pattern was chosen (plugin architecture, coordinate mode handling, event mapping strategy), or when justifying a technical approach for future reference.'
---

# Create Architectural Decision Record

Create an ADR document that records a significant design decision, its context, consequences, and alternatives considered.

## When to Use This Skill

- Choosing between design patterns (e.g., plugin architecture vs. inheritance)
- Deciding on a coordinate output strategy (implicit vs. explicit handling)
- Selecting an event mapping approach
- Any decision that future engineers will ask "why did we do it this way?"

## Output Location

Save ADR files to:
```
docs/adr/adr-NNNN-<title-slug>.md
```

Sequential numbering: `adr-0001-plugin-architecture.md`, `adr-0002-coordinate-mode-handling.md`

## Required Template

```md
---
title: "ADR-NNNN: [Decision Title]"
status: "Accepted"
date: "YYYY-MM-DD"
authors: "[Names/Roles]"
tags: ["architecture", "downloader"]
---

# ADR-NNNN: [Decision Title]

## Status

**Accepted** | Proposed | Rejected | Superseded | Deprecated

## Context

[Problem statement. What forced this decision? Technical constraints, E2 API limitations, customer requirements, maintainability concerns.]

## Decision

[Chosen approach with clear rationale.]

## Consequences

### Positive

- **POS-001**: [Benefit — e.g., "Keeps customization surface small"]
- **POS-002**: [Benefit — e.g., "Matches ABB_IRC5.py proven pattern"]

### Negative

- **NEG-001**: [Trade-off — e.g., "More files to maintain"]
- **NEG-002**: [Limitation]

## Alternatives Considered

### [Alternative 1]

- **Description**: [What this approach would look like]
- **Rejection Reason**: [Why not chosen]

### [Alternative 2]

- **Description**: [What this approach would look like]
- **Rejection Reason**: [Why not chosen]

## Implementation Notes

- **IMP-001**: [Key implementation detail]
- **IMP-002**: [Migration strategy if replacing existing approach]

## References

- **REF-001**: [Related spec, golden file, or community example]
- **REF-002**: [External documentation or E2 API reference]
```

## Status Values

| Status | Meaning |
|--------|---------|
| Proposed | Under discussion, not yet committed |
| Accepted | Decision made, implementation follows |
| Rejected | Considered but not adopted |
| Superseded | Replaced by a newer ADR (link to it) |
| Deprecated | No longer relevant |

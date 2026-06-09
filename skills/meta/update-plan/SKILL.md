---
name: update-plan
description: 'Update an existing implementation plan with progress, new tasks, or changed requirements. Use when marking tasks complete, adding discovered work, or adjusting phases based on testing results.'
---

# Update Implementation Plan

Update an existing implementation plan file to reflect current progress, new discoveries, or changed requirements.

## When to Use This Skill

- Marking tasks as completed (✅) after successful golden-file comparison
- Adding new tasks discovered during implementation
- Adjusting phase boundaries or acceptance criteria
- Changing plan status (Planned → In progress → Completed)

## Workflow

1. **Read the existing plan** at `docs/ctrl-specific/<VENDOR>/plan/<name>.md`
2. **Apply updates**:
   - Mark completed tasks with ✅ and date
   - Add new tasks with next sequential IDs
   - Update `status` in frontmatter if phase boundaries change
   - Update `last_updated` date
3. **Preserve history** — never delete completed tasks or change their descriptions

## Update Rules

- **Task completion**: Add ✅ and date: `| TASK-001 | Description | ✅ | 2026-05-18 |`
- **New tasks**: Append with next ID in the appropriate phase
- **Blocked tasks**: Add a note column or inline comment: `| TASK-005 | Description | ⏸️ blocked by DEP-002 | |`
- **Phase completion**: When all tasks in a phase have ✅, note it in the phase header
- **Status transitions**: Update frontmatter `status` field when overall plan status changes

## Status Transitions

```
Planned → In progress    (when first task starts)
In progress → Completed  (when all phases done)
In progress → On Hold    (when blocked externally)
On Hold → In progress    (when unblocked)
Any → Deprecated         (when superseded)
```

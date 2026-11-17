---
description: "Debrief the current session and turn genuine, reusable lessons into new or updated skills and docs."
agent: "agent"
tools: ["search", "editFiles", "runInTerminal"]
---

# Close Session — Knowledge Capture

Run this at the end of a working session to make sure hard-won lessons survive past this
conversation. This operationalizes the "Session Debrief" checklist in
[copilot-instructions.md](../copilot-instructions.md).

**Do not commit or push.** Edit and stage files only — the user reviews and commits separately
(see the repo's standing safety rule).

## Step 0 — Gather What Actually Happened

Don't rely on memory of the conversation alone — ground every finding in real diffs:

1. Review this session's conversation for: bugs found and their root causes, API gotchas,
   workarounds, decisions/tradeoffs made, and anything that took real investigation to figure out.
2. Run `git status` and `git diff` in the main repo, and in `community/` if it was touched, to see
   what actually changed.
3. List `/memories/session/` and `/memories/repo/` — session and repo memory notes written during
   this conversation are candidate material; they're ephemeral or workspace-local, while skills
   and docs are git-tracked and visible to every collaborator and future agent.

## Step 1 — Filter for Genuine, Reusable Lessons

For each candidate finding, ask: **would a different agent, on a different vendor or a different
day, hit the same wall without this note?** If not, discard it — do not manufacture busywork just
because this prompt runs regularly. It is a valid outcome to report "nothing this session rose to
the level of a skill/doc update."

Keep only findings that fit one of these categories (matching the copilot-instructions checklist):

1. **Cross-vendor pattern** — new framework API usage, event handling pattern, traversal strategy,
   or a mistake generic enough to bite any vendor.
2. **Vendor-specific gotcha** — output order, Euler convention, formatting quirk, state-machine
   flag, or an API split (like modify-time vs download-time attribute access) specific to one
   controller.
3. **Output format change** — the downloader/uploader now emits something different than before.
4. **Golden coverage gap** — new program variants exist without golden fixtures.
5. **Platform discovery** — undocumented E2 callback behavior, attribute-type trap, or framework
   rule not yet written down anywhere in this repo or the vault.

## Step 2 — Route Each Finding to Its Target

| Finding type | Target | Action |
|---|---|---|
| Cross-vendor pattern | `skills/downloader/SKILL.md`, `skills/technology/SKILL.md`, or `skills/uploader/SKILL.md` | Edit the relevant existing skill directly. |
| Pattern with no existing home | New skill folder | Use [skills/meta/make-skill/SKILL.md](../../skills/meta/make-skill/SKILL.md) to scaffold it. |
| Vendor-specific gotcha | `docs/ctrl-specific/<VENDOR>/spec/downloader-patterns.md` (or the equivalent spec file) | Add a short, scoped entry — no walls of text. |
| Output format change | `docs/ctrl-specific/<VENDOR>/spec/*.md` and `docs/ctrl-specific/<VENDOR>/current.md` | Update both per the repo's documentation rule. |
| Golden coverage gap | Golden fixtures | Run the "Check Golden Coverage" task; add missing golden files if feasible now, otherwise log the gap in `current.md`. |
| Platform discovery | Obsidian vault `90_Inbox_AI/` | Only if the `obsidian-e2` MCP is connected. Search the vault first to avoid duplicates, then `create_vault_file` with frontmatter `status: draft`, `source: agent-generated`. |
| Durable fact with no clear skill/doc home | User or repo memory | Last resort only — prefer git-tracked skills/docs for anything a collaborator or future agent needs. |

## Step 3 — Apply the Updates

- Edit existing skills/docs in place; keep additions short and scoped (this repo's style is
  concise, actionable notes, not prose).
- When updating a skill, re-check its frontmatter `description` still covers any new triggers
  introduced by the change.
- `git add` the touched files so they're visible in `git status`, but leave the commit itself to
  the user.

## Step 4 — Report Back

Summarize, in a short list:
- What was updated (linked file paths) and why, one line each.
- What was explicitly considered and rejected as not reusable enough.
- Any findings routed to the vault inbox or left as memory notes instead of git-tracked files, with
  the reason.

If nothing warranted a change, say so plainly instead of padding the summary.

---
description: Run the next step in memory update process (orchestrator)
---

Intelligent memory update orchestrator. Determines which step to run next based on file existence.

## Process

1. Check if today's staging directory exists: `Memory/YYYYMMDD-memory-update/`
2. If not, this is a new update cycle — run the scan phase

## Determining Next Step

Check which files exist in the staging directory to determine progress:

| Check | Missing File | Action |
|-------|--------------|--------|
| `scan-manifest.md` missing | Run scan phase |
| `memory-organization.md` missing | Run `/memory-org` |
| `memory-strategy.md` missing | Run `/memory-strategy` |
| `memory-projects.md` missing | Run `/memory-projects` |
| `memory-decisions.md` missing | Run `/memory-decisions` |
| `memory-team-dynamics.md` missing | Run `/memory-team` |
| `memory-relationships.md` missing | Run `/memory-relationships` |
| All 6 memory files exist | Run `/memory-consolidate` |

## For Each Memory Update Phase

Follow all guidelines in `Guidelines/memory-consolidation-guidelines.md`, especially:
- Professional tone
- Current state focus
- Status markers

Apply strict factual documentation standards:
- Source every assessment to a document/meeting
- Use metrics not adjectives
- Quote rather than interpret
- Remove ALL dramatic language unless directly quoted
- Focus on observable facts not predictions

Challenge yourself: "Is this fact or opinion?"

## Output

1. Report which step is being run and why
2. Execute that single step
3. STOP after completing one step
4. Inform user what to run next (or run `/memory-update` again)

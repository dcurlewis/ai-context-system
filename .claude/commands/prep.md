# Meeting Preparation

Prepare contextual briefing material for an upcoming meeting.

## Instructions

1. Read `config.yaml` for user identity, team, and role
2. Read `Memory/memory-index.md` for full context
3. Ask the user: **What meeting are you preparing for?** (or accept meeting name/topic as input)
4. Gather all relevant context and produce a briefing document

## Context Gathering

Search across these sources for anything related to the meeting topic, attendees, or project:

### Memory Files
- `Memory/memory-projects.md` — active project status
- `Memory/memory-decisions.md` — recent decisions related to this topic
- `Memory/memory-team-dynamics.md` — dynamics with attendees
- `Memory/memory-relationships.md` — relationship context for attendees

### Curated Context
- `Curated-Context/Project-Insights/` — previous meeting insights on this topic
- `Curated-Context/People/` — profiles of expected attendees
- `Curated-Context/Teams/` — team context if relevant
- `Curated-Context/Strategic-Documents/` — relevant strategy docs
- `Curated-Context/Technical-Documentation/` — relevant technical docs

### Synced Data
- `Synced-Data/Jira/` — ticket status relevant to the meeting
- `Synced-Data/Calendar/` — meeting details if available

## Output

Display the briefing directly to the user (and optionally save to `Curated-Context/Project-Insights/`).

### Briefing Template

```markdown
# Meeting Prep: {Meeting Name}

**Date**: {Meeting date if known}
**Attendees**: {Expected attendees with [[wikilinks]]}
**Your role**: {What the user's role/stake is in this meeting}

## Context
{2-3 paragraph summary of the current state of affairs relevant to this meeting.
Include recent decisions, open issues, and any political dynamics.}

## Key People in the Room
| Person | Role | What to Know |
|--------|------|-------------|
| [[Person]] | {Role} | {Key context — their position, concerns, recent interactions} |

## Topics to Expect
1. **{Topic}** — {Current status, your position, key facts}
2. **{Topic}** — {Current status, your position, key facts}

## Open Decisions
- {Decision needed} — {Options, your recommended position, who decides}

## Your Talking Points
- {Key point you should make}
- {Key point you should make}
- {Question you should ask}

## Watch For
- {Political dynamic to be aware of}
- {Potential conflict or sensitive topic}
- {Opportunity to advance a goal}

## Recent History
{Summary of the last 2-3 interactions related to this topic, with dates}
```

## Notes
- If insufficient context exists, say so clearly — don't fabricate
- Highlight gaps: "I don't have context on X — you may want to check before the meeting"
- Prioritise actionable intelligence over comprehensiveness

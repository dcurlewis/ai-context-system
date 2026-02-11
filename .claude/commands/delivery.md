# Generate Delivery / Status Update

Generate a polished status update or delivery report based on recent activity and memory.

## Instructions

1. Read `config.yaml` for user identity, role, team, and communication style
2. Read `Memory/memory-projects.md` for active project status
3. Read `Memory/memory-decisions.md` for recent decisions
4. Scan recent `Curated-Context/Daily-Journals/` for this week's activity
5. Scan recent `Curated-Context/Project-Insights/` for meeting outcomes
6. Check `Synced-Data/Jira/` for ticket progress if available
7. Ask the user for the reporting period (or default to "this week")

## Context Gathering

### What to Include
- **Accomplishments**: What was delivered, completed, or unblocked
- **Decisions made**: Key decisions with brief context
- **In progress**: What's actively being worked on
- **Risks & blockers**: Anything impeding progress
- **Coming up**: Key milestones or events in the next period
- **Team highlights**: Notable contributions from team members

### What to Exclude
- Routine meetings (unless they produced significant outcomes)
- Minor tasks and housekeeping
- Internal team dynamics (unless reporting to someone who needs to know)

## Output

### Save Location
`Curated-Context/Delivery-Reports/YYYYMMDD-delivery-report.md`

### Output Template

```markdown
# Delivery Report — {Period}

**Author**: {Name from config.yaml}
**Role**: {Role from config.yaml}
**Period**: {Date range}

## Highlights
{2-3 sentence executive summary of the most important outcomes}

## Delivered
- **{Item}**: {Brief description of what was completed and its impact}
- **{Item}**: {Brief description}

## Decisions Made
| Decision | Context | Impact |
|----------|---------|--------|
| {decision} | {brief context} | {what it means} |

## In Progress
| Item | Status | Expected Completion |
|------|--------|-------------------|
| {item} | {On track / At risk / Blocked} | {Date} |

## Risks & Blockers
| Risk/Blocker | Impact | Mitigation |
|-------------|--------|-----------|
| {issue} | {what's affected} | {what's being done} |

## Coming Up
- {Upcoming milestone or event} — {Date}

## Team Highlights
- [[Person]]: {Notable contribution}
```

### Tone & Style

Apply the communication style from `config.yaml`:
- **Professional**: Clean, factual, results-oriented
- **Imperial**: Authoritative, concise, emphasises command decisions
- **Casual**: Friendly, accessible, emphasises collaboration

The report should make the user look competent and on top of things — because they are.

## Notes
- If there isn't enough information for a full report, say so and suggest gathering more context first
- Offer to adjust the format for different audiences (team, leadership, stakeholders)
- The user may want to edit the output before sending — present it as a draft
- Wikilink people and projects for internal use; remove wikilinks if producing for external consumption

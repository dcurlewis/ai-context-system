---
description: Prepare delivery review summary from Jira and GitHub sync data
---

Analyse the Jira and GitHub sync data to prepare a concise delivery review summary. The report should be scannable in under 5 minutes.

## Process

1. **Load Data Sources**
   - Read `Synced-Data/Jira/INDEX.md` for overview
   - Use `Synced-Data/Jira/index.json` for filtering and analysis
   - Load individual issue files from `Synced-Data/Jira/issues/{KEY}.json` only when detailed information is needed
   - Read `Synced-Data/GitHub/index.json` for PR data (if available; proceed without if missing)
   - Note sync timestamps from `Synced-Data/Jira/_meta.json` and `Synced-Data/GitHub/_meta.json`
   - Read `Memory/memory-projects.md` and `Memory/memory-decisions.md` for context

2. **Correlate GitHub and Jira**
   - Match PRs to Jira tickets via the `jira_keys` field extracted from PR titles
   - Flag Jira tickets still "In Progress" that have merged PRs (stale status candidates)
   - Identify significant PRs with no Jira link (uncaptured work)

3. **Generate Report** using the template below

## Report Template

```markdown
# Delivery Review
**Date:** [Current Date]
**Period:** Past fortnight
**Data Sources:** Jira sync ([timestamp]) | GitHub sync ([timestamp])

## Risks & Callouts

[Items requiring senior leadership attention:
- Blocked work with business impact
- Resource or dependency risks
- Overdue milestones
- Anything needing escalation or input

Keep this short. If there are no significant risks, say so explicitly.]

## Capability Delivery

### Completed Work

#### Death Star Engineering
[Bullet list of meaningful deliveries from the past fortnight.
Focus on user value and impact, not individual tickets.
Group related tickets into single line items where they form a coherent delivery.
Reference Jira keys inline for traceability, e.g. "Thermal exhaust port remediation phase 1 complete (DS-608, DS-671)"]

#### Imperial Naval Operations
[Same format]

### Planned & Upcoming

#### Death Star Engineering
[What's coming in the next fortnight. Less detailed than completed work.
Draw from Jira "In Progress" and "To Do" items at levels 2-3,
plus any context from memory files about upcoming milestones or priorities.]

#### Imperial Naval Operations
[Same format]

## Engineering Activity
**Source:** GitHub ([timestamp]) | **Period:** [lookback days]

[Summary table per team:

| Team | PRs Merged | Key Contributors | Repos |
|------|-----------|-----------------|-------|
| DS Eng | 18 | Moff Jerjerrod (10), TK-421 (8) | death-star, turbolaser-systems |
| Naval Ops | 12 | Admiral Piett (7), Captain Needa (5) | fleet-ops, navigation-charts |

Notable items:
- PRs not linked to any Jira ticket (uncaptured work worth highlighting)
- Jira tickets marked done with no associated PRs (non-code work or stale data)
- Stale status indicators: tickets still "In Progress" with merged PRs]
```

## Key Principles

- **Brevity over completeness.** The report is a summary, not a dump. Individual ticket details live in Jira and GitHub; the report should synthesise.
- **Capability-oriented.** Organised by team (Death Star Engineering, Imperial Naval Operations), not by Jira hierarchy level.
- **Forward and backward looking.** "Completed" and "Planned" sections give the fortnight-over-fortnight view.
- **Engineering Activity is supplementary.** It adds data richness but should not duplicate the Capability Delivery section. Its main value is surfacing work that Jira misses and flagging data quality issues.
- **Risks up front.** Senior leadership reads top-down; the most important section comes first.
- **Graceful degradation.** If GitHub data is unavailable, omit the Engineering Activity section and note it. The Capability Delivery section works from Jira alone.

## Output

Create a markdown file in `Curated-Context/Delivery-Reports/` with filename format `[YYYYMMDD]-delivery-review.md`. Keep it concise, focusing on items that matter for a delivery review meeting. Use bullet points and clear language. Prioritise business value and user impact over technical details.

## Tips

- Focus on levels 0-2 (Company Goals, Team Goals, Milestones) for strategic overview
- Drill into level 3+ only for blockers or significant achievements
- Group related tickets into coherent deliveries rather than listing each individually
- Use issue descriptions and comments to understand context, not just titles
- Cross-reference GitHub PRs with Jira to find stale ticket statuses

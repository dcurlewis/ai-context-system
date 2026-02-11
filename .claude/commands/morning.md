# Morning Briefing

Start the day with a comprehensive briefing — calendar, priorities, context, and anything that needs attention.

## Instructions

1. Read `config.yaml` for user identity, timezone, team, and role
2. Read all memory files for current state:
   - `Memory/memory-index.md`
   - `Memory/memory-projects.md`
   - `Memory/memory-decisions.md`
   - `Memory/memory-team-dynamics.md`
   - `Memory/memory-relationships.md`
3. Check today's calendar data in `Synced-Data/Calendar/`
4. Check for unprocessed raw materials in `Raw-Materials/`
5. Review yesterday's daily journal in `Curated-Context/Daily-Journals/` if it exists
6. Generate the morning briefing

## Calendar Integration

### If Calendar Data Available
Check `Synced-Data/Calendar/` for today's events. If a calendar sync script exists (`Scripts/calendar-today.py`), note that the user can run it to refresh.

For each meeting today:
- What is it?
- Who's attending? (Cross-reference with `Memory/memory-relationships.md`)
- What context is relevant? (Check recent meeting insights, decisions, project status)
- What should the user prepare for?

### If No Calendar Data
Note that no calendar data is available. Suggest:
- Running the calendar sync script if configured
- Or manually sharing today's schedule

## Briefing Structure

### Output Template

```markdown
# Morning Briefing — {Day of Week}, {Date}

**Good morning, {Name from config.yaml}.**

## Today's Schedule
| Time | Meeting | Attendees | Key Context |
|------|---------|-----------|-------------|
| {time} | {meeting} | [[Person]], [[Person]] | {1-line context} |

*{N meetings today. Busiest period: {time range}. First meeting: {time}.}*

## Top Priorities
Based on active projects, pending decisions, and yesterday's activity:

1. **{Priority}** — {Why it's important today} — {Specific action to take}
2. **{Priority}** — {Why it's important today} — {Specific action to take}
3. **{Priority}** — {Why it's important today} — {Specific action to take}

## Decisions Pending
| Decision | Deadline | Who's Waiting |
|----------|----------|--------------|
| {decision} | {when} | [[Person]] |

## People to Check In With
Based on relationship dynamics and recent context:
- **[[Person]]**: {Why — e.g., "seemed stressed in yesterday's meeting", "waiting on your input", "has a deadline Friday"}

## Project Status Snapshot
| Project | Status | Next Milestone | Flag |
|---------|--------|---------------|------|
| [[Project]] | {On track/At risk/Blocked} | {What's next} | {Any concern} |

## Unprocessed Items
{List any raw materials that haven't been processed yet}
- {N} meeting transcripts in `Raw-Materials/Meeting-Transcripts/`
- {N} documents in `Raw-Materials/Docs/`
- {N} Slack exports in `Raw-Materials/Slack/`

## Yesterday's Loose Ends
{From yesterday's daily journal, if it exists:}
- {Anything flagged as follow-up}
- {Action items that were due yesterday}

## Weather / Context
**Timezone**: {From config.yaml}
**Location**: {From config.yaml}
```

## Day-of-Week Variations

### Monday
- Include a "week ahead" section with key events and deadlines for the week
- Note any delivery reports or status updates due this week
- Suggest running `/memory-scan` to catch up after the weekend

### Friday
- Include a "week in review" prompt
- Suggest running `/delivery` to capture the week's accomplishments
- Note any loose ends to close before the weekend

## After the Briefing

Create/update today's daily journal: `Curated-Context/Daily-Journals/YYYY-MM-DD.md`

```markdown
# Daily Journal — {Date}

**User**: {Name from config.yaml}
**Morning priorities**:
1. {Priority from briefing}
2. {Priority from briefing}
3. {Priority from briefing}

---

## Thoughts & Observations

```

## Notes
- The morning briefing is the system's flagship command — it should feel like having a chief of staff
- Prioritise actionable intelligence over comprehensiveness
- If memory is sparse (new system), acknowledge it and suggest building context: "Your memory system is still new. The briefing will get richer as you process more meetings and documents."
- Surface surprises and risks — don't just list facts
- Apply communication style from `config.yaml`

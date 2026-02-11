# Capture a Thought

Quickly capture a thought, observation, or reflection without full processing.

## Instructions

1. Read `config.yaml` for user identity and communication style
2. Accept the user's thought as input (the text following the command, or prompt for it)
3. Save it as a timestamped entry

## Process

### Categorise the Thought
Determine the best category:
- **Observation** — something noticed about a person, project, or situation
- **Idea** — a new idea or approach worth remembering
- **Decision** — a decision made or position taken
- **Reflection** — a personal reflection on how something went
- **Follow-up** — something to revisit or action later
- **Quote** — something someone said that's worth capturing

### Save Location

Append to today's daily journal: `Curated-Context/Daily-Journals/YYYY-MM-DD.md`

If the daily journal doesn't exist yet, create it with:

```markdown
# Daily Journal — {Date}

**User**: {Name from config.yaml}

---

## Thoughts & Observations
```

### Entry Format

```markdown
### {HH:MM} — {Category}
{The thought, with [[wikilinks]] for any people, projects, or teams mentioned}
```

## Memory Updates

If the thought contains:
- A **decision** → also append to `Memory/memory-decisions.md`
- A **team/relationship observation** → also append to `Memory/memory-team-dynamics.md`
- A **project insight** → also append to `Memory/memory-projects.md`

## Notes
- Keep it lightweight — this is for quick capture, not deep analysis
- Use wikilinks for any named entities (people, projects, teams)
- The daily journal accumulates throughout the day
- Confirm to the user: "Captured to {filename}" with the category

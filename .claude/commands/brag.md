# Achievement / Brag Document Update

Update the running achievement log — a structured record of impact, accomplishments, and growth for performance reviews, promotions, and interviews.

## Instructions

1. Read `config.yaml` for user identity, role, and team
2. Read existing brag document at `Curated-Context/Achievement-Log.md` (create if it doesn't exist)
3. Scan recent activity for new achievements to capture
4. Update the brag document

## Why This Matters

Nobody remembers what they accomplished six months ago. This document captures achievements as they happen, with context and impact — so when review season or an interview comes around, the evidence is already assembled.

## Achievement Sources

Scan these locations for recent accomplishments:
- `Curated-Context/Daily-Journals/` — daily activity and wins
- `Curated-Context/Project-Insights/` — meeting outcomes and delivery
- `Curated-Context/Delivery-Reports/` — past status updates
- `Memory/memory-projects.md` — project milestones reached
- `Memory/memory-decisions.md` — impactful decisions led
- `Synced-Data/Jira/` — tickets completed if available

Also ask the user: **"Anything you'd like to add that isn't captured elsewhere?"**

## Achievement Categories

### Delivery & Execution
- Projects delivered or milestones hit
- Deadlines met, especially challenging ones
- Problems solved, fires put out

### Leadership & Influence
- Decisions made that shaped direction
- People developed or mentored
- Difficult conversations navigated
- Cross-team collaboration driven

### Strategic Impact
- Initiatives proposed or championed
- Process improvements implemented
- Cost savings or efficiency gains
- Risk mitigation

### Technical Excellence
- Technical decisions made and their impact
- Systems designed, built, or improved
- Technical debt reduced
- Quality improvements

### Team & Culture
- Team morale or cohesion improved
- Hiring contributions (interviews, offers, onboarding)
- Knowledge sharing (docs, presentations, mentoring)
- Culture initiatives

## Output

### Brag Document Structure

Create or update `Curated-Context/Achievement-Log.md`:

```markdown
# Achievement Log — {Name from config.yaml}

**Role**: {Role from config.yaml}
**Team**: {Team from config.yaml}
**Last updated**: {Date}

---

## {Current Quarter/Year}

### {Date} — {Achievement Title}
**Category**: {Delivery / Leadership / Strategic / Technical / Team}
**Impact**: {Who or what was affected, and how}

{2-4 sentences describing what you did, why it mattered, and the outcome.
Include specific metrics where possible. Use [[wikilinks]] for people and projects.}

**Evidence**: {Link to meeting insight, decision record, or delivery report}

---

### {Date} — {Achievement Title}
**Category**: {Category}
**Impact**: {Impact}

{Description}

**Evidence**: {Source}

---

## {Previous Quarter/Year}
{Older entries, potentially consolidated}
```

### Formatting Rules
- **Newest entries at the top** — most recent first within each section
- **Be specific** — "Led the [[Death Star II Construction]] review that identified 3 critical risks" not "Helped with project"
- **Quantify where possible** — numbers, percentages, timelines
- **Include the "so what"** — what was the impact, not just the action
- **Wikilink everything** — people, projects, meetings, decisions

## Periodic Prompts

When running this command, also check:
- **Has it been 2+ weeks since the last entry?** Prompt: "It's been a while — let's make sure nothing's slipping through the cracks."
- **Is a review cycle approaching?** Offer to generate a review-ready summary from the brag doc.
- **Are there patterns?** Note if achievements cluster in certain categories and suggest if others are underrepresented.

## Notes
- This is one of the highest-ROI commands in the system — regular use pays off hugely at review time
- Don't be modest — this is a private document, not a public bio
- The "Evidence" link back to other curated context creates a paper trail
- Suggest running after any significant delivery, decision, or milestone

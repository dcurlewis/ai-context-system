# Meeting Communication Analysis

Deep analysis of communication patterns, dynamics, and effectiveness from a meeting transcript. Goes beyond the standard `/meeting` processing to focus on interpersonal dynamics and the user's own performance.

## Instructions

1. Read `config.yaml` for user identity, role, team, and communication style
2. Read `Memory/memory-relationships.md` for existing relationship context
3. Read `Memory/memory-team-dynamics.md` for existing team dynamics
4. Accept a meeting transcript (file path or reference to an already-processed meeting)
5. If referencing a processed meeting, also read the insight file from `Curated-Context/Project-Insights/`
6. Perform deep communication analysis

## This is Different From /meeting

`/meeting` processes a transcript into structured insights for knowledge capture.

`/meeting-analysis` goes deeper on the **human side** — communication patterns, power dynamics, the user's effectiveness, and coaching feedback. Think of it as having a trusted advisor watch the meeting and give you notes.

## Analysis Framework

### 1. Conversation Architecture
- **Who drove the agenda?** Who had the power in the room?
- **Talk-time distribution**: Who spoke most? Who was barely heard?
- **Turn-taking patterns**: Who interrupts? Who gets interrupted? Who defers?
- **Question dynamics**: Who asked questions? Were they genuine or performative?
- **Topic transitions**: Who changed the subject? Were any topics cut short?

### 2. Power & Influence Dynamics
- **Formal vs. informal power**: Did the most senior person dominate, or did influence flow differently?
- **Coalition signals**: Who agreed with whom? Are there forming alliances?
- **Deference patterns**: Who looked to whom before speaking? Who sought permission?
- **Challenge dynamics**: Was authority challenged? How was it handled?

### 3. Emotional & Political Subtext
- **Tension points**: Where did the conversation get uncomfortable?
- **Unspoken concerns**: What was NOT said that probably should have been?
- **Defensive reactions**: Who got defensive and about what?
- **Enthusiasm vs. compliance**: Who was genuinely bought in vs. going along?
- **Territory marking**: Was anyone protecting their domain?

### 4. Individual Communication Profiles

For each key participant:

```markdown
#### [[Person Name]]
**Communication style in this meeting**: {Assertive/Collaborative/Passive/Aggressive/Analytical}
**Key contributions**: {What they brought to the discussion}
**Body language signals**: {If visible from transcript — hedging language, qualifiers, etc.}
**Alignment**: {Aligned with / Opposed to / Neutral on key topics}
**Notable moments**: {Specific quotes or interactions worth noting}
```

### 5. The User's Performance (The Most Important Section)

Provide honest, constructive feedback on how the user came across:

```markdown
## Your Performance

### What You Did Well
- {Specific example with evidence from the transcript}
- {Specific example}

### What Could Improve
- {Specific observation} — *Suggestion: {How to handle it differently next time}*
- {Specific observation} — *Suggestion: {Alternative approach}*

### Your Influence in the Room
{Assessment of how the user was perceived, how much influence they wielded, and whether they achieved their likely goals}

### Communication Patterns Observed
- **Your talk-time**: {Approximate share}
- **Your style**: {Assertive/Facilitative/Directive/etc.}
- **Questions asked**: {Types — open, closed, leading, genuine}
- **Listening signals**: {Did you build on others' points? Acknowledge before redirecting?}

### Specific Coaching Notes
1. {Actionable coaching point with example from the transcript}
2. {Actionable coaching point}
```

### 6. Relationship Implications

Based on this meeting, what changed in relationships?
- **Strengthened**: {Which relationships and why}
- **Strained**: {Which relationships and why}
- **New dynamics**: {Anything that shifted}
- **Action needed**: {Relationship maintenance tasks}

## Output

### Save Location
`Curated-Context/Project-Insights/YYYYMMDD-Meeting-Analysis-{Meeting-Name}.md`

### Full Template

```markdown
# Meeting Communication Analysis — {Meeting Name}

**Date**: {Date}
**Analysed for**: {User name from config.yaml}
**Attendees**: [[Person 1]], [[Person 2]], [[Person 3]]

## Executive Summary
{3-4 sentence summary focusing on the dynamics, not the content}

## Conversation Architecture
{Talk-time, turn-taking, question dynamics}

## Power & Influence Dynamics
{Who had power, how it flowed, coalition signals}

## Emotional & Political Subtext
{Tension, unspoken concerns, territory}

## Individual Profiles
{Per-person analysis}

## Your Performance
{Strengths, improvements, coaching notes}

## Relationship Implications
{What changed, what to do about it}

## Key Takeaways
1. {Most important insight about the dynamics}
2. {Most actionable coaching point for the user}
3. {Most significant relationship implication}
```

## Memory Updates

After analysis:
- Update `Memory/memory-team-dynamics.md` with new dynamic observations
- Update `Memory/memory-relationships.md` with relationship changes
- Update relevant `Curated-Context/People/` profiles

## Notes
- This command requires a high degree of candour — the user wants honest feedback, not flattery
- Base all observations on evidence from the transcript — cite specific moments
- The coaching should be constructive and specific, not generic advice
- Acknowledge when you're inferring vs. observing — "From the hedging language used, it seems like..."
- Apply the user's communication style from `config.yaml` to the output, but not to the feedback itself (feedback should be direct regardless of style preference)

---
description: Meta-analysis of past 7 days' meetings with aggregated communication feedback
---

Perform a meta-analysis of meetings from the past 7 days, covering statistics and aggregated personal communication feedback.

## Step 1: Gather Meeting Data

1. Calculate the date range: **7 calendar days ending yesterday** (inclusive). This is a strict calendar-based lookback, NOT the current work week. Since this command typically runs early on a Friday morning before any meetings have occurred, the range covers the previous Friday through Thursday. For example, if today is Friday 2026-02-13, the range is 2026-02-06 (Friday) through 2026-02-12 (Thursday).
2. Scan both meeting directories for files with YYYYMMDD prefixes falling within that range:
   - `Curated-Context/Meeting-Insights/*.md`
   - `Curated-Context/Meeting-Insights/One-on-ones/*.md`
3. Read all matching meeting summaries

**Important**: Do NOT look at today's calendar or note the absence of meetings today. This analysis reviews meeting *summaries already written* from the past 7 days, not today's upcoming schedule.

## Step 2: Extract Meeting Metadata

For each meeting, extract:
- **Date** (from filename YYYYMMDD prefix)
- **Title** (from filename or H1 heading)
- **Duration** (from `Duration:` field, estimate if not present)
- **Participant count** (from `Participants:` field)
- **Meeting type** (classify based on participant count and context):
  - **One-on-one**: 2 participants
  - **Small group**: 3-5 participants
  - **Large group**: 6+ participants
  - **Vendor/External**: Participants from outside the organisation
  - **Calibration/Review**: Process-oriented meetings (role change, delivery review, etc.)
  - **Workshop/Planning**: Collaborative working sessions
  - **All Hands/Show & Tell**: Broadcast-style meetings

## Step 3: Generate Statistics Report

Present the following statistics:

### Meeting Volume
- Total meeting count for the 7-day period
- Meetings per day (breakdown and average)
- Comparison to typical week if pattern is observable

### Meeting Type Distribution
| Type | Count | % of Total |
|------|-------|------------|
| One-on-one | X | Y% |
| Small group | X | Y% |
| ... | ... | ... |

### Time Investment
- Total estimated meeting time (sum of durations)
- Average meeting duration
- Average time per day in meetings
- Longest meeting of the week
- Shortest meeting of the week

### Other Notable Patterns
- Most frequent meeting participants
- Peak meeting days
- Any notable scheduling patterns

## Step 4: Aggregate Personal Communication Feedback

Search each meeting summary for `## Meeting Analysis` section (and any `Personal Communication Feedback` subsections within).

### Collection
- List which meetings included personal communication feedback
- Note which meetings did NOT include feedback (typically shorter meetings under 10 minutes)

### Synthesis Across Meetings

Analyse the collected feedback sections and synthesise across these dimensions:

#### Participation Patterns
- How does participation vary by meeting type?
- Any patterns in speaking time or contribution level?

#### Communication Strengths (recurring positives)
- What communication behaviours appear consistently effective?
- Which patterns are noted as strengths multiple times?

#### Communication Patterns to Watch
- Any behaviours noted as improvement areas more than once?
- Patterns that may be limiting effectiveness?

#### Language and Clarity
- Hedging language patterns
- Directness vs qualification
- Informal vs formal register choices

#### Listening and Engagement
- Evidence of active listening across meetings
- Building on others' ideas vs introducing new topics

#### Strategic Positioning
- How are you positioning in different meeting contexts?
- Authority signalling patterns

### Aggregated Recommendations

Based on patterns across all meetings with feedback:

1. **Continue doing**: Behaviours to maintain (appeared effective in multiple contexts)
2. **Experiment with**: Adjustments that might improve impact
3. **Be mindful of**: Patterns that could become problematic if unchecked

## Output Format

Structure the report as:

```
# Meeting Meta-Analysis: [Date Range]

## Summary
[2-3 sentences: total meetings, key finding on time investment, key communication insight]

## Meeting Statistics
[Tables and metrics from Step 3]

## Communication Feedback Analysis

### Meetings Reviewed for Communication Feedback
[List of meetings with feedback sections]

### Synthesised Observations
[Analysis from Step 4]

### Key Takeaways
[Aggregated recommendations]

---
*Analysis generated: [Date]*
```

## Notes

- If fewer than 3 meetings have Meeting Analysis sections, note this limitation and provide what analysis is possible
- Focus on patterns that appear across multiple meetings rather than one-off observations
- Be specific with examples but avoid excessive quoting
- Maintain objective tone; present observations rather than judgements

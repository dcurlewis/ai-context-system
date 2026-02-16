---
description: Process the oldest meeting transcript from Raw-Materials
---

Process meeting transcripts from the queue:

1. List files in `Raw-Materials/Meeting-Transcripts/`
2. Identify the OLDEST file by date (ascending order)
3. Read ONLY that single file
4. Count the number of participants in the meeting
5. Assess meeting substance level (see Proportionality Principle below)
6. Process and write the summary using the appropriate template
7. Archive the processed transcript
8. STOP — do not process multiple files

## Configuration

Read `config.yaml` for user identity, team, stakeholders, and communication style.

## Proportionality Principle

**Scale summary depth to match meeting substance.** Not every meeting warrants full analytical treatment.

Assess the meeting and classify as:

- **Light** (under 15 mins OR routine check-in with no significant decisions): Use Minimal Template
- **Standard** (15-45 mins with some decisions or notable discussion): Use Standard Template
- **Substantive** (over 45 mins OR strategic content, significant decisions, complex topics): Use Full Template

When in doubt, err toward the lighter template. A concise summary that captures essentials is more valuable than exhaustive documentation of routine conversation.

## Meeting Type Classification

Determine the output subdirectory based on participant count:

- **2 participants** → `Curated-Context/Meeting-Insights/One-on-ones/`
- **3+ participants** → `Curated-Context/Meeting-Insights/`

## Context Integration

Before summarising, scan recent meeting summaries from past 2 weeks in `Curated-Context/Meeting-Insights/` (including subdirectories) for:

- Recurring topics that relate to this meeting
- Follow-ups on previously discussed items

Only incorporate cross-references if they add genuine value. Don't force connections.

## Balanced Reporting

- **Foundation**: Report what was explicitly stated
- **NO dramatic descriptors** (crisis, critical, urgent) unless directly quoted
- **Attribute assessments**: "Person described this as urgent" NOT "This is urgent"
- **Avoid redundancy**: Each fact should appear once, in the most appropriate section

---

## Minimal Template (Light meetings)

Use for brief check-ins, status updates, routine 1-on-1s with no significant decisions.

**Target length**: Under 60 lines

```
# [Meeting Title]

**Date**: [Date]
**Participants**: [[Names]]
**Duration**: ~[X] minutes

---

## Summary

[2-4 paragraphs covering what was discussed, any decisions made, and action items. Write in prose, not bullets, unless listing distinct items.]

---

## Decisions

- [Decision 1 — if any]

## Action Items

- [Item 1 — if any]

---

## Notable Quote

> "[One quote that captures the key point — if warranted]"
```

---

## Standard Template (Most meetings)

Use for typical working meetings with some substance.

**Target length**: 80-120 lines

```
# [Meeting Title]

**Date**: [Date]
**Participants**: [[Names]]
**Duration**: ~[X] minutes
**Context**: [One line of context if helpful]

---

## Key Topics Discussed

### 1. [Topic]

[Concise summary of discussion and outcome]

### 2. [Topic]

[Concise summary of discussion and outcome]

---

## Decisions

- [Decision with decision-maker noted]

---

## Action Items

- [Item with deadline if mentioned]

---

## Direct Quotes

> "[Quote 1]"

> "[Quote 2 — if warranted]"

---

## Context Notes

[Only if genuine cross-references to recent meetings exist. Otherwise omit this section entirely.]
```

---

## Full Template (Substantive meetings)

Use for strategic discussions, complex multi-topic meetings, or meetings with significant decisions.

**Target length**: 120-180 lines

```
# [Meeting Title]

**Date**: [Date]
**Participants**: [[Names]]
**Duration**: ~[X] minutes
**Context**: [Brief context]

---

## Key Topics Discussed

### 1. [Topic]

[Summary with relevant detail]

### 2. [Topic]

[Summary with relevant detail]

---

## Decisions

- [Decision with decision-maker and rationale if stated]

---

## Action Items

- [Item with deadline if mentioned]

---

## Direct Quotes

> "[Quote 1]"

> "[Quote 2]"

> "[Quote 3 — if warranted]"

---

## Context Notes

[Cross-references to recent related discussions where patterns genuinely exist]

---

## Meeting Analysis

[Include for all Full-template meetings. See Meeting Analysis Sections below.]
```

---

## Meeting Analysis Sections

**Include a `## Meeting Analysis` section for any meeting with an estimated duration of ~10 minutes or longer**, regardless of which template is used. Only omit it for very short meetings (under ~10 minutes).

The depth of the analysis should scale with the template:

### For Minimal and Standard templates

Include under `## Meeting Analysis`:

- **Insights**: 1-2 brief observations about patterns, implications, or connections to broader context. Grounded in facts, not speculation.
- **Personal Communication Feedback** (optional subsection): Include if the user's communication style had any observable impact worth noting. Keep to 1-2 specific observations. Omit if nothing notable.

### For Full template

Include under `## Meeting Analysis`:

- **Insights**: 1-2 professional observations about patterns or implications, grounded in facts. Not speculation or extrapolation.
- **Personal Communication Feedback**: 2-3 specific observations about the user's communication style and its impact. Keep factual and actionable.

---

## Wikilinks

Apply Obsidian wikilinks to the output file per `Guidelines/wikilink-guidelines.md`.

## What NOT to Include

- **Awareness Items as a separate section**: Integrate into Key Topics or omit
- **Redundant facts**: Don't repeat the same information across multiple sections
- **Exhaustive quotes**: 1-3 quotes maximum, choose the most telling
- **Forced context connections**: Only cross-reference if genuinely relevant
- **Meeting Analysis for very short meetings**: Only omit for meetings under ~10 minutes
- **Speculation or extrapolation**: Stick to what was actually discussed

---

## Output

1. **Determine output path** based on participant count:

   - 2 participants → `Curated-Context/Meeting-Insights/One-on-ones/`
   - 3+ participants → `Curated-Context/Meeting-Insights/`

2. Create summary file using naming format `[YYYYMMDD]-Meeting-Title.md`

3. Archive the processed transcript: move from `Raw-Materials/Meeting-Transcripts/` to `Archive/Raw-Materials/Meeting-Transcripts/`

4. Report to the user:

   - Participant count and selected output location
   - Template used (Minimal/Standard/Full) and why
   - A very brief summary of the meeting (2-3 sentences at most)
   - Whether there are more files to process

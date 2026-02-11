# Interview Preparation

Generate comprehensive interview preparation context — for conducting or participating in interviews.

## Instructions

1. Read `config.yaml` for user identity, role, company, and communication style
2. Read `Memory/memory-index.md` for relevant context
3. Ask the user:
   - **What kind of interview?** (Conducting / Being interviewed)
   - **For what role?** (Role title and level)
   - **Who with?** (Interviewer or candidate name, if known)
   - **Any specific focus areas?**
4. Generate preparation materials

## Mode A: Conducting an Interview

When the user is interviewing a candidate:

### Context Gathering
- Check `Curated-Context/Interview-Context/` for existing prep materials
- Check `Curated-Context/People/` if this is a known person (internal transfer, return candidate)
- Review the role requirements from the user's team context in `config.yaml`

### Output

```markdown
# Interview Prep — {Candidate Name} for {Role}

**Date**: {Date}
**Interviewer**: {User name from config.yaml}
**Candidate**: {Name}
**Role**: {Role title}
**Focus area**: {What this interview should assess}

## Role Context
{Brief overview of the role, the team's needs, and what good looks like}

## Suggested Questions

### Technical / Role-Specific
1. {Question} — *Looking for: {What a good answer demonstrates}*
2. {Question} — *Looking for: {What a good answer demonstrates}*

### Behavioural
1. {Question} — *Looking for: {Desired competency}*
2. {Question} — *Looking for: {Desired competency}*

### Culture & Values
1. {Question} — *Looking for: {Cultural alignment signal}*

### Candidate's Questions
{Be prepared for questions about:}
- {Topic they'll likely ask about}
- {Topic they'll likely ask about}

## Red Flags to Watch For
- {Warning sign}
- {Warning sign}

## Scorecard
| Dimension | Rating (1-5) | Notes |
|-----------|-------------|-------|
| Technical ability | | |
| Communication | | |
| Problem solving | | |
| Culture fit | | |
| Growth potential | | |

## After the Interview
- Save notes to `Curated-Context/Interview-Context/YYYYMMDD-Interview-{Candidate}.md`
- If strong candidate, note in memory for future reference
```

## Mode B: Being Interviewed

When the user is the one being interviewed:

### Context Gathering
- Read `Curated-Context/Professional-Development/` for achievements and brag docs
- Read `Memory/memory-projects.md` for project examples
- Read `Memory/memory-decisions.md` for decision examples
- Check `Curated-Context/People/` if the interviewer is known

### Output

```markdown
# Interview Prep — {Role/Company}

**Date**: {Date}
**Role**: {What you're interviewing for}
**Company**: {Where}
**Interviewer**: {Name if known}

## Your Story
{2-3 paragraph narrative arc — who you are, your experience, why this role}

## Key Achievements to Reference
| Achievement | Impact | STAR Framework |
|------------|--------|---------------|
| {What you did} | {Measurable impact} | {Situation → Task → Action → Result} |

## Likely Questions & Your Answers

### "Tell me about yourself"
{Prepared 2-minute pitch}

### "Why this role?"
{Prepared answer}

### "Tell me about a challenging project"
{Prepared STAR answer drawing from memory}

### "Tell me about a difficult decision"
{Prepared answer from memory-decisions.md}

### "How do you handle conflict?"
{Prepared answer with real examples}

## Questions to Ask Them
1. {Smart question showing research}
2. {Question about the role/team}
3. {Question about growth/culture}

## Research Notes
{What to research about the company/role before the interview}

## Logistics
- {What to bring/prepare}
- {Dress code}
- {Arrive by}
```

## Save Location
`Curated-Context/Interview-Context/YYYYMMDD-Interview-Prep-{Description}.md`

## Notes
- For "Being Interviewed" mode, draw heavily from existing memory and curated context to make answers specific and authentic
- For "Conducting" mode, tailor questions to the user's team culture and actual needs
- Apply communication style from `config.yaml`
- Interview prep is time-sensitive — focus on practical, usable content

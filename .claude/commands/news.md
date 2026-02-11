# Generate News Digest

Create a curated news digest from RSS feeds relevant to the user's interests and industry.

## Instructions

1. Read `config.yaml` for user identity, industry context, and news preferences
2. Read the `news` section of config for RSS feeds and interests
3. Check `Synced-Data/News/` for fetched RSS data
4. Process into a curated digest

## Prerequisites

This command works best when RSS data has been fetched:
```bash
python Scripts/News/fetch_rss.py
```

If no fetched data exists in `Synced-Data/News/`, inform the user and offer to work with any news content they paste directly.

## Processing Steps

### 1. Gather Raw News
- Read all recent files in `Synced-Data/News/`
- Parse article titles, summaries, sources, and dates

### 2. Filter & Prioritise
Using the `news.interests` from `config.yaml`, score articles by relevance:
- **High**: Directly relevant to user's industry, role, or active projects
- **Medium**: Related to broader interests or adjacent topics
- **Low**: Tangentially relevant
- **Skip**: Not relevant

### 3. Contextualise
For high-relevance articles, add context:
- How does this relate to the user's work?
- Does it affect any active projects?
- Is this something to discuss with the team?
- Does it validate or challenge any current decisions?

### 4. Generate Digest

## Output

### Save Location
`Curated-Context/News-Digests/YYYYMMDD-news-digest.md`

### Output Template

```markdown
# News Digest — {Date}

**Prepared for**: {Name from config.yaml}
**Industry**: {Industry from config.yaml}

## Top Stories

### {Article Title}
**Source**: {Publication} | **Date**: {Date}
**Relevance**: {High/Medium}

{2-3 sentence summary}

**Why it matters to you**: {Contextual relevance to the user's work}

---

### {Article Title}
**Source**: {Publication} | **Date**: {Date}
**Relevance**: {High/Medium}

{2-3 sentence summary}

**Why it matters to you**: {Contextual relevance}

---

## Quick Hits
- **{Title}** ({Source}): {One-line summary}
- **{Title}** ({Source}): {One-line summary}

## Trends to Watch
{2-3 sentences on emerging patterns across the news that are relevant to the user}

## Conversation Starters
{1-2 items that would make good discussion points in meetings or with the team}
```

### HTML Output (Optional)

If `Guidelines/news-digest-template.html` exists, also generate an HTML version for email-friendly distribution. Save to the same location with `.html` extension.

## Notes
- Quality over quantity — 5 well-contextualised articles beat 20 summaries
- The "Why it matters to you" section is what makes this valuable vs. a generic RSS reader
- Interests in `config.yaml` guide filtering but don't limit it — use judgement
- If no RSS data is available, the command can work with pasted articles or URLs

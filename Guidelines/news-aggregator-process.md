# News Aggregator Process

## Overview
This document defines the weekly news aggregation process, focusing on developments relevant to the user's role, engineering management, and their regional tech ecosystem. Read `config.yaml` for the user's specific role, company, and interests.

## News Sources

### Primary Sources (Check All)
1. **Hacker News** - https://news.ycombinator.com
   - Review top 30 stories from the past week
   - Check comments on AI/platform/infrastructure stories for interesting perspectives
   - Note any discussions about your company or competitors

2. **The Information AI** - https://www.theinformation.com/technology/artificial-intelligence
   - Focus on AI vendor movements, pricing changes, and strategic shifts
   - Pay attention to enterprise AI adoption patterns
   - Note any coverage of Anthropic, OpenAI, Google AI developments

3. **Techmeme** - https://techmeme.com
   - Review main stories from past 7 days
   - Follow links to original sources for major AI/platform announcements
   - Check "Earlier Picks" for stories that gained momentum

4. **Import AI** - https://jack-clark.net or https://importai.substack.com
   - Read the latest weekly edition in full
   - Focus on strategic implications sections
   - Note any mentions of evaluation, inference optimization, or platform trends

Users should add their own regional and industry-specific sources as appropriate.

## Aggregation Process

### Step 1: Collection
- Use web_search and web_fetch to access each source
- For Hacker News, check both front page and "Show HN" for relevant tools/projects
- For paywalled content, note the headline and attempt to find alternative coverage

### Step 2: Filtering for Relevance
Prioritise stories that relate to:
- **Direct work relevance**: Topics aligned with the user's role and team focus (from `config.yaml`)
- **Vendor ecosystem**: Key vendors and partners relevant to the user's work
- **Competitive landscape**: Competitors in the user's industry
- **Management insights**: Engineering leadership, team scaling, platform teams
- **Regional context**: Local tech scene, company mentions, regional business climate
- **Emerging patterns**: New capabilities, shifts in development practices

### Step 3: Summary Structure

Create a markdown document with the following sections:

```markdown
# Weekly News Summary - [Date Range]

## Executive Summary
[2-3 sentence overview of the most significant developments]

## AI & ML Developments
[Focus on technical advances, vendor updates, and industry shifts]
- **Highlight**: [Most important story] ([Source](URL))
- [Other significant developments] ([Source](URL))

## Platform & Infrastructure
[DevOps, MLOps, cloud infrastructure, platform engineering patterns]
- [Relevant updates] ([Source](URL))

## Competitive & Industry Intelligence  
[Competitors, industry space, enterprise adoption]
- [Key movements] ([Source](URL))

## Regional Tech Ecosystem
[Local tech news, startup activity, regional developments]
- [Notable stories] ([Source](URL))

## Engineering Leadership Insights
[Team management, scaling challenges, industry best practices]
- [Relevant articles or discussions] ([Source](URL))

## Worth Noting
[Interesting but lower priority items that might spark ideas or conversations]
- [Brief mentions] ([Source](URL))

## Sources Referenced
[Comprehensive list of all articles/links reviewed for this summary with full URLs]
```

#### URL Formatting Guidelines
- Include inline source links for EVERY news item using markdown format: `([Source Name](URL))`
- Use the actual article URL, not the aggregator URL where possible
- For paywalled content, include the URL anyway and note if paywalled: `([The Information - paywalled](URL))`
- If multiple sources cover the same story, include the most authoritative or accessible one
- In the "Sources Referenced" section, provide a comprehensive list of all URLs consulted

### Step 4: Contextualization
For each item, briefly note why it's relevant to the user's context:
- How it might impact their team's strategy
- Relevance to current initiatives (from memory files)
- Potential discussion points for team meetings
- Vendor relationship implications

### Example News Item Format
```markdown
- **Meta's massive infrastructure bet**: Planning $66-72B capital expenditure in 2025, up ~$30B year-over-year, building titan clusters including Prometheus (1GW) and Hyperion (5GW potential) ([TechCrunch](https://techcrunch.com/2025/07/30/meta-ai-infrastructure/))
```

## Quality Guidelines

1. **Brevity**: Each item should be 2-4 sentences max unless it's particularly significant
2. **Relevance**: Every item should have clear connection to the user's role or interests
3. **Actionability**: Where possible, note if something requires action or awareness
4. **Balance**: Don't over-index on any one source or topic area
5. **Accuracy**: Verify major claims by checking multiple sources when available
6. **Tone**: Professional but conversational, similar to a well-informed colleague's briefing
7. **Source Attribution**: ALWAYS include clickable URLs for every news item so the user can easily read the full story
8. **URL Quality**: Prefer direct article links over aggregator links; use stable URLs that won't expire quickly

## Update Frequency

This process is run weekly by cron job, on a Monday morning, to capture the previous week's developments.

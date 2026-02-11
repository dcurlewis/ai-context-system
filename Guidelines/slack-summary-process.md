# Slack Channel Summary Process Guide

## Overview

This document outlines the weekly process for extracting valuable context from Slack channels to supplement our memory system with information not captured in meetings or formal documentation.

## Process Schedule

**When**: Weekly
**Output**: Single summary file `[YYYYMMDD]-slack-summary.md`  
**Location**: `Curated-Context/Team-Communications/`

## Channels to Export

Configure the channels relevant to your role and team. Consider organising them into tiers by priority:

### Tier 1: Priority Channels (Export Weekly)

These are the channels you monitor most closely. Typically includes:
- Your **team's private channel** — internal discussions, technical blockers, team energy indicators
- **Leadership channels** — strategic decisions, coordination challenges, initiative planning
- **Key DMs with your manager and key stakeholders** — strategic direction, personnel decisions
- **Support/help channels** — demand signals, recurring pain points, customer sentiment

### Tier 2: Regular Channels (Export Weekly or Bi-weekly)

Channels you check regularly but are less critical:
- **DMs with direct reports** — team capacity, project progress, boundary questions
- **DMs with peers** — process coordination, strategy discussions
- **Cross-team coordination channels** — broader organisational context
- **Supergroup/department channels** — announcements, culture signals

### Tier 3: Project and Situational Channels (Export As Needed)

Channels that are relevant during specific periods:
- **Project-specific channels** — development progress, cross-team integration
- **Temporary channels** — incident response, time-bound initiatives
- **External-facing channels** — vendor interactions, partner coordination

Project channels will evolve over time. Some may become inactive, others may appear. The `/slack` command should handle ad-hoc additions gracefully.

## Export Files

- Slack channel export files will be provided with the following naming convention: `[YYYYMMDD]-[HHmm]-[ChannelName].md`

## Summary Creation Process

### Step 1: Check Previous Summary
- Read the most recent slack summary file in `Curated-Context/Team-Communications/`
- Note the date range it covers to identify any overlap with the current period
- If there is overlap, avoid capturing the same information again in this summary

### Step 2: Read All Export Files
- Read all attached `.md` files (or Slack channel data retrieved via MCP tools) for the week
- Note which channels had significant activity

### Step 3: Extract Key Information

Focus on identifying:

**Strategic & Decisions**
- Decisions made outside of meetings
- Strategic pivots or changes
- Vendor negotiations or concerns
- Resource allocation decisions

**Technical & Implementation**
- Technical blockers or workarounds
- Performance issues or outages
- Architecture decisions or debates
- Implementation gaps between plan and reality

**People & Culture**
- Team morale indicators (frustration, humor, energy)
- Personnel movements or concerns
- Health/availability impacts
- Shadow work patterns (who's actually doing what)

**Process & Coordination**
- Process breakdowns or friction
- Cross-team dependencies
- Communication gaps or delays
- Escalation patterns

**External Relationships**
- Vendor interactions
- Cross-functional challenges
- Stakeholder concerns
- Integration issues

### Step 4: Structure the Summary

Create `[YYYYMMDD]-slack-summary.md` with this structure:

```markdown
# Slack Channel Summary - Week of [Date Range]

## Executive Summary
[2-3 sentences capturing the most critical findings]

## Strategic Developments
[Decisions, initiatives, or changes not captured in meetings]

## Technical Insights
[Implementation details, blockers, architectural decisions]

## Team Dynamics
[Morale indicators, personnel changes, workload patterns]

## Process Observations
[What's working, what's not, shadow work patterns]

## External Interactions
[Vendor, stakeholder, or cross-functional notable events]

## Gap Analysis
[What leadership thinks is happening vs. reality]

## Items for Memory Update
[Specific items that should be incorporated into memory files]
```

## What Makes Good Summary Content

### Include:
- Decisions made in DMs that affect the team
- Technical issues discussed before they escalate
- Morale indicators (both positive and concerning)
- Process workarounds revealing systemic issues
- Personnel concerns mentioned informally
- Vendor relationship dynamics
- Shadow work patterns

### Exclude:
- Routine coordination messages
- Already documented decisions
- Personal information unrelated to work impact
- Speculation without substance
- Minor technical discussions resolved quickly

## Quality Checklist

Before finalizing the summary:
- [ ] Captures implementation reality vs. leadership perception?
- [ ] Identifies shadow work and actual ownership?
- [ ] Notes morale and energy indicators?
- [ ] Highlights process friction points?
- [ ] Reveals technical debt or blockers?
- [ ] Shows relationship dynamics?
- [ ] Avoids unnecessary personal details?
- [ ] Provides actionable intelligence for memory updates?

## Integration with Memory System

This weekly summary serves as a key input to the memory update process by:
1. Providing ground truth on implementation
2. Capturing informal decision rationales
3. Revealing team dynamics not visible in meetings
4. Identifying emerging issues before escalation
5. Tracking shadow work and actual ownership
6. Monitoring relationship health

This investment provides early warning on issues and captures valuable context that would otherwise be lost.

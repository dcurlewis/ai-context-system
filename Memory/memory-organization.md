# Memory Organisation

> How the memory system is structured and where information lives.

**Last reviewed**: 2026-01-01

---

## Architecture

### Memory Files (this directory)
Persistent, evolving system memory. These are the long-term brain — updated incrementally, never wiped.

- **memory-index.md** — Master index and activity log
- **memory-organization.md** — This file — structural documentation
- **memory-strategy.md** — Processing priorities and retention rules
- **memory-projects.md** — Active project tracking
- **memory-decisions.md** — Decision log
- **memory-team-dynamics.md** — Team health and interpersonal dynamics
- **memory-relationships.md** — Stakeholder relationship map

### Curated Context
Processed, structured knowledge in `Curated-Context/`. Organised by type:
- **Project-Insights/** — Meeting insights, organised by topic and 1:1s
- **People/** — Individual person profiles
- **Team-Knowledge/** — Team-level context and Slack summaries
- **Strategic-Documents/** — Strategy docs and planning materials
- **Daily-Journals/** — Day-by-day activity and observations
- **Professional-Development/** — Achievement tracking
- And 10 additional specialised directories

### Raw Materials
Unprocessed inputs in `Raw-Materials/`. Source-of-truth originals.
- **Meeting-Transcripts/** — Raw transcripts
- **Docs/** — Documents awaiting processing
- **Slack/** — Slack exports

---

## Information Flow

```
Raw Materials → (slash command) → Curated Context → (promotion) → Memory
```

1. Content enters as Raw Materials
2. Slash commands (`/meeting`, `/doc`, `/slack`) process it into Curated Context
3. Key insights get promoted to Memory via `/memory-promote` or `/memory-update`
4. Memory is periodically consolidated via `/memory-consolidate`

---

## Naming Conventions

- **Memory files**: `memory-{topic}.md` (lowercase, hyphenated)
- **Curated Context**: `YYYYMMDD-Descriptive-Title.md` (date prefix, title case, hyphenated)
- **Raw Materials**: `YYYYMMDD-description.ext` (date prefix, lowercase)

---

## Maintenance Schedule

| Task | Frequency | Command |
|------|-----------|---------|
| Scan for new content | Weekly | `/memory-scan` |
| Update from recent activity | After processing sessions | `/memory-update` |
| Validate consistency | Weekly | `/memory-validate` |
| Consolidate bloated files | Monthly | `/memory-consolidate` |
| Review strategy | Quarterly | `/memory-strategy` |
| Full organisation review | Quarterly | `/memory-org` |

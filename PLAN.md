# AI Context System - Build Plan

> **This file is the build plan for constructing the public version of a personal AI Context system.**
> It should be read at the start of each working session to understand what has been done and what comes next.
> Delete this file before making the repo public.

## Project Context

This project is a **clean-room rebuild** of a private AI-powered knowledge management system. The original system helps a user manage their professional context (meetings, documents, decisions, team dynamics) through Claude Code / Cursor slash commands, a structured memory pipeline, and Obsidian integration.

The goal is to make a **fully functional, publicly shareable version** that:
- Is configurable via `config.yaml` (users fill in their own identity, company, team)
- Ships with a Star Wars-themed demo persona (Darth Vader, COO of the Death Star) as entertaining sample data
- Contains **zero** confidential or personal information from the original system
- Can be cloned and used immediately by anyone

## Architecture: How Configuration Works

Rather than fragile template substitution, `CLAUDE.md` and commands include an instruction like:

```
Read config.yaml for user identity, company context, and team structure.
Use these values throughout all processing.
```

This is natural for how Claude operates - it already reads files for context. The `config.example.yaml` ships with the Star Wars demo persona.

## Current Status

- [x] Directory structure created
- [x] `.gitignore` created
- [ ] **Phase 1**: Foundation - config.example.yaml, CLAUDE.md, README.md, setup.sh
- [ ] **Phase 2**: All 24 slash commands (generalized)
- [ ] **Phase 3**: 6 guideline files (Star Wars-themed examples)
- [ ] **Phase 4**: Scripts and Sync infrastructure
- [ ] **Phase 5**: Star Wars sample data (Memory files, Curated-Context examples, sample transcript)
- [ ] **Phase 6**: Safety tooling (sensitive term scanner, pre-commit hooks, CI)
- [ ] **Phase 7**: Polish (CONTRIBUTING.md, LICENSE, Obsidian config, final review)

---

## Phase 1: Foundation

Create the core configuration and system files.

### config.example.yaml

Star Wars demo persona:

```yaml
user:
  name: "Darth Vader"
  role: "Chief Operating Officer"
  email: "vader@deathstar.empire.gov"
  timezone: "Galactic/Coruscant"
  location: "Death Star I, Outer Rim"

company:
  name: "Galactic Empire - Death Star Operations"
  jira_url: "https://empire.atlassian.net"

team:
  name: "Death Star Operations"
  members:
    - name: "Grand Moff Tarkin"
      role: "Station Commander / CEO"
    - name: "Admiral Piett"
      role: "VP Naval Operations"
    - name: "General Veers"
      role: "Director of Ground Forces"
    - name: "Moff Jerjerrod"
      role: "Engineering Lead"
    - name: "Captain Needa"
      role: "Senior Fleet Captain"

communication_style:
  spelling: "british"  # The Empire is very proper
  formality: "imperial"
```

### CLAUDE.md

Rewrite from scratch. Key principles:
- All user identity references point to `config.yaml`
- No hardcoded names, companies, emails, timezones, or paths
- Keep the full memory system, directory structure, file naming conventions, Obsidian integration
- Keep the processing workflow (Raw Materials -> Curated Context -> Memory)
- Keep communication style guidelines but make them configurable
- Remove any transcription corrections section
- Remove any company-specific tool references

### README.md

Public-facing documentation:
- What is this system and why does it exist
- Quick start guide (clone, edit config.yaml, start using)
- Architecture overview with diagram
- Command reference
- How the memory pipeline works
- Obsidian integration
- Contributing section

### setup.sh

Simple script:
- Copies `config.example.yaml` to `config.yaml` if it doesn't exist
- Creates any directories not tracked by git
- Prints next steps

---

## Phase 2: Slash Commands (24 total)

All commands live in `.claude/commands/`. Each needs these systematic changes:
- "David" / "David's" -> "the user" or reference config.yaml
- Company/team names -> reference config.yaml
- Hardcoded paths -> relative paths
- People names -> generic references
- Timezone references -> config.yaml
- Email references -> config.yaml

### Commands by effort level:

**Minimal changes needed:**
- backup.md, help.md, doc.md, prep.md, thought.md
- All memory-* commands (memory-scan, memory-org, memory-strategy, memory-projects, memory-decisions, memory-team, memory-relationships, memory-consolidate, memory-validate, memory-promote, memory-update)

**Moderate changes:**
- meeting.md, slack.md, delivery.md, news.md, interview.md

**Significant rework:**
- morning.md (day-specific tasks, calendar script, timezone)
- brag.md (achievement log personalisation)
- meeting-analysis.md (personal communication feedback)

---

## Phase 3: Guidelines (6 files)

- memory-consolidation-guidelines.md - Already largely generic
- wikilink-guidelines.md - Replace all names with Star Wars examples
- slack-summary-process.md - Replace channel names with generic examples
- monday-update-generation-guidelines.md - Replace name examples, generalise
- news-aggregator-process.md - Already mostly generic
- news-digest-template.html - Already generic HTML template

**Excluded:** slack-help-summary.md (too bespoke)

---

## Phase 4: Scripts and Sync

- Scripts/calendar-today.py - Remove hardcoded email, keep functionality
- Scripts/News/fetch_rss.py - Already generic
- Scripts/News/requirements.txt - As-is
- Sync/sync_jira.py - Remove hardcoded URLs
- Sync/utils.py - Already generic
- Sync/config.example.json - Imperial Jira keys (DS-001, IMP-42)
- Sync/.env.example - Already generic
- Sync/README.md - Rewrite for public audience

---

## Phase 5: Star Wars Sample Data

### The Cast

- **Darth Vader** (the user) - COO of Death Star Operations, reports to Emperor Palpatine
- **Grand Moff Tarkin** - Station Commander / CEO, Vader's peer
- **Admiral Piett** - VP Naval Operations (nervous, eager to please)
- **General Veers** - Director of Ground Forces (competent, reliable)
- **Moff Jerjerrod** - Engineering Lead, Death Star II (behind schedule)
- **Colonel Yularen** - Head of Imperial Security Bureau
- **Captain Needa** - Senior Fleet Captain (apologetic about failures)
- **Dr. Bevel Lemelisk** - Chief Architect, thermal exhaust port designer
- **Stormtrooper Commander TK-421** - Training Division Lead

### The Teams

- **Death Star Engineering** - Thermal exhaust port "definitely isn't a design flaw"
- **Stormtrooper Training Division** - 3.7% accuracy rate, new simulator procurement
- **Imperial Navy Operations** - Fleet coordination, Rebel pursuit
- **Sith Leadership** - Emperor's strategic vision

### Memory Files (Memory/)

- memory-index.md, memory-organization.md, memory-strategy.md, memory-projects.md, memory-decisions.md, memory-team-dynamics.md, memory-relationships.md

### Curated-Context Examples

- Meeting-Insights/20260101-Death-Star-Engineering-Review.md
- Meeting-Insights/One-on-ones/20260103-One-on-One-Admiral-Piett.md
- Decision-History/20260105-Stormtrooper-Training-Vendor-Selection.md
- Team-Communications/20260107-slack-summary.md

### Sample Raw Material

- Raw-Materials/Meeting-Transcripts/20260110-imperial-briefing.txt

---

## Phase 6: Safety

**CRITICAL: This project must contain zero confidential information.**

### Sensitive term scanner (safety/check-sensitive.sh)

Scans all project files for known sensitive patterns. The sensitive-patterns.txt should contain patterns specific to the original author's context that must never appear.

### Pre-commit hook

Runs the scanner on every commit. Any match = blocked commit.

### GitHub Actions CI

Runs scanner on every PR.

### Manual review checklist

Before making public:
- [ ] No real names of people
- [ ] No company names or domains
- [ ] No team/project/vendor names from original
- [ ] No Jira keys or Slack channels from original
- [ ] No absolute paths containing usernames
- [ ] No real email addresses
- [ ] No location/timezone that identifies the original author
- [ ] No internal URLs or documentation references
- [ ] No references to specific roles that could identify the person

---

## Phase 7: Polish

- CONTRIBUTING.md
- LICENSE (MIT)
- Obsidian vault configuration
- Blog-ready documentation
- Final multi-pass review

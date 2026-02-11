# AI Context Management System Guide

## Overview

This document explains the AI Context long-term memory system. The system uses file-based storage organised into curated directories, with modular memory files providing indexed summaries for efficient retrieval.

## Base Directory

All paths are relative to the project root directory. Set your own project root path when using this with Claude Desktop.

## Directory Structure

```text
.
├── Curated-Context/      # Processed and structured information ("Long term memory")
│   ├── Decision-History/       # Also opened as an Obsidian vault for browsing
│   ├── Professional-Development/
│   ├── Interview-Context/
│   ├── Meeting-Insights/
│   ├── News-Digests/
│   ├── Organizational-Context/
│   ├── People/
│   ├── Professional-Philosophies/
│   ├── Project-Insights/
│   ├── Projects/
│   ├── Strategic-Documents/
│   ├── Team-Communications/
│   ├── Team-Knowledge/
│   ├── Teams/
│   ├── Technical-Documentation/
│   ├── Vendors/
│   ├── Daily-Journals/         # Personal journal entries (excluded from memory scans)
│   └── Obsidian-Specific-Dirs/ # Templates, attachments (excluded from memory scans)
├── Memory/               # Aggregated "medium-term memory", summaries for indexed retrieval
├── Prompts/              # Project prompts and system instructions (this directory)
├── Synced-Data/Jira/     # Auto-synced Jira data
└── Archive/              # Archived files (mirrors main directory structure)
```

## Memory System

### Memory Files

Located in `Memory/`:

| File | Contains |
|------|----------|
| `memory-index.md` | Central index, last update summary, quick reference |
| `memory-organization.md` | Team structure, roles, leadership, reporting |
| `memory-strategy.md` | Company goals, vision, strategic initiatives |
| `memory-projects.md` | Current projects, timelines, status |
| `memory-decisions.md` | Important decisions, issues, approaches |
| `memory-team-dynamics.md` | Team interactions, communication patterns |
| `memory-relationships.md` | Cross-functional partners, stakeholders |

### Quick Reference - What to Read When

**For queries about:**

- People, roles, teams → `Memory/memory-organization.md`
- Company direction, goals, tech choices → `Memory/memory-strategy.md`
- Current work, project status → `Memory/memory-projects.md`
- Past decisions, why we chose X → `Memory/memory-decisions.md`
- Communication, team dynamics → `Memory/memory-team-dynamics.md`
- Stakeholders, partnerships → `Memory/memory-relationships.md`

### Status Markers

Memory files use standard status markers:

- `[IMPLEMENTED]`, `[IN PROGRESS]`, `[PENDING]`, `[BLOCKED]` - for decisions
- `[ACTIVE]`, `[PLANNED]`, `[COMPLETED]`, `[ON HOLD]` - for projects
- `[CURRENT]`, `[DEPARTING]`, `[DEPARTED]` - for people

## File Naming Convention

All curated files follow a strict naming convention:

- Format: `[YYYYMMDD]-Descriptive-Title.md`
- Example: `20250508-Team-Retrospective-Insights.md`

## Synced Jira Data

Located in `Synced-Data/Jira/`:

### Directory Structure

```text
Synced-Data/Jira/
├── INDEX.md          # Human-readable hierarchy overview (start here)
├── index.json        # Compact programmatic index with all issues
├── _meta.json        # Sync metadata and timestamps
└── issues/           # Individual issue JSON files with full details
    ├── PROJ-001.json
    ├── PROJ-002.json
    └── ...
```

### How to Use Jira Data

**Tiered access pattern - avoid loading all files at once:**

1. **Start with INDEX.md** for overview queries
   - Provides a browseable hierarchy organised by level
   - Grouped by status (To Do, In Progress, Done)
   - Shows issue key, summary, status, and assignee at a glance

2. **Use index.json for filtering/querying**
   - Compact JSON (~25KB for 150+ issues)
   - Contains: key, summary, level, status, status_category, parent
   - Good for: "Find all issues under PROJ-1 that are In Progress"

3. **Drill into specific issues/{KEY}.json when you need details**
   - Full issue data including description, comments, dates, and links
   - Only load individual files when specific detail is needed

### Issue Hierarchy Levels

| Level | Contains | Example |
|-------|----------|---------|
| 0 | Root Company Goals | PROJ-1, PROJ-2 |
| 1 | Team Goals | TEAM-29, TEAM-30 |
| 2 | Team Goals/Milestones | TEAM-445, TEAM-582 |
| 3+ | Milestones/Epics/Tasks | Individual work items |

## Curated Context Categories

Each subdirectory in `Curated-Context/` serves a specific purpose:

| Directory | Contains |
|-----------|----------|
| `Decision-History/` | Key decisions with rationale and outcomes |
| `Professional-Development/` | Career achievements, feedback, impact evidence |
| `Interview-Context/` | Interview preparation and candidate notes |
| `Meeting-Insights/` | Processed meeting summaries |
| `News-Digests/` | Weekly AI news summaries |
| `Organizational-Context/` | Org structure, team compositions |
| `People/` | Individual person profiles |
| `Professional-Philosophies/` | Articles, books, leadership approaches |
| `Project-Insights/` | Detailed project context and learnings |
| `Projects/` | Project briefs and status |
| `Strategic-Documents/` | Planning docs, roadmaps, strategy papers |
| `Team-Communications/` | Important team announcements, updates |
| `Team-Knowledge/` | Technical knowledge, processes, standards |
| `Teams/` | Team profiles |
| `Technical-Documentation/` | Architecture, systems documentation |
| `Vendors/` | Vendor evaluations and notes |
| `Daily-Journals/` | Personal daily journal entries (excluded from memory scans) |
| `Obsidian-Specific-Dirs/` | Obsidian templates and attachments (excluded from memory scans) |

## Context Retrieval Strategy

When addressing queries:

1. First determine what context would be helpful
2. Use file tools to locate relevant context in the appropriate directories
3. Start with memory files for quick orientation
4. Drill into Curated-Context for detailed information
5. Be selective in context application; avoid information overload

This system provides structured organisation for effective context retrieval across conversations.

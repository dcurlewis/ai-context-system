# AI Context System — Help

Display a comprehensive overview of the system and all available commands.

## Instructions

1. Read `config.yaml` to greet the user by name
2. Display the following help information

## Output

### System Overview

This is your personal AI context system. It processes raw materials (meeting transcripts, documents, Slack threads) into structured knowledge, maintains a living memory, and helps you operate with full context.

**Your configuration:** Read from `config.yaml`
**Memory status:** Check if `Memory/memory-index.md` exists. If yes, report how many memory files exist. If no, note that memory hasn't been initialised yet.

### Available Commands

#### Information Processing
| Command | Purpose |
|---------|---------|
| `/meeting` | Process a meeting transcript into structured insights |
| `/meeting-analysis` | Deep analysis of communication patterns from a meeting |
| `/slack` | Process Slack threads into summaries and action items |
| `/doc` | Process a document into structured notes |
| `/news` | Generate a news digest from RSS feeds |

#### Daily Operations
| Command | Purpose |
|---------|---------|
| `/morning` | Morning briefing — calendar, priorities, context for the day |
| `/delivery` | Generate a delivery/status update |
| `/prep` | Prepare context for an upcoming meeting |
| `/brag` | Update the achievement/impact document |
| `/interview` | Generate interview preparation context |

#### Memory Management
| Command | Purpose |
|---------|---------|
| `/memory-scan` | Scan for new information to incorporate into memory |
| `/memory-org` | Review and reorganise memory structure |
| `/memory-strategy` | Update memory processing strategies |
| `/memory-projects` | Update project tracking in memory |
| `/memory-decisions` | Record or review decisions in memory |
| `/memory-team` | Update team dynamics in memory |
| `/memory-relationships` | Update relationship/stakeholder map |
| `/memory-consolidate` | Consolidate and compress memory files |
| `/memory-validate` | Validate memory consistency and fix issues |
| `/memory-promote` | Promote curated context into long-term memory |
| `/memory-update` | General memory update from recent context |

#### Utilities
| Command | Purpose |
|---------|---------|
| `/thought` | Capture a quick thought or observation |
| `/backup` | Backup the current state of memory and context |
| `/help` | Show this help (you're looking at it) |

### Quick Tips

- **First time?** Drop a meeting transcript into `Raw-Materials/Meeting-Transcripts/` and run `/meeting`
- **Morning routine:** Run `/morning` at the start of your day for a full briefing
- **Memory health:** Run `/memory-validate` periodically to check for issues
- **Before a meeting:** Run `/prep` with the meeting name for relevant context

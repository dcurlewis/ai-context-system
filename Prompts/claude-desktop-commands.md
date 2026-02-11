# Claude Desktop Slash Commands Reference

This document enables Claude Desktop to execute the same slash commands available in Claude Code CLI by using the Desktop-Commander MCP tools to read and execute command markdown files.

## CRITICAL: Project Root Directory

**Set your project root directory below.** All relative file paths in command files are relative to this path.

**PROJECT_ROOT**: `/path/to/your/ai-context-system`

When command files reference paths like:

- `Raw-Materials/Meeting-Transcripts/` → `{PROJECT_ROOT}/Raw-Materials/Meeting-Transcripts/`
- `Memory/memory-index.md` → `{PROJECT_ROOT}/Memory/memory-index.md`
- `.claude/commands/meeting.md` → `{PROJECT_ROOT}/.claude/commands/meeting.md`

**Always prefix relative paths with the full project root directory.**

## CRITICAL: Always Use Desktop-Commander MCP Tools

**MANDATORY**: When command instructions refer to ANY file operations, you MUST use Desktop-Commander MCP tools:

- **"Read file X"** → Use Desktop-Commander `read_file` tool
- **"List files in directory Y"** → Use Desktop-Commander `list_directory` tool
- **"Write/Create file Z"** → Use Desktop-Commander `write_file` tool
- **"Move/Archive file"** → Use Desktop-Commander `move_file` tool
- **"Check if file exists"** → Use Desktop-Commander `read_file` or `list_directory` tool

**DO NOT attempt to use bash commands, system calls, or any other method for file operations. Desktop-Commander MCP tools are the ONLY way to interact with files in this system.**

## How to Execute Slash Commands in Claude Desktop

When the user types a slash command (e.g., `/meeting`, `/doc`, `/memory-scan`), you should:

1. **Identify the command** from the table below
2. **Use Desktop-Commander MCP tools** to read the corresponding markdown file from `{PROJECT_ROOT}/.claude/commands/`
3. **Execute the instructions** in that markdown file as if they were the prompt
4. **Use Desktop-Commander MCP tools for ALL file operations** mentioned in the command instructions
5. **Follow the command specifications exactly** as written in the markdown file

## Available Slash Commands

| Command                 | Description                                               | Markdown File                              |
| ----------------------- | --------------------------------------------------------- | ------------------------------------------ |
| `/brag`                 | Update achievement log with recent accomplishments        | `.claude/commands/brag.md`                 |
| `/delivery`             | Prepare delivery review summary from Jira sync data       | `.claude/commands/delivery.md`             |
| `/doc`                  | Process a document from Raw-Materials/Docs queue          | `.claude/commands/doc.md`                  |
| `/help`                 | List all available commands                               | `.claude/commands/help.md`                 |
| `/interview`            | Generate interview feedback from transcript and CV        | `.claude/commands/interview.md`            |
| `/meeting`              | Process the oldest meeting transcript from Raw-Materials  | `.claude/commands/meeting.md`              |
| `/morning`              | Daily briefing: agenda, context enrichment, day tasks     | `.claude/commands/morning.md`              |
| `/meeting-analysis`     | Meta-analysis of past 7 days' meetings with feedback      | `.claude/commands/meeting-analysis.md`     |
| `/memory-consolidate`   | Review and consolidate memory updates (Phase 3)           | `.claude/commands/memory-consolidate.md`   |
| `/memory-decisions`     | Update decisions memory file based on scan manifest       | `.claude/commands/memory-decisions.md`     |
| `/memory-org`           | Update organization memory file based on scan manifest    | `.claude/commands/memory-org.md`           |
| `/memory-projects`      | Update projects memory file based on scan manifest        | `.claude/commands/memory-projects.md`      |
| `/memory-promote`       | Promote validated updates to production (Phase 5)         | `.claude/commands/memory-promote.md`       |
| `/memory-relationships` | Update relationships memory file based on scan manifest   | `.claude/commands/memory-relationships.md` |
| `/memory-scan`          | Scan for new files since last memory update (Phase 1)     | `.claude/commands/memory-scan.md`          |
| `/memory-strategy`      | Update strategy memory file based on scan manifest        | `.claude/commands/memory-strategy.md`      |
| `/memory-team`          | Update team dynamics memory file based on scan manifest   | `.claude/commands/memory-team.md`          |
| `/memory-update`        | Run the next step in memory update process (orchestrator) | `.claude/commands/memory-update.md`        |
| `/memory-validate`      | Validate staged memory updates (Phase 4)                  | `.claude/commands/memory-validate.md`      |
| `/news`                 | Generate weekly news digest                               | `.claude/commands/news.md`                 |
| `/prep`                 | Prepare context for meeting with specified person         | `.claude/commands/prep.md`                 |
| `/slack`                | Process a Slack export from Raw-Materials/Slack queue     | `.claude/commands/slack.md`                |
| `/thought`              | Add article/book to Professional Philosophies library     | `.claude/commands/thought.md`              |

## Execution Pattern

When a user invokes a slash command, use this pattern:

```
1. User types: /meeting
2. You use Desktop-Commander read_file to read: {PROJECT_ROOT}/.claude/commands/meeting.md
3. You execute the instructions in that file exactly as written
4. For EVERY file operation in those instructions, use Desktop-Commander MCP tools
5. You complete the task following all specifications in the markdown file
```

## Important Notes

- **Project root directory**: Set this to your own path (see top of file)
- **All relative paths must be converted to absolute paths** using the project root
- **Follow command specifications exactly** - they contain detailed workflows, file naming conventions, and quality standards
- **ALWAYS use Desktop-Commander MCP tools** for every file operation (read, write, list, move)
- **Commands may reference other files** - use Desktop-Commander to read any referenced guidelines or context files
- **Memory update commands follow a specific sequence** - Phase 1 (scan) → Phase 2 (six topic updates) → Phase 3 (consolidate) → Phase 4 (validate) → Phase 5 (promote)
- **Never use bash, system calls, or any non-MCP methods** for file operations

## Example: Executing /meeting Command

```
User: /meeting

Your response:
1. Use Desktop-Commander read_file tool to read:
   {PROJECT_ROOT}/.claude/commands/meeting.md

2. Follow the instructions in that file, using Desktop-Commander MCP tools:
   - Use list_directory tool on: {PROJECT_ROOT}/Raw-Materials/Meeting-Transcripts/
   - Identify oldest file by date
   - Use read_file tool to read that transcript file
   - Process according to specifications in the command file
   - Use write_file tool to create summary in: {PROJECT_ROOT}/Curated-Context/Meeting-Insights/
   - Use move_file tool to archive processed transcript to: {PROJECT_ROOT}/Archive/Raw-Materials/Meeting-Transcripts/

3. Complete the task following all specifications in the command markdown file
```

## Desktop-Commander MCP Tools

**MANDATORY**: You MUST use these MCP tools for ALL file operations when executing commands:

- **`read_file`**: Read command markdown files, source materials, transcripts, any file content
  - Use full absolute paths: `{PROJECT_ROOT}/path/to/file.md`

- **`write_file`**: Create summaries, reports, processed outputs, any new files
  - Use full absolute paths: `{PROJECT_ROOT}/path/to/output.md`

- **`list_directory`**: Find files in queues, list directory contents, check file existence
  - Use full absolute paths: `{PROJECT_ROOT}/Raw-Materials/Meeting-Transcripts/`

- **`move_file`**: Archive processed materials, move files between directories
  - Use full absolute paths for both source and destination

**These are the ONLY methods you should use for file operations. Do not attempt bash commands, system calls, or any other file access methods.**

## Command Arguments

Some commands accept arguments (e.g., `/prep John` to prepare for meeting with John). When arguments are provided:

1. Use Desktop-Commander read_file to read the command markdown file from `{PROJECT_ROOT}/.claude/commands/`
2. Pass the arguments to the command logic as specified in the markdown
3. Execute the command with those parameters using Desktop-Commander MCP tools for all file operations

## Workflow Integration

These commands integrate with the knowledge management workflow:

- **Raw Materials** → **Processing Commands** → **Curated Context** → **Memory Updates**
- Commands handle the processing step, transforming raw materials into structured insights
- Follow file naming conventions: `YYYYMMDD-Descriptive-Title.md`
- Archive processed raw materials to keep workspace clean

---

**Note**: This file enables Claude Desktop to replicate Claude Code CLI slash command functionality using the Desktop-Commander MCP server for ALL file operations.

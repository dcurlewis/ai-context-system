# Prompts

This directory contains system prompt files for use with **Claude Desktop** (with the [Desktop-Commander MCP server](https://github.com/wonderwhy-er/DesktopCommanderMCP) for filesystem access).

**Users of Claude Code don't need these files.** Claude Code reads `CLAUDE.md` and `.claude/commands/` directly.

## Files

### `ai-context-instructions.md`
System overview: directory structure, memory file reference, Jira data usage guide, curated context category descriptions. Paste this into your Claude Desktop Project's custom instructions so Claude understands the system layout.

### `claude-desktop-commands.md`
Complete command mapping for Claude Desktop using Desktop-Commander MCP. Includes the full command table, execution pattern, examples, and MCP tool usage instructions. Paste this into your Claude Desktop Project's custom instructions alongside `ai-context-instructions.md`.

**Important**: Update the `PROJECT_ROOT` path at the top of this file to point to your local clone of this repository.

### `project-instructions.md`
Project-level system prompt for a Claude Desktop Project. Defines operating principles, response framework, and engagement style. Paste this into your Claude Desktop Project's custom instructions.

### `user-instructions.md`
Communication style guide for user-level custom instructions. This applies across all Claude Desktop Projects. Customise it to match your own communication preferences, then paste it into Claude Desktop's user-level custom instructions (Settings → Custom Instructions).

## Setup

1. Create a new Claude Desktop Project
2. Paste the contents of `ai-context-instructions.md`, `claude-desktop-commands.md`, and `project-instructions.md` into the project's custom instructions
3. Paste the contents of `user-instructions.md` into your user-level custom instructions
4. Update the `PROJECT_ROOT` path in `claude-desktop-commands.md` to your local path
5. Ensure Desktop-Commander MCP server is installed and configured

## Other AI Tools

This system could work with any AI tool that has filesystem access and can read a system prompt. The primary supported tools are:

- **Claude Code** (CLI) — reads `CLAUDE.md` and `.claude/commands/` automatically
- **Claude Desktop** (with Desktop-Commander MCP) — uses the files in this directory

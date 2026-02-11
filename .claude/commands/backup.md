---
description: Backup all changes to git with auto-generated commit messages
---

Backup all changes to git and push to remote. This command handles both functional changes and content additions with appropriate commit messages.

## Process

1. **Check git status**
   - Run `git status --short` to see all changes
   - If there are no changes, inform the user and exit

2. **Categorise changes into two buckets:**

   **Functional Changes** (infrastructure/tooling):
   - `.claude/commands/` — New or modified slash commands
   - `Scripts/` — Automation scripts
   - `Sync/` — Sync scripts
   - `CLAUDE.md` — System instructions
   - `Guidelines/` — Process documentation
   - `.gitignore` — Git configuration
   - `config.example.yaml` — Configuration template
   - `setup.sh` — Setup script
   - Any other code/config files

   **Content Additions** (day-to-day content):
   - `Curated-Context/` — All subdirectories
   - `Memory/` — Memory files and updates
   - `Synced-Data/` — Synced external data
   - Any other content files

3. **Commit functional changes first (if any)**
   - Stage only functional change files: `git add [files]`
   - Generate detailed commit message describing what was added/changed:
     - List new commands by name
     - Describe script changes
     - Note guideline updates
     - Mention any other infrastructure changes
   - Commit with descriptive message

4. **Commit content additions (if any)**
   - Stage all remaining files: `git add -A`
   - Generate lightweight commit message with categories:
     - Count files by category (meetings, docs, memory, etc.)
     - Use format: "Backup: [categories]"
     - Keep it concise (1-3 lines)
   - Commit with summary message

5. **Push to remote**
   - Run `git push`
   - Handle any errors (no remote configured, auth issues, etc.)

6. **Report summary**
   - Show what was committed (number of commits, files changed)
   - Confirm push was successful
   - Display commit SHAs for reference

## Important Notes

- **NO confirmation prompts** — just execute the backup
- If there are no changes, inform the user and exit
- If only one category of changes exists, only create one commit
- Apply spelling conventions from `config.yaml` to commit messages
- If push fails because no remote is configured, still report the local commits as successful

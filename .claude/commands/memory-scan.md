---
description: Scan for new files since last memory update (Phase 1 of 5)
---

Scan the `Curated-Context/` directory for new files since the last memory update.

## Process

1. Read `config.yaml` for user identity and context
2. Read `Memory/memory-index.md` to find the last update date
3. List all subdirectories in `Curated-Context/`
4. **Exclude the following directories from scanning:**
   - `.obsidian/` (Obsidian system directory)
   - `Obsidian-Specific-Dirs/` (Obsidian configuration, templates, attachments)
   - `Daily-Journals/` (personal scratchpad entries, processed separately)
   - `Blog/` (blog post drafts, not memory content)
5. Filter for files with dates on or after the last-updated date
6. Note any dramatic language in source files to be filtered during consolidation
7. Flag factual claims that need source verification
8. Identify opinion statements to be excluded from consolidation

## Output

Create a new dated directory `Memory/YYYYMMDD-memory-update/` containing:

**scan-manifest.md** — List of new files found, organised by:
- Directory (what was found where)
- Memory topic mapping (which files apply to which memory file)

## Important

- Write the COMPLETE manifest in a SINGLE operation
- DO NOT proceed to the next phase automatically
- Inform user to run the topic update commands next (any or all of: `/memory-org`, `/memory-strategy`, `/memory-projects`, `/memory-decisions`, `/memory-team`, `/memory-relationships`)
- The six topic commands can be run in any order, or in parallel

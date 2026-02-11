---
description: Update projects memory file based on scan manifest (Phase 2)
---

Update ONLY the projects and deliverables context based on today's scan manifest.

## Process

1. Find today's staging directory: `Memory/YYYYMMDD-memory-update/`
2. Read `scan-manifest.md` from that directory
3. Read current `Memory/memory-projects.md`
4. Read `config.yaml` for project context
5. Read relevant new files identified in the manifest
6. Create updated version incorporating new information

## Guidelines

Follow all guidelines in `Guidelines/memory-consolidation-guidelines.md`, especially:
- Professional tone
- Current state focus
- Status markers

## Factual Documentation Standards

Apply strict factual documentation:
- Source every assessment to a document/meeting
- Use metrics not adjectives
- Quote rather than interpret
- Remove ALL dramatic language unless directly quoted
- Focus on observable facts not predictions

Challenge yourself: "Is this fact or opinion?"

## Output

1. Plan the complete file structure before writing
2. Write the file in chunks to `Memory/YYYYMMDD-memory-update/memory-projects.md`:
   - First chunk: Write the header through the first major section (mode: rewrite)
   - Subsequent chunks: Append remaining sections one at a time (mode: append)
   - Keep each chunk under 120 lines to stay within output token limits
3. After all chunks written, read back the file to verify completeness and structure
4. STOP — do not proceed to other memory files

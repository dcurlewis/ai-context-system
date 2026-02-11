---
description: Promote validated updates to production (Phase 5 of 5)
---

Execute the final phase of memory update: promote staged files to production.

## Prerequisites

Only run after:
1. All six memory files exist in staging directory
2. Consolidation is complete (memory-index.md updated)
3. Validation has been run

## Process

1. Identify today's staging directory: `Memory/YYYYMMDD-memory-update/`
2. For each memory file in staging:
   - Archive previous version from `Memory/` to `Archive/Memory/YYYYMMDD-memory-archived/`
   - Copy new version from staging to `Memory/`
3. After all files promoted, move the entire staging directory to `Archive/Memory/`
   - `Memory/YYYYMMDD-memory-update/` → `Archive/Memory/YYYYMMDD-memory-update/`

## Files to Promote

From staging directory to `Memory/`:
- `memory-organization.md`
- `memory-strategy.md`
- `memory-projects.md`
- `memory-decisions.md`
- `memory-team-dynamics.md`
- `memory-relationships.md`

Note: `memory-index.md` is updated in-place during consolidation (not staged).

## Output

Confirm:
1. Which files were promoted
2. Where previous versions were archived (e.g., `Archive/Memory/20260202-memory-archived/`)
3. Where staging directory was moved (e.g., `Archive/Memory/20260202-memory-update/`)
4. Memory update cycle is complete

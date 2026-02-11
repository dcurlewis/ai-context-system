---
description: Validate staged memory updates (Phase 4 of 5)
---

Review the staged memory updates in today's staging directory for quality issues.

## Prerequisites

Verify all six memory files exist in `Memory/YYYYMMDD-memory-update/`. If any are missing, stop and inform the user.

## Validation Framework

### 1. Language Quality

Check for prohibited language (unless directly quoted from source):
- Crisis, emergency, critical
- Urgent, immediate, pressing (unless deadline-specific)
- Failure, collapse, disaster
- Hemorrhaging, bleeding, dying (metaphorical)
- Perfect storm, under siege, existential threat
- Total, complete, absolute (absolutist qualifiers)

### 2. Factual Rigour

- **Unsourced priority/severity assessments** — Flag for removal or add source
- **Predictive statements** — Convert to current state
- **Opinion vs fact** — Remove opinions unless attributed
- **Missing source attributions** — Add "SOURCE NEEDED" marker or fix

### 3. Content Quality

For each file, assess:
- **Coherence**: Does the content flow logically?
- **Completeness**: Are key topics covered adequately?
- **Clarity**: Is the writing clear and scannable?
- **Actionability**: Are status markers and next steps clear?

### 4. File Length Assessment

Compare each staged file against production:
- Is the file significantly longer than target? (see guidelines for targets)
- If longer: Is the additional length justified by new content?
- If shorter: Has important context been lost?

Report significant deviations but don't enforce strict line counts.

### 5. Staleness Detection

Look for content that should have been updated or removed:
- **Completed items still marked [IN PROGRESS]** or [PENDING]
- **Departed personnel** still listed as current
- **Resolved decisions** still in active sections
- **Past dates** in "upcoming" or "next steps" sections
- **Superseded information** not reflecting latest source files
- **Duplicate information** across multiple files

Cross-reference against scan manifest: if a topic had new source files, verify the staged file reflects that new information.

### 6. Cross-File Consistency

Check for:
- Same person/project described differently across files
- Contradictory status markers
- Duplicated content that should exist in one place only

## Output

Generate validation report with:

1. **Summary**: Pass/Fail with issue count
2. **Issues by severity**:
   - **Blocking**: Must fix before promotion (unsourced claims, factual errors, stale critical info)
   - **Warning**: Should fix (length concerns, minor staleness, language issues)
   - **Note**: Optional improvements
3. **Per-file breakdown**: Specific issues with line references where applicable
4. **Staleness findings**: Any content that appears outdated vs source files

## Decision

- **If blocking issues found**: List fixes needed, do not proceed
- **If only warnings**: List issues, recommend fixing, user decides whether to promote
- **If validation passes**: Inform user to run `/memory-promote`

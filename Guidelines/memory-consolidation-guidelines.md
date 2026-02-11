# Memory Consolidation Guidelines

*These guidelines serve as the source of truth for the memory update process and should be followed during all memory update operations to maintain concise, current-state-focused memory files.*

## Memory Update Process Overview

The memory system update follows a five-phase process using file existence to track progress:

### Phase 1: Scan (`/memory-scan`)

- Read `Memory/memory-index.md` to find the last update date
- List all subdirectories in `Curated-Context/`
- Filter for files with dates on or after the last-updated date
- Create `Memory/YYYYMMDD-memory-update/scan-manifest.md`
- Note any dramatic language in source files to be filtered during consolidation
- Flag factual claims that need source verification
- Identify opinion statements to be excluded from consolidation

### Phase 2: Update Individual Files

Six topic commands update memory files based on the scan manifest. These can run in parallel:

- `/memory-org` → `memory-organization.md`
- `/memory-strategy` → `memory-strategy.md`
- `/memory-projects` → `memory-projects.md`
- `/memory-decisions` → `memory-decisions.md`
- `/memory-team` → `memory-team-dynamics.md`
- `/memory-relationships` → `memory-relationships.md`

For each file:

1. Read current content from `Memory/`
2. Integrate new information from scanned files
3. Apply all consolidation techniques and tone guidelines
4. Write to staging directory (`Memory/YYYYMMDD-memory-update/`)

### Phase 3: Consolidate (`/memory-consolidate`)

**Prerequisite**: All six memory files must exist in staging. If any are missing, STOP.

- Review all updated files for adherence to guidelines
- Update `Memory/memory-index.md` with timestamp and changes summary
- Focus on content quality, not file sizes

### Phase 4: Validate (`/memory-validate`)

Comprehensive quality review:

- Check for unsourced assessments and dramatic language
- Convert predictive statements to current state
- Flag opinions for removal
- Assess overall content quality and coherence
- Check file lengths against targets
- Detect stale data that should have been updated
- Verify cross-file consistency

### Phase 5: Promote (`/memory-promote`)

- Archive previous versions to `Archive/Memory/YYYYMMDD-memory-archived/`
- Move updated files from staging to `Memory/`
- Only proceed after validation passes

## Core Principles

1. **Current State Focus**: Prioritise what's true today over historical narratives
2. **Status Tracking**: Use clear markers to indicate the state of items
3. **Conciseness**: Keep files focused; archive historical details
4. **No Duplication**: Information should exist in one place only
5. **Archive References**: Historical details go to archive with references
6. **Professional Tone**: Use neutral, factual language without dramatic descriptors

## Factual Documentation Standards

### Source Attribution Requirements

- Every claim must be traceable to a source document
- Use phrases like "Per [date] meeting notes..." or "According to [document]..."
- Distinguish between stated facts and observed patterns
- NO unsourced assessments of priority, risk, or importance

### Prohibited Language Patterns

NEVER use these terms unless directly quoted from source material:

- Crisis, emergency, critical (unless in direct quotes)
- Urgent, immediate, pressing (unless deadline-specific)
- Failure, collapse, disaster
- Hemorrhaging, bleeding, dying (metaphorical use)
- Perfect storm, under siege, existential threat
- Total, complete, absolute (absolutist qualifiers)

### Objective Alternatives

Instead of subjective assessments, use:

- Metrics: "3 of 10 engineers resigned" NOT "massive exodus"
- Timelines: "Due by Sept 15" NOT "urgent"
- Comparisons: "20% below target" NOT "failing"
- Quotes: "PM described as 'high priority'" NOT "high priority"

## Standard Status Markers

### For Decisions & Issues

- `[IMPLEMENTED]` - Decision executed and complete
- `[IN PROGRESS]` - Active implementation underway
- `[PENDING]` - Decided but not yet started
- `[BLOCKED]` - Implementation blocked by dependency
- `[UNRESOLVED]` - Decision not yet made
- `[STATUS UNKNOWN]` - Needs verification

### For Projects & Initiatives

- `[ACTIVE]` - Currently being worked on
- `[PLANNED]` - Scheduled but not started
- `[COMPLETED]` - Finished successfully
- `[BLOCKED]` - Progress halted
- `[CANCELLED]` - No longer proceeding
- `[ON HOLD]` - Temporarily paused

### For People & Relationships

- `[CURRENT]` - Active relationship/role
- `[DEPARTING]` - Leaving soon
- `[DEPARTED]` - Already left (remove in next update)
- `[CRITICAL]` - Needs immediate attention
- `[MONITORING]` - Watching for issues

### For Strategic Items

- `[ACTIVE]` - Current strategy in effect
- `[PLANNED]` - Future strategy approved
- `[DEPRECATED]` - Being phased out
- `[PROPOSED]` - Under consideration

## Target File Sizes (Loose Guidelines)

These are approximate targets to prevent bloat, NOT strict requirements. Focus on content quality and conciseness.

- **memory-organization.md**: ~100 lines (80-120 acceptable)
- **memory-strategy.md**: ~130 lines (100-150 acceptable)
- **memory-projects.md**: ~120 lines (90-140 acceptable)
- **memory-decisions.md**: ~120 lines (90-140 acceptable)
- **memory-relationships.md**: ~130 lines (100-150 acceptable)
- **memory-team-dynamics.md**: ~100 lines (80-120 acceptable)

If a file exceeds these significantly, consider whether content can be consolidated or archived.

## Consolidation Techniques

### 1. Compress Historical Narratives

**Before:**

```markdown
## Hoth Invasion Planning (June 4, 2025)
- Meeting held at 2pm with all commanders
- Veers initially very resistant, said "the walkers aren't ready"
- Discussion went for 2 hours
- Eventually agreed to timeline with conditions
- Piett will coordinate fleet positioning
[... 20 more lines of narrative ...]
```

**After:**

```markdown
## Hoth Invasion [IMPLEMENTED]
- Three battalions, full AT-AT complement committed
- Initial resistance overcome, operation launched successfully
```

### 2. Maintain Professional Tone

**Before:**

```markdown
## Fleet Crisis [EMERGENCY]
- Officers requesting transfers to Executor Command
- Under siege from multiple directions
- Existential threat to station readiness
```

**After:**

```markdown
## Retention Challenge [HIGH PRIORITY]
- 3 officers exploring fleet transfers
- Multiple concurrent resource constraints
- Mitigation: Commendation campaign, audiences with Lord Vader scheduled
```

### 3. Remove Resolved Items

- Personnel who have left the organisation
- Completed projects with no ongoing relevance
- Resolved conflicts or issues
- Outdated vendor relationships

### 4. Group by Status, Not Chronology

Instead of date-based entries, group items by their current status to make scanning easier.

### 5. Use Brief References

For items that need historical context, use single-line references:

```markdown
For implementation history, see: `Archive/Memory/YYYYMMDD-memory-archived/`
```

### 6. Combine Related Updates

Multiple dated updates about the same topic should be consolidated into current state.

## Quality Checks

Before finalising any memory update:

1. Verify all items have appropriate status markers
2. Confirm no duplication across files
3. Ensure focus is on current state
4. Add archive references where historical detail removed
5. **Verify professional tone throughout** - no dramatic language
6. Check content is reasonably concise

## Professional Tone Requirements

### Fact-Based Writing Framework

1. **Observable Facts Only**
   - ✅ "Meeting scheduled for next week"
   - ❌ "Critical meeting scheduled" (unless someone said "critical")

2. **Quantify When Possible**
   - ✅ "Response time increased from 2 to 5 days"
   - ❌ "Response time has become unacceptable"

3. **Source Your Assessments**
   - ✅ "Leadership team identified this as top priority in Aug meeting"
   - ❌ "This is a top priority"

4. **Avoid Predictive Language**
   - ✅ "Team exploring transfer options"
   - ❌ "Team likely to leave soon"

### Language Guidelines

Use neutral, factual descriptions throughout:

- ✅ "Team experiencing high attrition" NOT ❌ "hemorrhaging people"
- ✅ "Multiple concurrent challenges" NOT ❌ "perfect storm"  
- ✅ "Exploring transfer options" NOT ❌ "near-certain departure"
- ✅ "Limited resources" NOT ❌ "skeleton crew"
- ✅ "High priority" NOT ❌ "existential crisis"
- ✅ "Under pressure" NOT ❌ "under siege"
- ✅ "Resource constraints" NOT ❌ "crisis mode"

### Writing Approach

- State facts objectively with metrics where available
- Focus on current situation without catastrophising
- Present challenges as problems to solve
- Include mitigation steps where known
- Let status markers convey urgency without amplification
- Balance challenges with positive developments

## When NOT to Consolidate

- Active ongoing issues that need full context
- Recent decisions (< 1 month) still being implemented
- Critical relationship dynamics affecting current work
- Strategic items under active debate

## Archive Strategy

When removing content, ensure it's preserved in:

- `Archive/Memory/YYYYMMDD-memory-archived/`
- With clear filenames indicating what was archived
- Brief note in current file pointing to archive location

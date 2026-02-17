#!/bin/bash
# Nightly memory update automation script
# Orchestrates the full 5-phase memory update cycle using Claude CLI.
#
# Phases:
#   1. /memory-scan - Scan for new files since last update
#   2. 6x parallel topic updates (/memory-org, /memory-strategy, etc.)
#   3. /memory-consolidate - Review and refresh index
#   4. /memory-validate - Quality checks
#   5. /memory-promote - Move staged files to production
#
# Includes skip logic (no update if no new content), archive pruning,
# and git backup via /backup.
#
# Cron: 0 23 * * 1-5 /path/to/ai-context-system/Scripts/run_memory_update.sh

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BASE_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
LOG_FILE="${BASE_DIR}/Scripts/memory-update.log"
MEMORY_DIR="${BASE_DIR}/Memory"
CURATED_DIR="${BASE_DIR}/Curated-Context"
ARCHIVE_DIR="${BASE_DIR}/Archive/Memory"
CLAUDE_CMD="claude"

# Maximum number of archived directories to keep
MAX_ARCHIVES=30

log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') | $1" >> "$LOG_FILE"
}

log_section() {
    echo "" >> "$LOG_FILE"
    echo "========================================" >> "$LOG_FILE"
    log "$1"
    echo "========================================" >> "$LOG_FILE"
}

run_claude() {
    local description="$1"
    local command_file="$2"

    log "Starting: $description"
    $CLAUDE_CMD -p "Read and execute the command file at .claude/commands/${command_file}. Follow all instructions in it exactly." \
        --permission-mode auto-accept \
        --output-format text \
        2>&1 | tail -20 >> "$LOG_FILE"
    local exit_code=${PIPESTATUS[0]}
    log "Finished: $description (exit code: $exit_code)"
    return $exit_code
}

cd "$BASE_DIR" || exit 1

log_section "MEMORY UPDATE started"

# --- Skip Logic ---
# Check if there are new files in Curated-Context/ since the last memory update.
# Extract the last update date from memory-index.md.
LAST_UPDATE_DATE=$(grep -m1 "Last Updated" "$MEMORY_DIR/memory-index.md" 2>/dev/null \
    | grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2}' \
    | head -1)

if [ -z "$LAST_UPDATE_DATE" ]; then
    log "WARNING: Could not extract last update date from memory-index.md. Proceeding with update."
else
    log "Last memory update: $LAST_UPDATE_DATE"

    # Count new/modified files in Curated-Context/ (excluding dirs we skip)
    NEW_FILE_COUNT=$(find "$CURATED_DIR" \
        -not -path "*/.obsidian/*" \
        -not -path "*/Obsidian-Specific-Dirs/*" \
        -not -path "*/Daily-Journals/*" \
        -not -path "*/Blog/*" \
        -name "*.md" \
        -newer "$MEMORY_DIR/memory-index.md" \
        -type f 2>/dev/null | wc -l | tr -d ' ')

    log "New/modified files since last update: $NEW_FILE_COUNT"

    if [ "$NEW_FILE_COUNT" -eq 0 ]; then
        log "No new content since last update - skipping memory update"

        # Still run backup to catch any other changes (synced data, journals, etc.)
        log "Running /backup for any other changes..."
        run_claude "/backup" "backup.md"

        log_section "MEMORY UPDATE skipped (no new content)"
        exit 0
    fi
fi

# --- Check for existing staging directory ---
# If a staging directory already exists, the previous run may have been
# interrupted. The file-existence-based progress tracking means we can
# resume from where we left off.
TODAY=$(date '+%Y%m%d')
STAGING_DIR="${MEMORY_DIR}/${TODAY}-memory-update"

if [ -d "$STAGING_DIR" ]; then
    log "Found existing staging directory: $STAGING_DIR (resuming)"
else
    log "No existing staging directory; starting fresh"
fi

# --- Phase 1: Memory Scan ---
if [ ! -f "${STAGING_DIR}/scan-manifest.md" ]; then
    log "--- Phase 1: Memory Scan ---"
    run_claude "memory-scan" "memory-scan.md"
    SCAN_EXIT=$?

    if [ $SCAN_EXIT -ne 0 ] || [ ! -f "${STAGING_DIR}/scan-manifest.md" ]; then
        log "ERROR: Memory scan failed or did not produce scan-manifest.md"
        log_section "MEMORY UPDATE failed at Phase 1 (scan)"
        exit 1
    fi
else
    log "Phase 1: scan-manifest.md already exists, skipping scan"
fi

# --- Phase 2: Topic Updates (parallel) ---
log "--- Phase 2: Topic Updates (6 parallel) ---"

TOPIC_COMMANDS=(
    "memory-org:memory-organization.md"
    "memory-strategy:memory-strategy.md"
    "memory-projects:memory-projects.md"
    "memory-decisions:memory-decisions.md"
    "memory-team:memory-team-dynamics.md"
    "memory-relationships:memory-relationships.md"
)

PIDS=()
TOPIC_NAMES=()

for entry in "${TOPIC_COMMANDS[@]}"; do
    CMD="${entry%%:*}"
    OUTPUT_FILE="${entry##*:}"

    if [ -f "${STAGING_DIR}/${OUTPUT_FILE}" ]; then
        log "  $CMD: ${OUTPUT_FILE} already exists, skipping"
        continue
    fi

    log "  Starting: $CMD (-> ${OUTPUT_FILE})"
    (
        run_claude "$CMD" "${CMD}.md"
    ) &
    PIDS+=($!)
    TOPIC_NAMES+=("$CMD")
done

# Wait for all parallel topic updates
PHASE2_FAILED=0
for i in "${!PIDS[@]}"; do
    wait "${PIDS[$i]}"
    EXIT_CODE=$?
    if [ $EXIT_CODE -ne 0 ]; then
        log "  ERROR: ${TOPIC_NAMES[$i]} failed (exit code: $EXIT_CODE)"
        PHASE2_FAILED=1
    fi
done

# Verify all 6 files exist
MISSING_FILES=()
for entry in "${TOPIC_COMMANDS[@]}"; do
    OUTPUT_FILE="${entry##*:}"
    if [ ! -f "${STAGING_DIR}/${OUTPUT_FILE}" ]; then
        MISSING_FILES+=("$OUTPUT_FILE")
    fi
done

if [ ${#MISSING_FILES[@]} -gt 0 ]; then
    log "ERROR: Missing files after Phase 2: ${MISSING_FILES[*]}"
    log_section "MEMORY UPDATE failed at Phase 2 (topic updates incomplete)"
    exit 1
fi

log "Phase 2 complete: all 6 topic files present"

# --- Phase 3: Consolidate ---
log "--- Phase 3: Consolidate ---"
run_claude "memory-consolidate" "memory-consolidate.md"
CONSOLIDATE_EXIT=$?
if [ $CONSOLIDATE_EXIT -ne 0 ]; then
    log "ERROR: Consolidation failed"
    log_section "MEMORY UPDATE failed at Phase 3 (consolidate)"
    exit 1
fi

# --- Phase 4: Validate ---
log "--- Phase 4: Validate ---"
run_claude "memory-validate" "memory-validate.md"
VALIDATE_EXIT=$?
if [ $VALIDATE_EXIT -ne 0 ]; then
    log "WARNING: Validation reported issues (exit code: $VALIDATE_EXIT)"
    log "Proceeding with promotion (automated run; review logs if needed)"
fi

# --- Phase 5: Promote ---
log "--- Phase 5: Promote ---"
run_claude "memory-promote" "memory-promote.md"
PROMOTE_EXIT=$?
if [ $PROMOTE_EXIT -ne 0 ]; then
    log "ERROR: Promotion failed"
    log_section "MEMORY UPDATE failed at Phase 5 (promote)"
    exit 1
fi

log "Memory update cycle complete"

# --- Archive Pruning ---
log "--- Archive Pruning ---"
if [ -d "$ARCHIVE_DIR" ]; then
    # Prune old *-memory-archived directories
    ARCHIVED_DIRS=($(ls -d "${ARCHIVE_DIR}/"*-memory-archived 2>/dev/null | sort))
    ARCHIVED_COUNT=${#ARCHIVED_DIRS[@]}
    if [ $ARCHIVED_COUNT -gt $MAX_ARCHIVES ]; then
        PRUNE_COUNT=$((ARCHIVED_COUNT - MAX_ARCHIVES))
        log "Pruning $PRUNE_COUNT old archived directories (keeping last $MAX_ARCHIVES)"
        for ((i=0; i<PRUNE_COUNT; i++)); do
            rm -rf "${ARCHIVED_DIRS[$i]}"
            log "  Removed: $(basename "${ARCHIVED_DIRS[$i]}")"
        done
    else
        log "Archived directories: $ARCHIVED_COUNT (under limit of $MAX_ARCHIVES)"
    fi

    # Prune old *-memory-update directories
    UPDATE_DIRS=($(ls -d "${ARCHIVE_DIR}/"*-memory-update 2>/dev/null | sort))
    UPDATE_COUNT=${#UPDATE_DIRS[@]}
    if [ $UPDATE_COUNT -gt $MAX_ARCHIVES ]; then
        PRUNE_COUNT=$((UPDATE_COUNT - MAX_ARCHIVES))
        log "Pruning $PRUNE_COUNT old update directories (keeping last $MAX_ARCHIVES)"
        for ((i=0; i<PRUNE_COUNT; i++)); do
            rm -rf "${UPDATE_DIRS[$i]}"
            log "  Removed: $(basename "${UPDATE_DIRS[$i]}")"
        done
    else
        log "Update directories: $UPDATE_COUNT (under limit of $MAX_ARCHIVES)"
    fi
else
    log "No archive directory found at $ARCHIVE_DIR"
fi

# --- Git Backup ---
log "--- Git Backup ---"
run_claude "/backup" "backup.md"
BACKUP_EXIT=$?
if [ $BACKUP_EXIT -ne 0 ]; then
    log "WARNING: Git backup failed (exit code: $BACKUP_EXIT)"
fi

log_section "MEMORY UPDATE completed successfully"
exit 0

#!/bin/bash
# Wrapper script for automated Jira + GitHub sync
# Adds timestamps and ensures proper environment

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
LOG_FILE="${SCRIPT_DIR}/sync.log"

cd "$SCRIPT_DIR" || exit 1

echo "" >> "$LOG_FILE"
echo "========================================" >> "$LOG_FILE"
echo "Sync started: $(date '+%Y-%m-%d %H:%M:%S')" >> "$LOG_FILE"
echo "========================================" >> "$LOG_FILE"

# Run Jira sync
"$SCRIPT_DIR/.venv/bin/python" "$SCRIPT_DIR/sync_jira.py" >> "$LOG_FILE" 2>&1
JIRA_EXIT=$?
echo "Jira sync finished: $(date '+%Y-%m-%d %H:%M:%S') (exit code: $JIRA_EXIT)" >> "$LOG_FILE"

# Run GitHub sync
echo "GitHub sync started: $(date '+%Y-%m-%d %H:%M:%S')" >> "$LOG_FILE"
"$SCRIPT_DIR/.venv/bin/python" "$SCRIPT_DIR/sync_github.py" >> "$LOG_FILE" 2>&1
GITHUB_EXIT=$?
echo "GitHub sync finished: $(date '+%Y-%m-%d %H:%M:%S') (exit code: $GITHUB_EXIT)" >> "$LOG_FILE"

echo "" >> "$LOG_FILE"

# Exit with non-zero if either sync failed
if [ $JIRA_EXIT -ne 0 ] || [ $GITHUB_EXIT -ne 0 ]; then
    exit 1
fi
exit 0

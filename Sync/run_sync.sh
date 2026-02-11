#!/bin/bash
# Wrapper script for automated Jira sync
# Adds timestamps and ensures proper environment

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
LOG_FILE="${SCRIPT_DIR}/sync_jira.log"

cd "$SCRIPT_DIR" || exit 1

echo "" >> "$LOG_FILE"
echo "========================================" >> "$LOG_FILE"
echo "Sync started: $(date '+%Y-%m-%d %H:%M:%S')" >> "$LOG_FILE"
echo "========================================" >> "$LOG_FILE"

# Run the sync with the virtual environment's Python
"$SCRIPT_DIR/.venv/bin/python" "$SCRIPT_DIR/sync_jira.py" >> "$LOG_FILE" 2>&1
EXIT_CODE=$?

echo "Sync finished: $(date '+%Y-%m-%d %H:%M:%S') (exit code: $EXIT_CODE)" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

exit $EXIT_CODE

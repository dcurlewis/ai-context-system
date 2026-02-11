#!/bin/bash
# Wrapper script for automated RSS news fetch
# Adds timestamps and ensures proper environment

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
LOG_FILE="$PROJECT_ROOT/Synced-Data/News/fetch_rss.log"

cd "$SCRIPT_DIR" || exit 1

echo "" >> "$LOG_FILE"
echo "========================================" >> "$LOG_FILE"
echo "News fetch started: $(date '+%Y-%m-%d %H:%M:%S')" >> "$LOG_FILE"
echo "========================================" >> "$LOG_FILE"

# Run the fetch script with the virtual environment's Python
"$SCRIPT_DIR/.venv/bin/python" "$SCRIPT_DIR/fetch_rss.py" >> "$LOG_FILE" 2>&1
EXIT_CODE=$?

echo "News fetch finished: $(date '+%Y-%m-%d %H:%M:%S') (exit code: $EXIT_CODE)" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

exit $EXIT_CODE

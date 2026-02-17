#!/bin/bash
# Automated morning journal generation script
# Invokes Claude CLI to run the /morning command after data ingress completes.
#
# Cron: 30 7 * * 1-5 /path/to/ai-context-system/Scripts/run_morning.sh

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BASE_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
LOG_FILE="${BASE_DIR}/Scripts/morning.log"
CLAUDE_CMD="claude"

cd "$BASE_DIR" || exit 1

echo "" >> "$LOG_FILE"
echo "========================================" >> "$LOG_FILE"
echo "MORNING started: $(date '+%Y-%m-%d %H:%M:%S')" >> "$LOG_FILE"
echo "========================================" >> "$LOG_FILE"

$CLAUDE_CMD -p "Read and execute the command file at .claude/commands/morning.md. Follow all instructions in it exactly." \
    --permission-mode auto-accept \
    --output-format text \
    2>&1 | tail -50 >> "$LOG_FILE"
EXIT_CODE=${PIPESTATUS[0]}

echo "MORNING finished: $(date '+%Y-%m-%d %H:%M:%S') (exit code: $EXIT_CODE)" >> "$LOG_FILE"
echo "========================================" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

exit $EXIT_CODE

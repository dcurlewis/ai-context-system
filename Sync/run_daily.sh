#!/bin/bash
# Daily data ingress orchestration script
# Runs all sync tasks sequentially with independent failure handling.
# Each step can fail without blocking subsequent steps.
#
# Cron: 0 7 * * 1-5 /path/to/ai-context-system/Sync/run_daily.sh
#
# Replaces the old run_sync.sh (Monday-only Jira + GitHub).

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BASE_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
SYNC_DIR="${BASE_DIR}/Sync"
SCRIPTS_DIR="${BASE_DIR}/Scripts"
LOG_FILE="${SYNC_DIR}/daily.log"
PYTHON="${SYNC_DIR}/.venv/bin/python"

cd "$SYNC_DIR" || exit 1

echo "" >> "$LOG_FILE"
echo "========================================" >> "$LOG_FILE"
echo "DAILY SYNC started: $(date '+%Y-%m-%d %H:%M:%S')" >> "$LOG_FILE"
echo "========================================" >> "$LOG_FILE"

# Track results for summary line
JIRA_STATUS="SKIP"
GITHUB_STATUS="SKIP"
SLACK_STATUS="SKIP"
CALENDAR_STATUS="SKIP"

# --- Step 1: Jira sync ---
echo "--- Jira sync started: $(date '+%Y-%m-%d %H:%M:%S') ---" >> "$LOG_FILE"
"$PYTHON" "$SYNC_DIR/sync_jira.py" >> "$LOG_FILE" 2>&1
JIRA_EXIT=$?
if [ $JIRA_EXIT -eq 0 ]; then
    JIRA_STATUS="OK"
else
    JIRA_STATUS="FAIL(exit=$JIRA_EXIT)"
fi
echo "Jira sync finished: $(date '+%Y-%m-%d %H:%M:%S') (exit code: $JIRA_EXIT)" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

# --- Step 2: GitHub sync ---
echo "--- GitHub sync started: $(date '+%Y-%m-%d %H:%M:%S') ---" >> "$LOG_FILE"
"$PYTHON" "$SYNC_DIR/sync_github.py" >> "$LOG_FILE" 2>&1
GITHUB_EXIT=$?
if [ $GITHUB_EXIT -eq 0 ]; then
    GITHUB_STATUS="OK"
else
    GITHUB_STATUS="FAIL(exit=$GITHUB_EXIT)"
fi
echo "GitHub sync finished: $(date '+%Y-%m-%d %H:%M:%S') (exit code: $GITHUB_EXIT)" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

# --- Step 3: Slack sync ---
echo "--- Slack sync started: $(date '+%Y-%m-%d %H:%M:%S') ---" >> "$LOG_FILE"
"$PYTHON" "$SYNC_DIR/sync_slack.py" >> "$LOG_FILE" 2>&1
SLACK_EXIT=$?
if [ $SLACK_EXIT -eq 0 ]; then
    SLACK_STATUS="OK"
elif grep -q "expired_token\|token expired\|invalid_auth\|Re-extract" "$LOG_FILE" 2>/dev/null; then
    SLACK_STATUS="FAIL(expired_token)"
else
    SLACK_STATUS="FAIL(exit=$SLACK_EXIT)"
fi
echo "Slack sync finished: $(date '+%Y-%m-%d %H:%M:%S') (exit code: $SLACK_EXIT)" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

# --- Step 4: Calendar fetch ---
echo "--- Calendar fetch started: $(date '+%Y-%m-%d %H:%M:%S') ---" >> "$LOG_FILE"
python3 "$SCRIPTS_DIR/calendar-today.py" >> "$LOG_FILE" 2>&1
CALENDAR_EXIT=$?
if [ $CALENDAR_EXIT -eq 0 ]; then
    CALENDAR_STATUS="OK"
else
    CALENDAR_STATUS="FAIL(exit=$CALENDAR_EXIT)"
fi
echo "Calendar fetch finished: $(date '+%Y-%m-%d %H:%M:%S') (exit code: $CALENDAR_EXIT)" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

# --- Summary ---
SUMMARY="DAILY SYNC COMPLETE: jira=$JIRA_STATUS github=$GITHUB_STATUS slack=$SLACK_STATUS calendar=$CALENDAR_STATUS"
echo "$SUMMARY" >> "$LOG_FILE"
echo "Finished: $(date '+%Y-%m-%d %H:%M:%S')" >> "$LOG_FILE"
echo "========================================" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

# Exit with non-zero only if a critical sync failed (Jira)
# GitHub and Slack failures are non-fatal (auth issues, token expiry)
if [ $JIRA_EXIT -ne 0 ]; then
    exit 1
fi
exit 0

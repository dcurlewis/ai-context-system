# Data Sync Setup Guide

## Overview

The sync scripts fetch data from external services (Jira, GitHub, Slack, Calendar) and store it locally as JSON files. This data is then available to Claude for context during your sessions.

## What the Scripts Support

1. **Jira sync** — Issue hierarchies with prefix filtering, multiple root issues, and ADF-to-Markdown conversion
2. **GitHub sync** — Merged PRs by team members with Jira key cross-referencing
3. **Slack sync** — Channel messages with thread replies, user name resolution, and incremental sync
4. **Calendar sync** — Today's calendar events via macOS EventKit
5. **Daily orchestration** — All syncs run together with independent failure handling
6. **Automated pipeline** — Cron-based daily data ingress, morning journal generation, and nightly memory updates

## Setup Steps

### 1. Set up Python environment (one-time)

```bash
cd Sync

# Create virtual environment
python3 -m venv .venv

# Activate it
source .venv/bin/activate

# Install dependencies
pip install requests python-dotenv
```

### 2. Configure credentials

Copy the example `.env` file and fill in your details:

```bash
cp .env.example .env
```

Your `.env` file should contain:

```bash
# Jira Configuration
JIRA_EMAIL=your.email@company.com
JIRA_API_TOKEN=your-api-token-here
JIRA_BASE_URL=https://your-company.atlassian.net

# GitHub Configuration
GITHUB_TOKEN=ghp_xxxxxxxxxxxx

# Slack Configuration
SLACK_SESSION_TOKEN=xoxc-your-session-token-here
SLACK_COOKIE_D=your-d-cookie-value-here
SLACK_WORKSPACE_URL=https://your-workspace.slack.com
```

**Get your Jira API token:**
1. Go to https://id.atlassian.com/manage-profile/security/api-tokens
2. Click "Create API token"
3. Name it "AI-Context Sync"
4. Copy and paste into `.env`

**Get your Slack session token and cookie:**
1. Open Slack in your browser and press F12 (DevTools)
2. Go to Console and run:
   ```javascript
   JSON.parse(localStorage.getItem('localConfig_v2')).teams[
       Object.keys(JSON.parse(localStorage.getItem('localConfig_v2')).teams)[0]
   ].token
   ```
3. Copy the `xoxc-...` token into `SLACK_SESSION_TOKEN`
4. For the `d` cookie, run in Console:
   ```javascript
   document.cookie.split('; ').find(c => c.startsWith('d=')).slice(2)
   ```
   Or: DevTools > Application > Cookies > `https://app.slack.com` > find the `d` cookie
5. Copy into `SLACK_COOKIE_D`

Note: Session tokens expire periodically (typically every few weeks). When they do, the Slack sync will report an `expired_token` error and you'll need to re-extract from the browser.

### 3. Configure root issues

Copy the example config and adjust for your Jira project:

```bash
cp config.example.json config.json
```

Edit `config.json` with your root issue keys and optional filter prefix.

### 4. Test the sync

```bash
cd Sync
source .venv/bin/activate

# Run the sync
python sync_jira.py
```

### 5. Review the output

```bash
# Human-readable index
cat ../Synced-Data/Jira/INDEX.md

# Metadata
cat ../Synced-Data/Jira/_meta.json

# List all synced issues
ls ../Synced-Data/Jira/issues/

# View a specific issue
cat ../Synced-Data/Jira/issues/PROJ-123.json
```

## What to Expect

The script will:
1. Fetch your root issues
2. Get their children (optionally filtered by prefix)
3. Recursively fetch all descendants
4. Convert descriptions and comments from ADF to Markdown
5. Save everything to `Synced-Data/Jira/`

**Output includes:**
- Individual JSON files for each issue
- `INDEX.md` - Human-readable grouped by level and status
- `index.json` - Structured data for programmatic access
- `_meta.json` - Sync metadata

## Command Line Options

```bash
# Use config (default)
python sync_jira.py

# Override roots temporarily
python sync_jira.py --root PROJ-1 --root PROJ-2

# Override filter temporarily
python sync_jira.py --filter TEAM-

# Combine overrides
python sync_jira.py --root PROJ-1 --root PROJ-2 --filter TEAM-
```

## Automation (Optional)

The system includes a full automation pipeline with daily data ingress, morning journal generation, and nightly memory updates.

### Install the cron schedule

A reference crontab is provided at `Scripts/crontab.txt`. Edit the paths to match your clone location, then install:

```bash
# Review and edit paths first
vi Scripts/crontab.txt

# Install (replaces existing crontab)
crontab Scripts/crontab.txt

# Or merge into existing crontab
crontab -e
# ... paste the entries from Scripts/crontab.txt
```

### Cron schedule

| Schedule | Script | Purpose |
|----------|--------|---------|
| Weekdays 7:00am | `Sync/run_daily.sh` | Data ingress: Jira, GitHub, Slack, Calendar |
| Weekdays 7:30am | `Scripts/run_morning.sh` | Morning journal via Claude CLI |
| Monday 7:15am | `Scripts/News/run_fetch_news.sh` | RSS news fetch |
| Weekdays 11:00pm | `Scripts/run_memory_update.sh` | Full memory update cycle via Claude CLI |

`run_daily.sh` runs all four syncs sequentially with independent failure handling (one failure does not block others). `run_memory_update.sh` orchestrates the full 5-phase memory update cycle with skip logic (skips if no new content) and archive pruning. Both Claude CLI scripts use `claude -p` in non-interactive mode with `--permission-mode auto-accept`.

### View logs

```bash
# Daily sync log
tail -50 Sync/daily.log

# Morning journal log
tail -50 Scripts/morning.log

# Memory update log
tail -50 Scripts/memory-update.log

# RSS fetch log
tail -50 Synced-Data/News/fetch_rss.log

# View scheduled jobs
crontab -l
```

## Troubleshooting

**"Invalid credentials"**
- Verify your JIRA_EMAIL matches your Atlassian account
- Regenerate API token if it's expired

**"Issue not found"**
- Verify issue keys exist and you have access
- Check issue keys in Jira web interface

**"No issues found"**
- Verify there are matching child issues under your root issues
- Try removing the filter temporarily to see all children:
  ```bash
  python sync_jira.py --filter ""
  ```

## Next Steps

Once sync is working:
1. Review the synced data structure
2. Set up automation if desired
3. Use the data for AI analysis and context building
4. Consider creating process guidelines in `Guidelines/`

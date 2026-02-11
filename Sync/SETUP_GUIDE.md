# Jira Sync Setup Guide

## Overview

The Jira sync script fetches issue hierarchies from your Jira instance and stores them locally as JSON files. This data is then available to Claude for context during your sessions.

## What the Script Supports

1. **Multiple root issues** - Track issues from multiple parent goals
2. **Prefix filtering** - Only sync children matching specific key patterns (e.g., "TEAM-")
3. **Issue type filtering** - Automatically excludes "Effort Estimate" issues (planning artifacts, not real work)
4. **Flexible configuration** - Backward compatible with single-root setups
5. **New Jira API** - Uses `/rest/api/3/search/jql` with token-based pagination

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
```

**Get your Jira API token:**
1. Go to https://id.atlassian.com/manage-profile/security/api-tokens
2. Click "Create API token"
3. Name it "AI-Context Sync"
4. Copy and paste into `.env`

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

A wrapper script `run_sync.sh` is provided that adds timestamps to logs.

### Set up weekly sync (every Monday at 8am)

```bash
crontab -e
```

Add this line:
```bash
0 8 * * 1 /path/to/your/ai-context-system/Sync/run_sync.sh
```

### Alternative schedules

```bash
# Daily at 8am
0 8 * * * /path/to/your/ai-context-system/Sync/run_sync.sh

# Weekdays at 8am
0 8 * * 1-5 /path/to/your/ai-context-system/Sync/run_sync.sh

# Monday and Thursday at 9am
0 9 * * 1,4 /path/to/your/ai-context-system/Sync/run_sync.sh
```

### View logs

```bash
# View recent log entries
tail -50 Sync/sync_jira.log

# Follow logs in real-time
tail -f Sync/sync_jira.log

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

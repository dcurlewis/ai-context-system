# AI-Context Sync Scripts

Sync Jira issue hierarchies into the AI-Context system for analysis.

## Setup

### 1. Create Python environment

```bash
cd Sync
python3 -m venv .venv
source .venv/bin/activate
pip install requests python-dotenv
```

### 2. Configure credentials

```bash
cp .env.example .env
# Edit .env with your actual credentials
```

### 3. Get API tokens

**Jira:**
1. Go to https://id.atlassian.com/manage-profile/security/api-tokens
2. Create a new API token
3. Use your Atlassian account email and this token

### 4. Configure root issues

Edit `config.json` to specify:
- Jira root issue key(s) - can be single or multiple
- Optional: filter_prefix to only sync children matching a key pattern

## Usage

### Jira Sync

```bash
# Sync entire hierarchy under root issue(s) from config
python sync_jira.py

# Override root issue (single)
python sync_jira.py --root PROJ-54

# Specify multiple root issues
python sync_jira.py --root PROJ-1 --root PROJ-2

# Filter children by key prefix (only gets TEAM-* issues)
python sync_jira.py --filter TEAM-

# Combine multiple roots with filtering
python sync_jira.py --root PROJ-1 --root PROJ-2 --filter TEAM-
```

## Jira Filtering

The `filter_prefix` option allows you to selectively sync only certain child issues from a parent goal. This is useful when:
- Parent goals contain issues from multiple teams
- You only want to track issues with specific key prefixes (e.g., "TEAM-" for your team)

**How it works:**
- The filter is applied to **level 1 only** (immediate children of root issues)
- All descendants of filtered issues are included automatically
- Use JQL wildcard syntax: `TEAM-` matches `TEAM-123`, `TEAM-456`, etc.

**Example:**
```json
{
  "jira": {
    "root_issues": ["PROJ-1", "PROJ-2"],
    "filter_prefix": "TEAM-",
    "description": "Only your team's goals"
  }
}
```

This will:
1. Fetch PROJ-1 and PROJ-2
2. Get only children starting with "TEAM-" (e.g., TEAM-101, TEAM-102)
3. Recursively fetch all descendants of those TEAM- issues (no filtering at deeper levels)

## Output Structure

```
Synced-Data/
└── Jira/
    ├── _meta.json             # Sync metadata
    ├── index.json             # Structured index for programmatic access
    ├── INDEX.md               # Human-readable navigation
    └── issues/
        └── {KEY}.json         # Individual issue files
```

## Issue Schema (Jira)

```json
{
  "key": "PROJ-123",
  "hierarchy_level": 1,
  "project": "PROJ",
  "summary": "Issue title",
  "description_text": "Markdown-converted description",
  "status": {"name": "In Progress", "category": "In Progress"},
  "issue_type": {"name": "Goal"},
  "assignee": {"name": "Jane Smith"},
  "parent": {"key": "PROJ-54", "summary": "Parent title"},
  "comments": [...],
  "jira_url": "https://your-company.atlassian.net/browse/PROJ-123"
}
```

## Automation (Optional)

Add to crontab for weekly syncs:

```bash
# Edit crontab
crontab -e

# Add line (adjust path as needed)
0 8 * * 1 /path/to/your/ai-context-system/Sync/run_sync.sh
```

## Troubleshooting

**"Jira 401 Unauthorized"**
- Verify email matches your Atlassian account
- Regenerate API token if expired

**"Issue not found"**
- Check issue key is correct
- Verify you have permission to view the issue

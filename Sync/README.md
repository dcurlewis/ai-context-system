# AI-Context Sync Scripts

Sync Jira issue hierarchies, GitHub activity, and Slack channels into the AI-Context system for analysis.

## Setup

### 1. Create Python environment

```bash
cd Sync
python3 -m venv .venv
source .venv/bin/activate
pip install requests python-dotenv pyyaml
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

**GitHub:**
1. Go to https://github.com/settings/tokens
2. Create a Personal Access Token (classic) with `repo` scope
3. For public-only orgs, `public_repo` scope is sufficient

### 4. Configure root issues and teams

Edit `config.json` to specify:
- Jira root issue key(s) — can be single or multiple
- Optional: `filter_prefix` to only sync children matching a key pattern
- GitHub org name and teams to sync (team names must match filenames in `Curated-Context/Teams/`)

### 5. GitHub sync prerequisites

Team members must have a `github` field in their `Curated-Context/People/{Name}.md` YAML front-matter:

```yaml
---
aliases:
  - Piett
role: VP Naval Operations
github: admiral-piett
# ...
---
```

Members without a `github` field will be skipped (with a warning).

## Usage

### Jira Sync

```bash
# Activate venv first
source .venv/bin/activate

# Sync entire hierarchy under root issue(s) from config
python sync_jira.py

# Override root issue (single)
python sync_jira.py --root PROJ-54

# Specify multiple root issues
python sync_jira.py --root DS-001 --root IMP-017

# Filter children by key prefix (only gets DS-* issues)
python sync_jira.py --filter DS-

# Combine multiple roots with filtering
python sync_jira.py --root DS-001 --root IMP-017 --filter DS-
```

### GitHub Sync

```bash
# Sync all configured teams (default 14-day lookback)
python sync_github.py

# Override lookback period
python sync_github.py --lookback 7

# Sync a single team (for testing)
python sync_github.py --team "Death Star Engineering"

# Verbose output including API queries
python sync_github.py --debug
```

The script reads team membership from `Curated-Context/Teams/{name}.md` stubs, resolves GitHub handles from `Curated-Context/People/{name}.md` front-matter, and fetches merged PRs via the GitHub Search API. Jira ticket keys are extracted from PR titles (regex: `[A-Z][A-Z0-9]+-\d+`).

### Slack Sync

```bash
# Activate venv first
source .venv/bin/activate

# Sync all configured channels
python sync_slack.py

# Sync a single channel
python sync_slack.py --channel general

# Override lookback period
python sync_slack.py --lookback 14

# Full sync (ignore last_synced timestamps)
python sync_slack.py --full

# Debug mode (show API responses)
python sync_slack.py --debug
```

The script uses Slack's internal web APIs with your session token (the same approach used by the [slacksnap](https://curlewis.co.nz/2025/08/05/i-built-another-thing-extract-slack/) browser extension). It supports incremental sync, thread replies, user/channel name resolution, and rate limiting.

**Session token extraction** (required for authentication):

1. Open Slack in your browser and press F12 (DevTools)
2. **Token** — Go to Console and run:
   ```javascript
   JSON.parse(localStorage.getItem('localConfig_v2')).teams[
       Object.keys(JSON.parse(localStorage.getItem('localConfig_v2')).teams)[0]
   ].token
   ```
3. **Cookie** — Go to Console and run:
   ```javascript
   document.cookie.split('; ').find(c => c.startsWith('d=')).slice(2)
   ```
   Or: DevTools > Application > Cookies > `https://app.slack.com` > find the `d` cookie

4. Add both to `Sync/.env`:
   ```
   SLACK_SESSION_TOKEN=xoxc-your-token-here
   SLACK_COOKIE_D=your-d-cookie-value-here
   SLACK_WORKSPACE_URL=https://your-workspace.slack.com
   ```

**Channel configuration** in `config.json`:
```json
{
  "slack": {
    "channels": [
      {"name": "general", "id": "C01234567", "enabled": true},
      {"name": "DM: Alice", "id": "D01234567", "type": "dm", "enabled": true}
    ],
    "lookback_days": 7,
    "include_threads": true
  }
}
```

Get channel IDs from the Slack URL (e.g., `https://app.slack.com/client/T.../C01234567`) or by right-clicking a channel > "Copy link".

## Jira Filtering

The `filter_prefix` option allows you to selectively sync only certain child issues from a parent goal. This is useful when:
- Parent goals contain issues from multiple teams
- You only want to track issues with specific key prefixes (e.g., "DS-" for Death Star issues)

**How it works:**
- The filter is applied to **level 1 only** (immediate children of root issues)
- All descendants of filtered issues are included automatically
- Use JQL wildcard syntax: `DS-` matches `DS-123`, `DS-456`, etc.

**Example:**
```json
{
  "jira": {
    "root_issues": ["DS-001", "IMP-017"],
    "filter_prefix": "DS-",
    "description": "Only Death Star team goals"
  }
}
```

This will:
1. Fetch DS-001 and IMP-017
2. Get only children starting with "DS-" (e.g., DS-101, DS-102)
3. Recursively fetch all descendants of those DS- issues (no filtering at deeper levels)

## Output Structure

```
Synced-Data/
├── Jira/
│   ├── _meta.json             # Sync metadata
│   ├── index.json             # Structured index for programmatic access
│   ├── INDEX.md               # Human-readable navigation
│   └── issues/
│       └── {KEY}.json         # Individual issue files
├── GitHub/
│   ├── _meta.json             # Sync metadata (teams, member counts, timestamps)
│   ├── index.json             # Compact queryable index (all PRs)
│   ├── INDEX.md               # Human-readable summary grouped by team/author
│   └── pull-requests/
│       └── {repo}_{number}.json  # Individual PR detail files
└── Slack/
    ├── _meta.json             # Sync metadata (workspace, timestamps)
    └── {channel-name}/
        └── messages.json      # All messages with threads, reactions, usernames
```

## Issue Schema (Jira)

```json
{
  "key": "DS-123",
  "hierarchy_level": 1,
  "project": "DS",
  "summary": "Issue title",
  "description_text": "Markdown-converted description",
  "status": {"name": "In Progress", "category": "In Progress"},
  "issue_type": {"name": "Goal"},
  "assignee": {"name": "Moff Jerjerrod"},
  "parent": {"key": "DS-001", "summary": "Parent title"},
  "comments": [...],
  "jira_url": "https://empire.atlassian.net/browse/DS-123"
}
```

## PR Schema (GitHub)

```json
{
  "number": 12345,
  "repo": "galactic-empire/death-star",
  "title": "[DS-608] Thermal exhaust port remediation phase 1",
  "author": "jerjerrod",
  "author_name": "Moff Jerjerrod",
  "team": "Death Star Engineering",
  "state": "merged",
  "created_at": "2026-02-12T03:36:10Z",
  "merged_at": "2026-02-15T22:47:22Z",
  "url": "https://github.com/galactic-empire/death-star/pull/12345",
  "jira_keys": ["DS-608"],
  "labels": ["structural", "priority-critical"],
  "comments": 5
}
```

## Automation

The `run_daily.sh` script orchestrates all syncs (Jira, GitHub, Slack, Calendar) with logging and independent failure handling:

```bash
# Run manually
./run_daily.sh

# Or install the full automation schedule
crontab Scripts/crontab.txt
```

The full automation pipeline runs on weekday cron schedules:

| Schedule | Script | Purpose |
|----------|--------|---------|
| Weekdays 7:00am | `Sync/run_daily.sh` | Data ingress: Jira, GitHub, Slack, Calendar |
| Weekdays 7:30am | `Scripts/run_morning.sh` | Morning journal via Claude CLI |
| Monday 7:15am | `Scripts/News/run_fetch_news.sh` | RSS news fetch |
| Weekdays 11:00pm | `Scripts/run_memory_update.sh` | Full memory update cycle via Claude CLI |

See `Scripts/crontab.txt` for the installable crontab.

The legacy `run_sync.sh` is still available for running just Jira + GitHub syncs.

## Troubleshooting

**"Jira 401 Unauthorized"**
- Verify email matches your Atlassian account
- Regenerate API token if expired

**"Issue not found"**
- Check issue key is correct
- Verify you have permission to view the issue

**GitHub sync: "Missing or placeholder GITHUB_TOKEN"**
- Ensure `GITHUB_TOKEN` is set in `Sync/.env`
- Token needs `repo` scope (or `public_repo` for public-only orgs)

**GitHub sync: API returns 422**
- The search query may be malformed — run with `--debug` to see the full query
- Check the org name in `config.json` is correct

**GitHub sync: member skipped (no GitHub handle)**
- Add a `github` field to the person's YAML front-matter in `Curated-Context/People/{Name}.md`

**Slack sync: "Missing SLACK_SESSION_TOKEN"**
- Add `SLACK_SESSION_TOKEN` and `SLACK_COOKIE_D` to `Sync/.env`
- Both are required — the xoxc- token won't work without the `d` cookie

**Slack sync: "Slack token expired or invalid"**
- Session tokens expire periodically (typically every few weeks)
- Re-extract from browser DevTools using the instructions above

**Slack sync: "No Slack channels configured"**
- Add channels to `Sync/config.json` under `slack.channels`
- Each channel needs at minimum `name` and `id` fields

**Slack sync: rate limiting**
- The script has built-in rate limiting and retry logic
- If you still hit limits, reduce the number of channels or increase lookback intervals

# RSS News Fetcher

Automated RSS feed fetcher that collects articles from curated tech and AI sources for weekly news digests.

## Setup

The script uses a Python virtual environment with required dependencies:

```bash
# Create virtual environment
python3 -m venv .venv

# Install dependencies
.venv/bin/pip install -r requirements.txt
```

## Usage

### Manual Run
```bash
# Run directly
./run_fetch_news.sh

# Or run the Python script
.venv/bin/python fetch_rss.py
```

### Automated Schedule

The script can be run automatically via cron. For example, to fetch every Monday at 8:15 AM:
```
15 8 * * 1 /path/to/your/ai-context-system/Scripts/News/run_fetch_news.sh
```

## Output

- `rss_digest.json` - Raw JSON data of all fetched articles
- `rss_digest.md` - Formatted markdown summary for easy reading
- `fetch_rss.log` - Execution log with timestamps

## Configuration

Edit `fetch_rss.py` to:
- Add/remove RSS feeds in the `FEEDS` dictionary
- Adjust `DAYS_BACK` to change the lookback period (default: 7 days)
- Modify categories or feed sources

## Feed Categories

- **AI/ML**: OpenAI, Google AI, Hugging Face, Simon Willison, etc.
- **Engineering Leadership**: LeadDev, Pragmatic Engineer, Will Larson, etc.
- **Tech News**: Hacker News, Ars Technica, The Verge, TechCrunch

#!/usr/bin/env python3
"""
RSS Feed Fetcher for News Digest
Fetches articles from curated RSS feeds and saves them for Claude summarisation.
"""

import feedparser
import json
import ssl
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path
import html
import re

# Fix SSL certificate verification on macOS
ssl._create_default_https_context = ssl._create_unverified_context

# Configuration
OUTPUT_DIR = Path(__file__).parent.parent.parent / "Synced-Data" / "News"
DAYS_BACK = 7  # How many days of articles to fetch

# RSS Feed Sources
# Customise these feeds for your own interests. The categories and sources below
# are examples — add, remove, or reorganise to match the topics you care about.
FEEDS = {
    "ai_ml": {
        "Last Week in AI": "https://lastweekin.ai/feed",
        "OpenAI Blog": "https://openai.com/blog/rss.xml",
        "Google AI Blog": "https://blog.google/technology/ai/rss/",
        "Hugging Face Blog": "https://huggingface.co/blog/feed.xml",
        "Simon Willison": "https://simonwillison.net/atom/everything/",
        "Chip Huyen": "https://huyenchip.com/feed.xml",
        "MIT Tech Review AI": "https://www.technologyreview.com/topic/artificial-intelligence/feed",
        "VentureBeat AI": "https://venturebeat.com/category/ai/feed/",
    },
    "engineering_leadership": {
        "LeadDev": "https://leaddev.com/rss.xml",
        "The Pragmatic Engineer": "https://newsletter.pragmaticengineer.com/feed",
        "Will Larson": "https://lethain.com/feeds/",
        "Jacob Kaplan-Moss": "https://jacobian.org/feed/",
        "Camille Fournier": "https://skamille.medium.com/feed",
        "Charity Majors": "https://charity.wtf/feed/",
    },
    "tech_news": {
        "Hacker News (Top)": "https://hnrss.org/best?points=100",
        "Ars Technica": "https://feeds.arstechnica.com/arstechnica/technology-lab",
        "The Verge AI": "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml",
        "TechCrunch AI": "https://techcrunch.com/category/artificial-intelligence/feed/",
    }
}


def clean_html(raw_html: str) -> str:
    """Remove HTML tags and decode entities."""
    if not raw_html:
        return ""
    # Remove HTML tags
    clean = re.sub(r'<[^>]+>', '', raw_html)
    # Decode HTML entities
    clean = html.unescape(clean)
    # Normalise whitespace
    clean = re.sub(r'\s+', ' ', clean).strip()
    return clean


def get_published_date(entry) -> datetime | None:
    """Extract published date from feed entry."""
    for attr in ['published_parsed', 'updated_parsed', 'created_parsed']:
        parsed = getattr(entry, attr, None)
        if parsed:
            try:
                return datetime(*parsed[:6])
            except (TypeError, ValueError):
                continue
    return None


def fetch_feed(name: str, url: str, cutoff_date: datetime) -> list[dict]:
    """Fetch and parse a single RSS feed."""
    articles = []
    try:
        feed = feedparser.parse(url)
        if feed.bozo and not feed.entries:
            print(f"  ⚠️  Error fetching {name}: {feed.bozo_exception}")
            return articles
        
        for entry in feed.entries:
            pub_date = get_published_date(entry)
            
            # Skip articles older than cutoff
            if pub_date and pub_date < cutoff_date:
                continue
            
            # Extract summary/description
            summary = ""
            if hasattr(entry, 'summary'):
                summary = clean_html(entry.summary)
            elif hasattr(entry, 'description'):
                summary = clean_html(entry.description)
            elif hasattr(entry, 'content') and entry.content:
                summary = clean_html(entry.content[0].get('value', ''))
            
            # Truncate long summaries
            if len(summary) > 500:
                summary = summary[:500] + "..."
            
            article = {
                "title": entry.get('title', 'No title'),
                "link": entry.get('link', ''),
                "published": pub_date.isoformat() if pub_date else None,
                "summary": summary,
                "source": name,
            }
            articles.append(article)
        
        print(f"  ✓ {name}: {len(articles)} articles")
    except Exception as e:
        print(f"  ✗ {name}: {e}")
    
    return articles


def main():
    print(f"\n📰 Fetching RSS feeds (past {DAYS_BACK} days)\n")
    
    cutoff_date = datetime.now() - timedelta(days=DAYS_BACK)
    all_articles = {"fetched_at": datetime.now().isoformat(), "categories": {}}
    total_count = 0
    
    for category, feeds in FEEDS.items():
        print(f"\n{category.upper().replace('_', ' ')}:")
        category_articles = []
        
        for name, url in feeds.items():
            articles = fetch_feed(name, url, cutoff_date)
            category_articles.extend(articles)
        
        # Sort by date (newest first)
        category_articles.sort(
            key=lambda x: x['published'] or '1970-01-01',
            reverse=True
        )
        
        all_articles["categories"][category] = category_articles
        total_count += len(category_articles)
    
    # Save to JSON
    output_file = OUTPUT_DIR / "rss_digest.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_articles, f, indent=2, ensure_ascii=False)
    
    # Also create a markdown summary for easier reading
    md_output = OUTPUT_DIR / "rss_digest.md"
    with open(md_output, 'w', encoding='utf-8') as f:
        f.write(f"# RSS Feed Digest\n\n")
        f.write(f"*Fetched: {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n")
        f.write(f"*Period: Past {DAYS_BACK} days*\n")
        f.write(f"*Total articles: {total_count}*\n\n")
        
        for category, articles in all_articles["categories"].items():
            f.write(f"## {category.replace('_', ' ').title()}\n\n")
            
            for article in articles:
                pub = article['published'][:10] if article['published'] else 'Unknown date'
                f.write(f"### [{article['title']}]({article['link']})\n")
                f.write(f"*{article['source']} — {pub}*\n\n")
                if article['summary']:
                    f.write(f"{article['summary']}\n\n")
                f.write("---\n\n")
    
    print(f"\n✅ Done! {total_count} articles saved to:")
    print(f"   - {output_file}")
    print(f"   - {md_output}\n")


if __name__ == "__main__":
    main()

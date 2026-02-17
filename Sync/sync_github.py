#!/usr/bin/env python3
"""
GitHub Activity Sync Script

Fetches merged PRs authored by team members over a configurable lookback period.
Team membership and GitHub handles are read from Curated-Context stubs.

Uses the GitHub Search API with a Personal Access Token for authentication.

Usage:
    python sync_github.py [--lookback DAYS] [--team TEAM_NAME] [--debug]

Options:
    --lookback DAYS     Override the default 14-day lookback window
    --team TEAM_NAME    Sync only a specific team (for testing)
    --debug             Verbose output including API responses

Required Environment Variables:
    GITHUB_TOKEN        Personal Access Token with `repo` scope
                        Create one at: https://github.com/settings/tokens
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import requests
import yaml
from dotenv import load_dotenv

from utils import (
    GITHUB_DIR,
    CURATED_DIR,
    load_config,
    save_config,
    save_json,
    iso_now,
    RateLimiter,
    with_retry,
)

# Load environment variables
load_dotenv(Path(__file__).parent / ".env")

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_API_BASE = "https://api.github.com"

# GitHub search API allows 30 requests/minute for authenticated users
rate_limiter = RateLimiter(calls_per_second=0.5)

# Regex for Jira keys in PR titles
JIRA_KEY_RE = re.compile(r"[A-Z][A-Z0-9]+-\d+")


def get_headers() -> dict[str, str]:
    """Get auth headers for GitHub API."""
    if not GITHUB_TOKEN or GITHUB_TOKEN == "ghp_xxxxxxxxxxxx":
        print("ERROR: Missing or placeholder GITHUB_TOKEN in .env file")
        print("Required: GITHUB_TOKEN (PAT with `repo` scope)")
        print("Create one at: https://github.com/settings/tokens")
        sys.exit(1)
    return {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }


@with_retry(max_attempts=3, initial_delay=2.0)
def github_search_prs(
    query: str, per_page: int = 100, page: int = 1, debug: bool = False
) -> dict[str, Any]:
    """Search GitHub PRs via the search/issues API."""
    rate_limiter.wait()
    url = f"{GITHUB_API_BASE}/search/issues"
    params = {"q": query, "per_page": per_page, "page": page}

    if debug:
        print(f"    API: {url}?q={query}&page={page}&per_page={per_page}")

    response = requests.get(url, headers=get_headers(), params=params)

    if response.status_code == 422:
        print("    WARNING: Search query validation failed (422)")
        if debug:
            print(f"    Response: {response.text[:500]}")
        return {"total_count": 0, "items": []}

    if response.status_code != 200:
        print(f"    ERROR: GitHub API returned {response.status_code}")
        if debug:
            print(f"    Response: {response.text[:500]}")
        return {"total_count": 0, "items": []}

    return response.json()


def parse_front_matter(text: str) -> dict[str, Any]:
    """Parse YAML front-matter from a markdown file."""
    text = text.strip()
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    try:
        return yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError:
        return {}


def parse_team_members(team_name: str) -> list[str]:
    """
    Read a team stub and return the list of member names from the ## Members section.
    Names are extracted from wikilinks: [[Full Name]] or [[Full Name|Alias]].
    """
    team_file = CURATED_DIR / "Teams" / f"{team_name}.md"
    if not team_file.exists():
        print(f"  WARNING: Team stub not found: {team_file}")
        return []

    content = team_file.read_text(encoding="utf-8")
    members: list[str] = []
    in_members_section = False

    for line in content.splitlines():
        if line.strip().startswith("## Members"):
            in_members_section = True
            continue
        if in_members_section:
            if line.strip().startswith("## "):
                break
            match = re.search(r"\[\[([^\]|]+)", line)
            if match:
                members.append(match.group(1).strip())

    return members


def resolve_github_handle(member_name: str) -> dict[str, str | None]:
    """
    Read a person stub and extract the github handle from front-matter.
    Returns {"name": ..., "github": ...} or {"name": ..., "github": None}.
    """
    person_file = CURATED_DIR / "People" / f"{member_name}.md"
    if not person_file.exists():
        print(f"    WARNING: Person stub not found: {person_file}")
        return {"name": member_name, "github": None}

    content = person_file.read_text(encoding="utf-8")
    fm = parse_front_matter(content)
    return {"name": member_name, "github": fm.get("github")}


def fetch_merged_prs(
    org: str, handle: str, cutoff_date: str, debug: bool = False
) -> list[dict[str, Any]]:
    """
    Fetch all merged PRs for a user in the org since the cutoff date.
    Handles pagination for users with many PRs.
    """
    all_items: list[dict[str, Any]] = []
    page = 1
    per_page = 100

    query = f"is:pr is:merged org:{org} author:{handle} merged:>={cutoff_date}"

    while True:
        data = github_search_prs(query, per_page=per_page, page=page, debug=debug)
        items = data.get("items", [])
        all_items.extend(items)

        if debug:
            print(f"    Got {len(items)} items (total_count: {data.get('total_count', 0)})")

        total_count = data.get("total_count", 0)
        if len(all_items) >= total_count or len(items) < per_page:
            break

        page += 1

    return all_items


def extract_pr_data(
    item: dict[str, Any], author_name: str, team: str
) -> dict[str, Any]:
    """Extract structured PR data from a GitHub search result item."""
    html_url = item.get("html_url", "")

    # Parse repo from URL: https://github.com/org/repo/pull/12345
    repo = ""
    url_match = re.search(r"github\.com/([^/]+/[^/]+)/pull/", html_url)
    if url_match:
        repo = url_match.group(1).lower()

    title = item.get("title", "")
    jira_keys = JIRA_KEY_RE.findall(title)

    labels = [label.get("name", "") for label in item.get("labels", [])]

    return {
        "number": item.get("number"),
        "repo": repo,
        "title": title,
        "author": item.get("user", {}).get("login", ""),
        "author_name": author_name,
        "team": team,
        "state": "merged",
        "created_at": item.get("created_at"),
        "merged_at": item.get("pull_request", {}).get("merged_at"),
        "url": html_url,
        "jira_keys": jira_keys,
        "labels": labels,
        "comments": item.get("comments", 0),
    }


def generate_index_md(
    org: str,
    lookback_days: int,
    cutoff_date: str,
    synced_at: str,
    prs_by_team: dict[str, list[dict[str, Any]]],
    total_prs: int,
    total_members: int,
) -> str:
    """Generate human-readable INDEX.md grouped by team then author."""
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    lines = [
        "# GitHub Activity Summary",
        f"**Org:** {org}",
        f"**Period:** {cutoff_date} to {today} ({lookback_days} days)",
        f"**Last synced:** {synced_at}",
        f"**Total PRs merged:** {total_prs} across {total_members} members",
        "",
    ]

    for team_name in sorted(prs_by_team.keys()):
        team_prs = prs_by_team[team_name]
        lines.append(f"## {team_name} ({len(team_prs)} PRs)")
        lines.append("")

        # Group by author
        by_author: dict[str, list[dict[str, Any]]] = {}
        for pr in team_prs:
            author_key = pr.get("author_name", pr.get("author", "Unknown"))
            by_author.setdefault(author_key, []).append(pr)

        for author_name in sorted(by_author.keys()):
            author_prs = by_author[author_name]
            github_handle = author_prs[0].get("author", "")
            lines.append(
                f"### {author_name} ({github_handle}) \u2014 {len(author_prs)} PRs"
            )

            # Sort by merged_at descending
            author_prs.sort(key=lambda p: p.get("merged_at") or "", reverse=True)
            for pr in author_prs:
                repo_short = pr["repo"].split("/")[-1] if "/" in pr["repo"] else pr["repo"]
                merged_date = (pr.get("merged_at") or "")[:10]
                jira_tag = ""
                if pr.get("jira_keys"):
                    jira_tag = f" [{', '.join(pr['jira_keys'])}]"
                lines.append(
                    f"- [{repo_short}#{pr['number']}]({pr['url']}): "
                    f"{pr['title']} (merged {merged_date}){jira_tag}"
                )

            lines.append("")

    return "\n".join(lines)


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Sync GitHub activity for team members")
    parser.add_argument(
        "--lookback",
        type=int,
        help="Override the default lookback period in days",
    )
    parser.add_argument(
        "--team",
        type=str,
        help="Sync only a specific team (for testing)",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Verbose output including API responses",
    )
    args = parser.parse_args()

    config = load_config()
    gh_config = config.setdefault("github", {})

    org = gh_config.get("org", "galactic-empire")
    teams = gh_config.get("teams", [])
    lookback_days = args.lookback or gh_config.get("lookback_days", 14)

    if args.team:
        if args.team not in teams:
            print(f"WARNING: Team '{args.team}' not in config, proceeding anyway")
        teams = [args.team]

    if not teams:
        print("ERROR: No teams configured")
        print("Set 'github.teams' in Sync/config.json")
        sys.exit(1)

    cutoff_date = (
        datetime.now(timezone.utc) - timedelta(days=lookback_days)
    ).strftime("%Y-%m-%d")

    print("GitHub sync started")
    print(f"  Org: {org}")
    print(f"  Teams: {', '.join(teams)}")
    print(f"  Lookback: {lookback_days} days (since {cutoff_date})")

    # Phase 1: Resolve team members and GitHub handles
    all_members: list[dict[str, str | None]] = []
    member_team_map: dict[str, str] = {}  # github_handle -> team_name
    skipped = 0

    for team_name in teams:
        member_names = parse_team_members(team_name)
        for name in member_names:
            info = resolve_github_handle(name)
            if info["github"]:
                all_members.append(info)
                member_team_map[info["github"]] = team_name
            else:
                print(f"    SKIPPED: {name} (no GitHub handle in stub)")
                skipped += 1

    print(f"  Members found: {len(all_members)} ({skipped} skipped - no GitHub handle)")

    if not all_members:
        print("ERROR: No members with GitHub handles found")
        sys.exit(1)

    # Phase 2: Fetch merged PRs per member
    all_prs: list[dict[str, Any]] = []
    prs_by_team: dict[str, list[dict[str, Any]]] = {t: [] for t in teams}
    member_summaries: list[dict[str, Any]] = []

    for member in all_members:
        handle = member["github"]
        name = member["name"]
        team = member_team_map[handle]

        print(f"  Fetching PRs for {handle}...", end=" ", flush=True)
        raw_prs = fetch_merged_prs(org, handle, cutoff_date, debug=args.debug)
        print(f"{len(raw_prs)} PRs")

        member_pr_list: list[dict[str, Any]] = []
        for item in raw_prs:
            pr_data = extract_pr_data(item, name, team)
            all_prs.append(pr_data)
            prs_by_team[team].append(pr_data)
            member_pr_list.append(pr_data)

        member_summaries.append({
            "github": handle,
            "name": name,
            "team": team,
            "pr_count": len(member_pr_list),
        })

    print(f"  Total PRs: {len(all_prs)}")

    # Phase 3: Write output
    GITHUB_DIR.mkdir(parents=True, exist_ok=True)
    pr_dir = GITHUB_DIR / "pull-requests"
    pr_dir.mkdir(parents=True, exist_ok=True)

    synced_at = iso_now()

    # _meta.json
    meta = {
        "org": org,
        "teams": teams,
        "lookback_days": lookback_days,
        "last_synced": synced_at,
        "total_prs": len(all_prs),
        "members_synced": len(all_members),
        "members_skipped": skipped,
    }
    save_json(meta, GITHUB_DIR / "_meta.json")

    # index.json (compact)
    index_data = {
        "org": org,
        "synced_at": synced_at,
        "lookback_days": lookback_days,
        "total_prs": len(all_prs),
        "members": member_summaries,
        "pull_requests": [
            {
                "number": pr["number"],
                "repo": pr["repo"],
                "title": pr["title"],
                "author": pr["author"],
                "author_name": pr["author_name"],
                "team": pr["team"],
                "merged_at": pr["merged_at"],
                "jira_keys": pr["jira_keys"],
                "url": pr["url"],
            }
            for pr in sorted(all_prs, key=lambda p: p.get("merged_at") or "", reverse=True)
        ],
    }
    save_json(index_data, GITHUB_DIR / "index.json")

    # INDEX.md (human-readable)
    index_md = generate_index_md(
        org=org,
        lookback_days=lookback_days,
        cutoff_date=cutoff_date,
        synced_at=synced_at,
        prs_by_team=prs_by_team,
        total_prs=len(all_prs),
        total_members=len(all_members),
    )
    (GITHUB_DIR / "INDEX.md").write_text(index_md, encoding="utf-8")

    # Individual PR files
    for pr in all_prs:
        repo_slug = pr["repo"].replace("/", "_")
        save_json(pr, pr_dir / f"{repo_slug}_{pr['number']}.json")

    # Update config
    gh_config["last_synced"] = synced_at
    gh_config["total_prs"] = len(all_prs)
    save_config(config)

    print(f"  Output: Synced-Data/GitHub/")
    print("GitHub sync complete")


if __name__ == "__main__":
    main()

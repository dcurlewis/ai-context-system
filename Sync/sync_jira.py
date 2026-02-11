#!/usr/bin/env python3
"""
Jira Issue Hierarchy Sync Script

Fetches the entire issue hierarchy under a root issue and stores as JSON files.
Converts Atlassian Document Format (ADF) descriptions to Markdown.

Usage:
    python sync_jira.py [--root ISSUE_KEY] [--full]

Options:
    --root ISSUE_KEY    Override root issue from config (e.g., GOAL-54)
    --full              Force full sync (currently always does full sync)

Required Environment Variables:
    JIRA_EMAIL          Your Atlassian account email
    JIRA_API_TOKEN      API token from https://id.atlassian.com/manage-profile/security/api-tokens
    JIRA_BASE_URL       Your Jira instance URL (e.g., https://your-company.atlassian.net)
"""

import argparse
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from collections import defaultdict

import requests
from dotenv import load_dotenv

from utils import (
    JIRA_DIR,
    load_config,
    save_config,
    save_json,
    iso_now,
    RateLimiter,
    with_retry,
)

# Load environment variables
load_dotenv(Path(__file__).parent / ".env")

JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
JIRA_BASE_URL = os.getenv("JIRA_BASE_URL", "").rstrip("/")

# Rate limiter (~10 requests per second)
rate_limiter = RateLimiter(calls_per_second=10.0)


def get_auth() -> tuple[str, str]:
    """Get auth tuple for Jira API."""
    if not all([JIRA_EMAIL, JIRA_API_TOKEN, JIRA_BASE_URL]):
        print("ERROR: Missing Jira credentials in .env file")
        print("Required: JIRA_EMAIL, JIRA_API_TOKEN, JIRA_BASE_URL")
        print("Get API token from: https://id.atlassian.com/manage-profile/security/api-tokens")
        sys.exit(1)
    return (JIRA_EMAIL, JIRA_API_TOKEN)


@with_retry(max_attempts=3, initial_delay=1.0)
def jira_get(endpoint: str, params: dict[str, Any] | None = None) -> requests.Response:
    """Make a GET request to Jira API."""
    rate_limiter.wait()
    url = f"{JIRA_BASE_URL}/rest/api/3/{endpoint}"
    return requests.get(
        url,
        auth=get_auth(),
        headers={"Accept": "application/json"},
        params=params or {},
    )


@with_retry(max_attempts=3, initial_delay=1.0)
def jira_post(endpoint: str, data: dict[str, Any] | None = None, debug: bool = False) -> requests.Response:
    """Make a POST request to Jira API."""
    rate_limiter.wait()
    url = f"{JIRA_BASE_URL}/rest/api/3/{endpoint}"
    if debug:
        print(f"    POST {url}")
        print(f"    Body: {data}")
    return requests.post(
        url,
        auth=get_auth(),
        headers={"Accept": "application/json", "Content-Type": "application/json"},
        json=data or {},
    )


def fetch_issue(issue_key: str) -> dict[str, Any] | None:
    """Fetch a single issue by key."""
    try:
        response = jira_get(f"issue/{issue_key}")
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            print(f"    Issue {issue_key} not found (404)")
            return None
        elif response.status_code == 401:
            print(f"    Authentication failed (401) - Check your JIRA_EMAIL and JIRA_API_TOKEN")
            print(f"    Response: {response.text[:200]}")
            return None
        elif response.status_code == 403:
            print(f"    Permission denied (403) - You may not have access to {issue_key}")
            print(f"    Response: {response.text[:200]}")
            return None
        else:
            print(f"    Error fetching {issue_key}: HTTP {response.status_code}")
            print(f"    Response: {response.text[:200]}")
            return None
    except Exception as e:
        print(f"    Error fetching {issue_key}: {e}")
        return None


def fetch_children(parent_keys: list[str], filter_prefix: str | None = None) -> list[dict[str, Any]]:
    """Fetch all children of given parent issues using JQL, optionally filtering by key prefix."""
    if not parent_keys:
        return []
    
    all_children: list[dict[str, Any]] = []
    
    # Batch parent keys to avoid 413 errors (max ~100 per query)
    batch_size = 100
    for i in range(0, len(parent_keys), batch_size):
        batch = parent_keys[i:i + batch_size]
        parent_clause = ", ".join(batch)
        
        # Add key filter if specified
        if filter_prefix:
            jql = f"parent in ({parent_clause}) AND key ~ '{filter_prefix}*' ORDER BY key ASC"
        else:
            jql = f"parent in ({parent_clause}) ORDER BY key ASC"
        
        next_page_token = None
        max_results = 100
        
        while True:
            try:
                payload = {
                    "jql": jql,
                    "maxResults": max_results,
                    "fields": ["*all"],
                }
                if next_page_token:
                    payload["nextPageToken"] = next_page_token
                
                response = jira_post("search/jql", payload, debug=False)
                
                if response.status_code != 200:
                    print(f"    Error in search: HTTP {response.status_code}")
                    print(f"    Response: {response.text[:500]}")
                    break
                
                data = response.json()
                issues = data.get("issues", [])
                all_children.extend(issues)
                
                # Check for next page token
                next_page_token = data.get("nextPageToken")
                if not next_page_token:
                    break
                
            except Exception as e:
                print(f"    Error fetching children: {e}")
                break
    
    return all_children


def adf_to_markdown(adf: dict[str, Any] | None) -> str:
    """Convert Atlassian Document Format to Markdown."""
    if not adf or not isinstance(adf, dict):
        return ""
    
    def process_node(node: dict[str, Any], depth: int = 0) -> str:
        if not isinstance(node, dict):
            return str(node) if node else ""
        
        node_type = node.get("type", "")
        content = node.get("content", [])
        text = node.get("text", "")
        
        # Text node
        if node_type == "text":
            result = text
            for mark in node.get("marks", []):
                mark_type = mark.get("type", "")
                if mark_type == "strong":
                    result = f"**{result}**"
                elif mark_type == "em":
                    result = f"*{result}*"
                elif mark_type == "code":
                    result = f"`{result}`"
                elif mark_type == "link":
                    href = mark.get("attrs", {}).get("href", "")
                    result = f"[{result}]({href})"
            return result
        
        # Paragraph
        elif node_type == "paragraph":
            inner = "".join(process_node(c, depth) for c in content)
            return f"{inner}\n\n"
        
        # Headings
        elif node_type == "heading":
            level = node.get("attrs", {}).get("level", 1)
            inner = "".join(process_node(c, depth) for c in content)
            return f"{'#' * level} {inner}\n\n"
        
        # Lists
        elif node_type == "bulletList":
            items = []
            for item in content:
                item_content = "".join(process_node(c, depth + 1) for c in item.get("content", []))
                items.append(f"{'  ' * depth}- {item_content.strip()}")
            return "\n".join(items) + "\n\n"
        
        elif node_type == "orderedList":
            items = []
            for i, item in enumerate(content, 1):
                item_content = "".join(process_node(c, depth + 1) for c in item.get("content", []))
                items.append(f"{'  ' * depth}{i}. {item_content.strip()}")
            return "\n".join(items) + "\n\n"
        
        elif node_type == "listItem":
            return "".join(process_node(c, depth) for c in content)
        
        # Code block
        elif node_type == "codeBlock":
            language = node.get("attrs", {}).get("language", "")
            code_text = "".join(process_node(c, depth) for c in content)
            return f"```{language}\n{code_text}\n```\n\n"
        
        # Blockquote
        elif node_type == "blockquote":
            inner = "".join(process_node(c, depth) for c in content)
            lines = inner.strip().split("\n")
            quoted = "\n".join(f"> {line}" for line in lines)
            return f"{quoted}\n\n"
        
        # Table
        elif node_type == "table":
            rows = []
            for row_node in content:
                if row_node.get("type") == "tableRow":
                    cells = []
                    for cell_node in row_node.get("content", []):
                        cell_content = "".join(process_node(c, depth) for c in cell_node.get("content", []))
                        cells.append(cell_content.strip().replace("|", "\\|"))
                    rows.append("| " + " | ".join(cells) + " |")
            
            if rows:
                header = rows[0]
                separator = "| " + " | ".join(["---"] * len(rows[0].split("|")[1:-1])) + " |"
                body = "\n".join(rows[1:]) if len(rows) > 1 else ""
                return f"{header}\n{separator}\n{body}\n\n"
            return ""
        
        # Mention
        elif node_type == "mention":
            mention_text = node.get("attrs", {}).get("text", "")
            return f"@{mention_text}"
        
        # Emoji
        elif node_type == "emoji":
            short_name = node.get("attrs", {}).get("shortName", "")
            return short_name
        
        # Rule (horizontal line)
        elif node_type == "rule":
            return "---\n\n"
        
        # Hard break
        elif node_type == "hardBreak":
            return "\n"
        
        # Panel/info box
        elif node_type == "panel":
            panel_type = node.get("attrs", {}).get("panelType", "info")
            inner = "".join(process_node(c, depth) for c in content)
            return f"> **{panel_type.upper()}:** {inner.strip()}\n\n"
        
        # Media (images, etc)
        elif node_type in ("media", "mediaSingle", "mediaGroup"):
            return "[Media attachment]\n\n"
        
        # Default: process children
        elif content:
            return "".join(process_node(c, depth) for c in content)
        
        return ""
    
    try:
        result = "".join(process_node(node) for node in adf.get("content", []))
        # Clean up excessive newlines
        while "\n\n\n" in result:
            result = result.replace("\n\n\n", "\n\n")
        return result.strip()
    except Exception as e:
        return f"[Error converting description: {e}]"


def parse_issue(raw_issue: dict[str, Any], hierarchy_level: int) -> dict[str, Any]:
    """Parse a raw Jira issue into our schema."""
    fields = raw_issue.get("fields", {})
    
    # Get parent info
    parent = fields.get("parent")
    parent_info = None
    if parent:
        parent_info = {
            "key": parent.get("key"),
            "summary": parent.get("fields", {}).get("summary", ""),
        }
    
    # Get status
    status = fields.get("status", {})
    status_info = {
        "name": status.get("name", "Unknown"),
        "category": status.get("statusCategory", {}).get("name", "Unknown"),
    }
    
    # Get issue type
    issue_type = fields.get("issuetype", {})
    issue_type_info = {
        "name": issue_type.get("name", "Unknown"),
        "subtask": issue_type.get("subtask", False),
    }
    
    # Get assignee
    assignee = fields.get("assignee")
    assignee_info = None
    if assignee:
        assignee_info = {
            "account_id": assignee.get("accountId"),
            "name": assignee.get("displayName", "Unknown"),
            "email": assignee.get("emailAddress", ""),
        }
    
    # Get reporter
    reporter = fields.get("reporter")
    reporter_info = None
    if reporter:
        reporter_info = {
            "account_id": reporter.get("accountId"),
            "name": reporter.get("displayName", "Unknown"),
        }
    
    # Parse description
    description_adf = fields.get("description")
    description_text = adf_to_markdown(description_adf) if description_adf else ""
    
    # Parse comments
    comments = []
    comment_data = fields.get("comment", {})
    for comment in comment_data.get("comments", []):
        comment_author = comment.get("author", {})
        comment_body = adf_to_markdown(comment.get("body")) if comment.get("body") else ""
        comments.append({
            "id": comment.get("id"),
            "author": comment_author.get("displayName", "Unknown"),
            "created": comment.get("created"),
            "updated": comment.get("updated"),
            "body": comment_body,
        })
    
    # Parse links
    links = []
    for link in fields.get("issuelinks", []):
        link_type = link.get("type", {}).get("name", "")
        if "outwardIssue" in link:
            linked = link["outwardIssue"]
            direction = link.get("type", {}).get("outward", "relates to")
        elif "inwardIssue" in link:
            linked = link["inwardIssue"]
            direction = link.get("type", {}).get("inward", "relates to")
        else:
            continue
        links.append({
            "type": link_type,
            "direction": direction,
            "key": linked.get("key"),
            "summary": linked.get("fields", {}).get("summary", ""),
        })
    
    return {
        "key": raw_issue.get("key"),
        "id": raw_issue.get("id"),
        "hierarchy_level": hierarchy_level,
        "project": fields.get("project", {}).get("key", ""),
        "summary": fields.get("summary", ""),
        "description_text": description_text,
        "status": status_info,
        "issue_type": issue_type_info,
        "priority": fields.get("priority", {}).get("name"),
        "assignee": assignee_info,
        "reporter": reporter_info,
        "created": fields.get("created"),
        "updated": fields.get("updated"),
        "resolved": fields.get("resolutiondate"),
        "parent": parent_info,
        "labels": fields.get("labels", []),
        "links": links,
        "comments": comments,
        "jira_url": f"{JIRA_BASE_URL}/browse/{raw_issue.get('key')}",
    }


def generate_index_md(issues: list[dict[str, Any]], root_keys: list[str]) -> str:
    """Generate human-readable INDEX.md."""
    root_links = ", ".join([f"[{key}]({JIRA_BASE_URL}/browse/{key})" for key in root_keys])
    lines = [
        f"# Jira Issue Hierarchy",
        "",
        f"**Root Issues:** {root_links}",
        f"**Total Issues:** {len(issues)}",
        f"**Last Synced:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
        "",
        "---",
        "",
    ]
    
    # Group by hierarchy level
    by_level: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for issue in issues:
        by_level[issue.get("hierarchy_level", 0)].append(issue)
    
    for level in sorted(by_level.keys()):
        level_issues = by_level[level]
        level_name = {0: "Root", 1: "Company Goals", 2: "Team Goals", 3: "Milestones/Epics"}.get(level, f"Level {level}")
        lines.append(f"## {level_name} ({len(level_issues)} issues)")
        lines.append("")
        
        # Group by status category
        by_status: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for issue in level_issues:
            status_cat = issue.get("status", {}).get("category", "Unknown")
            by_status[status_cat].append(issue)
        
        for status_cat in ["To Do", "In Progress", "Done", "Unknown"]:
            if status_cat not in by_status:
                continue
            status_issues = by_status[status_cat]
            lines.append(f"### {status_cat} ({len(status_issues)})")
            lines.append("")
            
            for issue in sorted(status_issues, key=lambda x: x.get("key", "")):
                key = issue.get("key", "")
                summary = issue.get("summary", "")[:80]
                status = issue.get("status", {}).get("name", "")
                assignee = issue.get("assignee", {})
                assignee_name = assignee.get("name", "Unassigned") if assignee else "Unassigned"
                
                lines.append(f"- [{key}]({JIRA_BASE_URL}/browse/{key}): {summary}")
                lines.append(f"  - Status: {status} | Assignee: {assignee_name}")
            
            lines.append("")
    
    return "\n".join(lines)


def sync_hierarchy(root_keys: list[str], filter_prefix: str | None = None) -> dict[str, Any]:
    """Sync the entire issue hierarchy under multiple root issues."""
    print(f"\n  Root issues: {', '.join(root_keys)}")
    if filter_prefix:
        print(f"  Filtering children by prefix: {filter_prefix}")
    
    all_issues: list[dict[str, Any]] = []
    issues_dir = JIRA_DIR / "issues"
    issues_dir.mkdir(parents=True, exist_ok=True)
    
    # Fetch all root issues
    print("    Fetching root issues...")
    root_parsed_list = []
    for root_key in root_keys:
        root_raw = fetch_issue(root_key)
        if not root_raw:
            print(f"    Warning: Root {root_key} not found, skipping")
            continue
        root_parsed = parse_issue(root_raw, hierarchy_level=0)
        all_issues.append(root_parsed)
        root_parsed_list.append(root_parsed)
        save_json(root_parsed, issues_dir / f"{root_key}.json")
    
    if not root_parsed_list:
        return {"error": "no_roots_found", "issues": 0}
    
    # Traverse hierarchy level by level
    current_level_keys = root_keys
    level = 0
    effort_estimates_filtered = 0
    
    while current_level_keys:
        level += 1
        print(f"    Fetching level {level} children of {len(current_level_keys)} parents...")
        
        # Apply filter only at level 1 (immediate children of roots)
        filter_to_use = filter_prefix if level == 1 else None
        children = fetch_children(current_level_keys, filter_to_use)
        
        if not children:
            break
        
        print(f"    Found {len(children)} issues at level {level}")
        
        next_level_keys = []
        for child_raw in children:
            child_parsed = parse_issue(child_raw, hierarchy_level=level)
            
            # Skip "Effort Estimate" issues
            if child_parsed.get("issue_type", {}).get("name") == "Effort Estimate":
                effort_estimates_filtered += 1
                continue
            
            all_issues.append(child_parsed)
            
            # Only add to next level if key exists
            if child_parsed.get("key"):
                next_level_keys.append(child_parsed["key"])
                # Save individual issue
                save_json(child_parsed, issues_dir / f"{child_parsed['key']}.json")
            else:
                print(f"    Warning: Issue without key: {child_raw.get('id', 'unknown')}")
        
        current_level_keys = next_level_keys
        
        # Safety limit
        if level >= 10:
            print("    Warning: Reached max depth of 10 levels")
            break
    
    # Generate index files
    print(f"    Generating index files...")
    
    index_md = generate_index_md(all_issues, root_keys)
    with open(JIRA_DIR / "INDEX.md", "w") as f:
        f.write(index_md)
    
    # Structured index for programmatic access
    index_json = {
        "root_keys": root_keys,
        "total_issues": len(all_issues),
        "synced_at": iso_now(),
        "issues": [
            {
                "key": i["key"],
                "summary": i["summary"],
                "level": i["hierarchy_level"],
                "status": i["status"]["name"],
                "status_category": i["status"]["category"],
                "parent": i["parent"]["key"] if i["parent"] else None,
            }
            for i in all_issues
        ],
    }
    save_json(index_json, JIRA_DIR / "index.json")
    
    # Metadata
    save_json({
        "root_keys": root_keys,
        "last_synced": iso_now(),
        "total_issues": len(all_issues),
        "jira_base_url": JIRA_BASE_URL,
    }, JIRA_DIR / "_meta.json")
    
    print(f"    Saved {len(all_issues)} issues")
    if effort_estimates_filtered > 0:
        print(f"    Filtered out {effort_estimates_filtered} 'Effort Estimate' issues")
    
    return {"issues": len(all_issues), "levels": level, "filtered": effort_estimates_filtered}


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Sync Jira issue hierarchy")
    parser.add_argument("--root", type=str, action='append', help="Root issue key (can specify multiple times, e.g., --root PROJ-1 --root PROJ-2)")
    parser.add_argument("--filter", type=str, help="Filter children by key prefix (e.g., TEAM-)")
    parser.add_argument("--full", action="store_true", help="Force full sync (default behaviour)")
    parser.add_argument("--debug", action="store_true", help="Show debug information")
    args = parser.parse_args()
    
    # Verify credentials are set
    if args.debug:
        print(f"\nDebug - Credentials Check:")
        print(f"  JIRA_EMAIL: {'[SET]' if JIRA_EMAIL else '[NOT SET]'}")
        print(f"  JIRA_API_TOKEN: {'[SET]' if JIRA_API_TOKEN else '[NOT SET]'}")
        print(f"  JIRA_BASE_URL: {JIRA_BASE_URL or '[NOT SET]'}")
        print()
    
    config = load_config()
    jira_config = config.setdefault("jira", {})
    
    # Support both single root_issue (old) and multiple root_issues (new)
    if args.root:
        root_keys = args.root
    elif "root_issues" in jira_config:
        root_keys = jira_config["root_issues"]
    elif "root_issue" in jira_config:
        root_keys = [jira_config["root_issue"]]
    else:
        root_keys = []
    
    if not root_keys:
        print("ERROR: No root issue(s) specified")
        print("Either pass --root ISSUE_KEY or set 'root_issues' in config.json")
        sys.exit(1)
    
    filter_prefix = args.filter or jira_config.get("filter_prefix")
    
    print("=" * 60)
    print("Jira Issue Hierarchy Sync")
    print("=" * 60)
    
    JIRA_DIR.mkdir(parents=True, exist_ok=True)
    
    result = sync_hierarchy(root_keys, filter_prefix)
    
    if "error" in result:
        print(f"\nSync failed: {result['error']}")
        sys.exit(1)
    
    # Update config (support both old and new formats)
    if len(root_keys) == 1:
        jira_config["root_issue"] = root_keys[0]
    jira_config["root_issues"] = root_keys
    if filter_prefix:
        jira_config["filter_prefix"] = filter_prefix
    jira_config["last_synced"] = iso_now()
    jira_config["total_issues"] = result.get("issues", 0)
    save_config(config)
    
    print()
    print("=" * 60)
    print("Sync Complete!")
    print("=" * 60)
    print(f"  Root issues: {', '.join(root_keys)}")
    if filter_prefix:
        print(f"  Filtered by: {filter_prefix}*")
    print(f"  Total issues: {result.get('issues', 0)}")
    if result.get('filtered', 0) > 0:
        print(f"  Effort Estimates excluded: {result.get('filtered', 0)}")
    print(f"  Hierarchy levels: {result.get('levels', 0)}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Slack Channel Sync Script

Fetches messages from configured Slack channels using Slack's internal web APIs
and the user's session token. Replicates the approach used by the slacksnap
browser extension, but as a standalone script suitable for cron automation.

Usage:
    python sync_slack.py [--channel CHANNEL_NAME] [--lookback DAYS] [--full] [--debug]

Options:
    --channel NAME      Sync a single channel by name (must be in config)
    --lookback DAYS     Override lookback days from config
    --full              Ignore last_synced timestamps; fetch full history window
    --debug             Show debug information including API responses

Required Environment Variables:
    SLACK_SESSION_TOKEN  Session token from Slack web app (xoxc-*)
    SLACK_COOKIE_D       The 'd' cookie from Slack (required for xoxc- tokens)
    SLACK_WORKSPACE_URL  Slack workspace URL (e.g. https://company.slack.com)

Token & Cookie Extraction:
    Open Slack in your browser, press F12 (DevTools), go to Console, and run:

    Token (Console):
    JSON.parse(localStorage.getItem('localConfig_v2')).teams[
        Object.keys(JSON.parse(localStorage.getItem('localConfig_v2')).teams)[0]
    ].token

    Cookie (Console):
    document.cookie.split('; ').find(c => c.startsWith('d=')).slice(2)

    Or get the 'd' cookie from DevTools > Application > Cookies > https://app.slack.com
"""

import argparse
import os
import re
import sys
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any

import requests
from dotenv import load_dotenv

from utils import (
    SLACK_DIR,
    load_config,
    save_config,
    save_json,
    iso_now,
    RateLimiter,
    with_retry,
)

# Load environment variables
load_dotenv(Path(__file__).parent / ".env")

SLACK_TOKEN = os.getenv("SLACK_SESSION_TOKEN", "")
SLACK_COOKIE_D = os.getenv("SLACK_COOKIE_D", "")
SLACK_WORKSPACE_URL = os.getenv("SLACK_WORKSPACE_URL", "https://your-workspace.slack.com").rstrip("/")

# Rate limiters matching slacksnap's approach
history_limiter = RateLimiter(calls_per_second=1.0)  # 1s between history pages
thread_limiter = RateLimiter(calls_per_second=1.25)   # 800ms between thread fetches
user_limiter = RateLimiter(calls_per_second=10.0)     # 100ms between user lookups


class SlackTokenError(Exception):
    """Raised when the Slack session token is invalid or expired."""
    pass


def check_token() -> None:
    """Verify the Slack session token and cookie are set."""
    if not SLACK_TOKEN:
        print("ERROR: Missing SLACK_SESSION_TOKEN in .env file")
        print("Extract from browser DevTools console on Slack:")
        print('  JSON.parse(localStorage.getItem("localConfig_v2")).teams[')
        print('    Object.keys(JSON.parse(localStorage.getItem("localConfig_v2")).teams)[0]')
        print("  ].token")
        sys.exit(1)
    if not SLACK_COOKIE_D:
        print("ERROR: Missing SLACK_COOKIE_D in .env file")
        print("The xoxc- token requires the 'd' cookie from your Slack session.")
        print("Extract from browser DevTools console on Slack:")
        print("  document.cookie.split('; ').find(c => c.startsWith('d=')).slice(2)")
        print("Or: DevTools > Application > Cookies > https://app.slack.com > 'd'")
        sys.exit(1)


def slack_api(endpoint: str, params: dict[str, str], limiter: RateLimiter,
              max_retries: int = 3) -> dict[str, Any]:
    """
    Call a Slack internal API endpoint with rate limiting and retry.

    Uses form-encoded POST (matching how the Slack web client and slacksnap
    call these APIs).
    """
    limiter.wait()

    url = f"{SLACK_WORKSPACE_URL}/api/{endpoint}"
    params["token"] = SLACK_TOKEN

    for attempt in range(1, max_retries + 1):
        try:
            response = requests.post(
                url,
                data=params,
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                cookies={"d": SLACK_COOKIE_D},
                timeout=30,
            )
            data = response.json()

            if not data.get("ok"):
                error = data.get("error", "unknown_error")

                if error in ("invalid_auth", "token_revoked", "not_authed",
                             "account_inactive", "token_expired"):
                    raise SlackTokenError(
                        f"Slack token expired or invalid ({error}). "
                        "Re-extract from browser DevTools."
                    )

                if error == "ratelimited":
                    retry_after = int(data.get("headers", {}).get("Retry-After",
                                      2 ** attempt * 2))
                    if attempt < max_retries:
                        print(f"    Rate limited, waiting {retry_after}s "
                              f"(attempt {attempt}/{max_retries})...")
                        time.sleep(retry_after)
                        continue
                    raise RuntimeError(f"Rate limited after {max_retries} retries")

                raise RuntimeError(f"Slack API {endpoint} failed: {error}")

            return data

        except (requests.ConnectionError, requests.Timeout) as e:
            if attempt < max_retries:
                delay = 2 ** attempt
                print(f"    Connection error: {e}. Retrying in {delay}s "
                      f"(attempt {attempt}/{max_retries})...")
                time.sleep(delay)
                continue
            raise

    raise RuntimeError(f"Failed after {max_retries} attempts")


def fetch_messages(channel_id: str, oldest_unix: int,
                   debug: bool = False) -> list[dict[str, Any]]:
    """
    Fetch all messages from a channel since oldest_unix timestamp.

    Uses conversations.history with cursor-based pagination.
    """
    all_messages: list[dict[str, Any]] = []
    cursor = ""
    page = 0

    while True:
        page += 1
        params: dict[str, str] = {
            "channel": channel_id,
            "limit": "100",
            "oldest": str(oldest_unix),
            "inclusive": "true",
        }
        if cursor:
            params["cursor"] = cursor

        data = slack_api("conversations.history", params, history_limiter)

        messages = data.get("messages", [])
        all_messages.extend(messages)

        if debug:
            print(f"      Page {page}: {len(messages)} messages "
                  f"(total: {len(all_messages)})")

        if not data.get("has_more"):
            break

        cursor = data.get("response_metadata", {}).get("next_cursor", "")
        if not cursor:
            break

    return all_messages


def fetch_thread_replies(channel_id: str, thread_ts: str,
                         oldest_unix: int) -> list[dict[str, Any]]:
    """Fetch all replies in a thread."""
    params: dict[str, str] = {
        "channel": channel_id,
        "ts": thread_ts,
        "limit": "200",
        "oldest": str(oldest_unix),
    }

    data = slack_api("conversations.replies", params, thread_limiter)
    return data.get("messages", [])


def fetch_user(user_id: str) -> dict[str, Any] | None:
    """Fetch a single user's profile."""
    params: dict[str, str] = {"user": user_id}

    try:
        data = slack_api("users.info", params, user_limiter)
        return data.get("user")
    except RuntimeError:
        return None


def resolve_users(user_ids: set[str], debug: bool = False) -> dict[str, str]:
    """
    Resolve a set of user IDs to display names.

    Returns a dict mapping user_id -> display_name.
    """
    user_map: dict[str, str] = {}
    total = len(user_ids)

    if debug:
        print(f"    Resolving {total} users...")

    for i, user_id in enumerate(user_ids, 1):
        user = fetch_user(user_id)
        if user:
            name = (
                user.get("real_name")
                or user.get("profile", {}).get("display_name")
                or user.get("profile", {}).get("real_name")
                or user.get("name")
                or "Unknown User"
            )
            user_map[user_id] = name
        else:
            user_map[user_id] = "Unknown User"

        # Longer pause every 10 users
        if i % 10 == 0 and i < total:
            time.sleep(0.5)

    if debug:
        print(f"    Resolved {len(user_map)} users")

    return user_map


def fetch_channel_info(channel_id: str) -> dict[str, Any] | None:
    """Fetch a single channel's info."""
    params: dict[str, str] = {"channel": channel_id}

    try:
        data = slack_api("conversations.info", params, user_limiter)
        return data.get("channel")
    except RuntimeError:
        return None


def resolve_channels(channel_ids: set[str],
                     debug: bool = False) -> dict[str, str]:
    """
    Resolve a set of channel IDs to channel names.

    Returns a dict mapping channel_id -> channel_name.
    """
    channel_map: dict[str, str] = {}
    if not channel_ids:
        return channel_map

    if debug:
        print(f"    Resolving {len(channel_ids)} channel references...")

    for channel_id in channel_ids:
        info = fetch_channel_info(channel_id)
        if info:
            channel_map[channel_id] = info.get("name", channel_id)
        else:
            channel_map[channel_id] = channel_id

    if debug:
        print(f"    Resolved {len(channel_map)} channels")

    return channel_map


def clean_text(text: str, user_map: dict[str, str] | None = None,
               channel_map: dict[str, str] | None = None) -> str:
    """Clean Slack message text, resolving user mentions and channel links."""
    if not text:
        return ""

    # Resolve user mentions <@U12345> -> @DisplayName
    if user_map:
        text = re.sub(
            r"<@([A-Z0-9]+)>",
            lambda m: "@" + user_map.get(m.group(1), "unknown"),
            text,
        )

    # Resolve channel references <#C12345|channel-name> -> #channel-name
    text = re.sub(r"<#[A-Z0-9]+\|([^>]+)>", r"#\1", text)
    if channel_map:
        text = re.sub(
            r"<#([A-Z0-9]+)>",
            lambda m: "#" + channel_map.get(m.group(1), m.group(1)),
            text,
        )
    else:
        text = re.sub(r"<#([A-Z0-9]+)>", r"#\1", text)

    # Resolve URLs <http://example.com|label> -> [label](http://example.com)
    text = re.sub(r"<(https?://[^|>]+)\|([^>]+)>", r"[\2](\1)", text)
    text = re.sub(r"<(https?://[^>]+)>", r"\1", text)

    # Handle Slack formatting
    text = re.sub(r"<!here\|?[^>]*>", "@here", text)
    text = re.sub(r"<!channel\|?[^>]*>", "@channel", text)
    text = re.sub(r"<!everyone\|?[^>]*>", "@everyone", text)

    return text.strip()


def ts_to_iso(ts: str) -> str:
    """Convert Slack timestamp (e.g. '1753160757.123400') to ISO 8601."""
    try:
        unix_ts = float(ts)
        dt = datetime.fromtimestamp(unix_ts, tz=timezone.utc)
        return dt.isoformat().replace("+00:00", "Z")
    except (ValueError, TypeError, OSError):
        return ts


def sync_channel(channel_id: str, channel_name: str, oldest_unix: int,
                 include_threads: bool = True,
                 debug: bool = False) -> dict[str, Any]:
    """
    Sync a single channel and return structured data.

    Returns a dict with channel metadata and enriched messages.
    """
    print(f"    Fetching messages since {datetime.fromtimestamp(oldest_unix, tz=timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}...")

    raw_messages = fetch_messages(channel_id, oldest_unix, debug)

    if not raw_messages:
        print(f"    No messages found")
        return {"channel": channel_name, "channel_id": channel_id,
                "messages": [], "message_count": 0}

    print(f"    Found {len(raw_messages)} messages")

    # Collect user IDs and channel IDs from messages
    user_ids: set[str] = set()
    channel_ids: set[str] = set()
    thread_replies_cache: dict[str, list[dict[str, Any]]] = {}

    for msg in raw_messages:
        if msg.get("user"):
            user_ids.add(msg["user"])

        msg_text = msg.get("text", "")

        # Collect user mentions
        mentions = re.findall(r"<@([A-Z0-9]+)>", msg_text)
        user_ids.update(mentions)

        # Collect channel references without pipe alias: <#C12345>
        chan_refs = re.findall(r"<#([A-Z0-9]+)>", msg_text)
        channel_ids.update(chan_refs)

        # Fetch thread replies
        if (include_threads and msg.get("thread_ts")
                and msg.get("reply_count", 0) > 0
                and msg["ts"] == msg["thread_ts"]):
            replies = fetch_thread_replies(channel_id, msg["thread_ts"],
                                           oldest_unix)
            thread_replies_cache[msg["thread_ts"]] = replies

            for reply in replies:
                if reply.get("user"):
                    user_ids.add(reply["user"])
                reply_text = reply.get("text", "")
                reply_mentions = re.findall(r"<@([A-Z0-9]+)>", reply_text)
                user_ids.update(reply_mentions)
                reply_chan_refs = re.findall(r"<#([A-Z0-9]+)>", reply_text)
                channel_ids.update(reply_chan_refs)

    if debug:
        print(f"    Threads fetched: {len(thread_replies_cache)}")

    # Resolve user IDs to names
    user_map = resolve_users(user_ids, debug)

    # Resolve channel IDs to names
    channel_map = resolve_channels(channel_ids, debug)

    # Build enriched messages
    enriched: list[dict[str, Any]] = []
    for msg in raw_messages:
        # Skip thread replies that appear in the main timeline
        # (they show up as both a reply and a standalone message)
        if (msg.get("thread_ts") and msg.get("thread_ts") != msg.get("ts")
                and not msg.get("subtype")):
            continue

        sender = user_map.get(msg.get("user", ""), "Unknown User")
        text = clean_text(msg.get("text", ""), user_map, channel_map)

        message_data: dict[str, Any] = {
            "ts": msg.get("ts", ""),
            "user_id": msg.get("user", ""),
            "user_name": sender,
            "text": text,
            "timestamp": ts_to_iso(msg.get("ts", "")),
            "thread_ts": msg.get("thread_ts") if msg.get("reply_count", 0) > 0 else None,
            "reply_count": msg.get("reply_count", 0),
            "reactions": [
                {"name": r.get("name", ""), "count": r.get("count", 0)}
                for r in msg.get("reactions", [])
            ],
            "files": [
                {"name": f.get("name", ""), "mimetype": f.get("mimetype", "")}
                for f in msg.get("files", [])
            ],
            "replies": [],
        }

        # Add thread replies
        if msg.get("thread_ts") and msg["ts"] == msg.get("thread_ts"):
            replies_raw = thread_replies_cache.get(msg["thread_ts"], [])
            for reply in replies_raw:
                if reply["ts"] == msg["ts"]:
                    continue  # Skip parent message
                reply_sender = user_map.get(reply.get("user", ""),
                                            "Unknown User")
                reply_text = clean_text(reply.get("text", ""), user_map,
                                        channel_map)
                message_data["replies"].append({
                    "ts": reply.get("ts", ""),
                    "user_id": reply.get("user", ""),
                    "user_name": reply_sender,
                    "text": reply_text,
                    "timestamp": ts_to_iso(reply.get("ts", "")),
                })

        enriched.append(message_data)

    # Sort chronologically
    enriched.sort(key=lambda m: float(m.get("ts", "0")))

    return {
        "channel": channel_name,
        "channel_id": channel_id,
        "messages": enriched,
        "message_count": len(enriched),
    }



def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Sync Slack channel messages")
    parser.add_argument("--channel", type=str,
                        help="Sync a single channel by name")
    parser.add_argument("--lookback", type=int,
                        help="Override lookback days")
    parser.add_argument("--full", action="store_true",
                        help="Ignore last_synced; use full lookback window")
    parser.add_argument("--debug", action="store_true",
                        help="Show debug information")
    args = parser.parse_args()

    check_token()

    config = load_config()
    slack_config = config.setdefault("slack", {})

    # Get channel list from config
    channels = slack_config.get("channels", [])
    if not channels:
        print("ERROR: No Slack channels configured")
        print("Add channels to Sync/config.json under 'slack.channels':")
        print('  {"slack": {"channels": [')
        print('    {"name": "general", "id": "C01234567"}')
        print("  ]}}")
        sys.exit(1)

    lookback_days = args.lookback or slack_config.get("lookback_days", 7)
    include_threads = slack_config.get("include_threads", True)

    # Filter to single channel if specified
    if args.channel:
        channels = [c for c in channels if c.get("name") == args.channel]
        if not channels:
            print(f"ERROR: Channel '{args.channel}' not found in config")
            print("Available channels: " +
                  ", ".join(c.get("name", "?") for c in
                            slack_config.get("channels", [])))
            sys.exit(1)

    print("=" * 60)
    print("Slack Channel Sync")
    print("=" * 60)
    print(f"  Channels: {len(channels)}")
    print(f"  Lookback: {lookback_days} days")
    print(f"  Threads: {'yes' if include_threads else 'no'}")

    SLACK_DIR.mkdir(parents=True, exist_ok=True)
    total_messages = 0
    results: list[dict[str, Any]] = []

    for channel_cfg in channels:
        channel_name = channel_cfg.get("name", "unknown")
        channel_id = channel_cfg.get("id", "")
        enabled = channel_cfg.get("enabled", True)

        if not enabled:
            print(f"\n  [{channel_name}] Skipped (disabled)")
            continue

        if not channel_id:
            print(f"\n  [{channel_name}] Skipped (no channel ID)")
            continue

        print(f"\n  [{channel_name}] (ID: {channel_id})")

        # Determine oldest timestamp
        if args.full:
            oldest = datetime.now(timezone.utc) - timedelta(days=lookback_days)
        else:
            last_synced = slack_config.get("last_synced_channels", {}).get(
                channel_id)
            if last_synced:
                # Use last sync time, but cap at lookback_days
                try:
                    last_dt = datetime.fromisoformat(
                        last_synced.replace("Z", "+00:00"))
                    lookback_dt = (datetime.now(timezone.utc)
                                   - timedelta(days=lookback_days))
                    oldest = max(last_dt, lookback_dt)
                except (ValueError, TypeError):
                    oldest = (datetime.now(timezone.utc)
                              - timedelta(days=lookback_days))
            else:
                oldest = (datetime.now(timezone.utc)
                          - timedelta(days=lookback_days))

        oldest_unix = int(oldest.timestamp())

        try:
            channel_data = sync_channel(
                channel_id, channel_name, oldest_unix,
                include_threads=include_threads, debug=args.debug,
            )

            msg_count = channel_data.get("message_count", 0)
            total_messages += msg_count
            results.append({"channel": channel_name, "messages": msg_count,
                            "status": "OK"})

            # Save channel data
            channel_dir = SLACK_DIR / channel_name
            channel_dir.mkdir(parents=True, exist_ok=True)

            save_json(channel_data, channel_dir / "messages.json")

            # Track last synced time per channel
            last_synced_channels = slack_config.setdefault(
                "last_synced_channels", {})
            last_synced_channels[channel_id] = iso_now()

            print(f"    Saved {msg_count} messages")

            # Delay between channels
            if len(channels) > 1:
                time.sleep(2.5)

        except SlackTokenError as e:
            print(f"    ERROR: {e}")
            results.append({"channel": channel_name, "messages": 0,
                            "status": "FAIL(expired_token)"})
            # Token is expired; no point continuing with other channels
            print("\n  Stopping: Slack token needs to be refreshed")
            break

        except Exception as e:
            print(f"    ERROR: {e}")
            results.append({"channel": channel_name, "messages": 0,
                            "status": f"FAIL({e})"})
            continue

    # Update config with sync metadata
    slack_config["last_synced"] = iso_now()
    slack_config["total_messages"] = total_messages
    save_config(config)

    # Save overall metadata
    save_json({
        "last_synced": iso_now(),
        "total_messages": total_messages,
        "channels_synced": len(results),
        "workspace_url": SLACK_WORKSPACE_URL,
    }, SLACK_DIR / "_meta.json")

    print()
    print("=" * 60)
    print("Sync Complete!")
    print("=" * 60)
    for r in results:
        print(f"  {r['channel']}: {r['messages']} messages ({r['status']})")
    print(f"  Total: {total_messages} messages")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Extract today's calendar events from macOS Calendar.app via EventKit.
Outputs JSON to Synced-Data/Calendar/today.json

Note: This script is macOS-only as it uses the EventKit framework. Users on
Linux or Windows would need to implement their own calendar integration
(e.g. using the Google Calendar API or Microsoft Graph API).

Usage:
    python3 Scripts/calendar-today.py              # Today's events
    python3 Scripts/calendar-today.py 2026-02-12   # Specific date
    python3 Scripts/calendar-today.py tomorrow      # Tomorrow's events

Requires: pyobjc-framework-EventKit
    pip3 install pyobjc-framework-EventKit

macOS Calendar access must be granted to the calling application
(Terminal, iTerm2, etc.) via System Settings > Privacy & Security > Calendars.
"""

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

try:
    from EventKit import (
        EKEventStore, EKEntityTypeEvent,
        EKParticipantStatusAccepted, EKParticipantStatusTentative,
    )
    from Foundation import NSDate
except ImportError:
    print("Error: EventKit not available. Install with:")
    print("  pip3 install pyobjc-framework-EventKit")
    sys.exit(1)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_PATH = PROJECT_ROOT / "Synced-Data" / "Calendar" / "today.json"

# Email used to filter out "self" from attendee lists.
# Falls back to USER_EMAIL env var, then empty string.
# Set this to your company email (e.g. 'johndoe@company.com') either here
# or via the USER_EMAIL environment variable.
USER_EMAIL = os.environ.get("USER_EMAIL", "").lower()

# Optional: comma-separated calendar names to include (empty = all)
CALENDAR_INCLUDE = os.environ.get("CALENDAR_INCLUDE", "").strip()
CALENDAR_EXCLUDE = os.environ.get("CALENDAR_EXCLUDE", "").strip()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def parse_target_date(arg: str | None) -> datetime:
    """Parse CLI argument into a date. Supports YYYY-MM-DD, 'today', 'tomorrow'."""
    if arg is None or arg.lower() == "today":
        return datetime.now()
    if arg.lower() == "tomorrow":
        return datetime.now() + timedelta(days=1)
    return datetime.strptime(arg, "%Y-%m-%d")


def filter_calendars(store, calendars):
    """Apply include/exclude filters to calendar list."""
    if not CALENDAR_INCLUDE and not CALENDAR_EXCLUDE:
        return calendars

    filtered = []
    for cal in calendars:
        title = str(cal.title()).lower() if cal.title() else ""
        if CALENDAR_INCLUDE:
            includes = [c.strip().lower() for c in CALENDAR_INCLUDE.split(",")]
            if any(inc in title for inc in includes):
                filtered.append(cal)
        elif CALENDAR_EXCLUDE:
            excludes = [c.strip().lower() for c in CALENDAR_EXCLUDE.split(",")]
            if not any(exc in title for exc in excludes):
                filtered.append(cal)
    return filtered


def is_resource_calendar(email: str) -> bool:
    """Detect Google Workspace room/resource calendars."""
    return (
        email.startswith("c_") and "@resource.calendar.google.com" in email
        or "@group.calendar.google.com" in email
    )


def name_from_email(email: str) -> str:
    """Extract a readable name from a company email like 'johndoe@company.com' -> 'Johndoe'."""
    local = email.split("@")[0]
    # Handle common patterns: firstname, firstnamelastname, first.last
    return local.replace(".", " ").title()


def extract_attendees(event):
    """Return list of non-self, non-resource attendee dicts with name and email."""
    raw = event.attendees() if event.attendees() else []
    attendees = []
    for att in raw:
        email = str(att.emailAddress()).lower() if att.emailAddress() else ""
        # Skip self
        if USER_EMAIL and USER_EMAIL in email:
            continue
        # Skip room/resource calendars
        if is_resource_calendar(email):
            continue
        # Accept all statuses except explicitly declined (status 3)
        # This keeps accepted, tentative, pending, and unknown statuses
        status = att.participantStatus()
        if status == 3:  # EKParticipantStatusDeclined
            continue
        name = str(att.name()) if att.name() else ""
        # If name is empty or looks like an email, derive from email
        if not name or "@" in name:
            name = name_from_email(email) if email else "Unknown"
        attendees.append({
            "name": name,
            "email": email,
            "email_local": email.split("@")[0] if "@" in email else "",
        })
    return attendees


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def fetch_events(target_date: datetime) -> list[dict]:
    store = EKEventStore.alloc().init()
    # Check authorization status synchronously
    auth_status = EKEventStore.authorizationStatusForEntityType_(EKEntityTypeEvent)
    if auth_status < 3:  # 3 = Authorized, 4 = Full Access
        print("Error: Calendar access not granted.", file=sys.stderr)
        print("Go to System Settings > Privacy & Security > Calendars", file=sys.stderr)
        sys.exit(1)

    day_start = target_date.replace(hour=0, minute=0, second=0, microsecond=0)
    day_end = target_date.replace(hour=23, minute=59, second=59, microsecond=0)

    ns_start = NSDate.dateWithTimeIntervalSince1970_(day_start.timestamp())
    ns_end = NSDate.dateWithTimeIntervalSince1970_(day_end.timestamp())

    all_cals = store.calendarsForEntityType_(EKEntityTypeEvent)
    calendars = filter_calendars(store, all_cals)
    predicate = store.predicateForEventsWithStartDate_endDate_calendars_(
        ns_start, ns_end, calendars
    )
    events = store.eventsMatchingPredicate_(predicate)

    meetings = []
    seen = set()

    for event in events:
        if event.isAllDay():
            continue

        title = str(event.title()) if event.title() else "Untitled"
        start_ts = event.startDate().timeIntervalSince1970()
        end_ts = event.endDate().timeIntervalSince1970()

        start_dt = datetime.fromtimestamp(start_ts)
        end_dt = datetime.fromtimestamp(end_ts)

        # Deduplicate (same title + start)
        key = (title.lower(), start_dt.strftime("%H:%M"))
        if key in seen:
            continue
        seen.add(key)

        attendees = extract_attendees(event)

        # Extract first names for easy matching
        attendee_first_names = []
        for a in attendees:
            parts = a["name"].split()
            if parts:
                attendee_first_names.append(parts[0])

        meetings.append({
            "title": title,
            "start": start_dt.strftime("%H:%M"),
            "end": end_dt.strftime("%H:%M"),
            "start_iso": start_dt.isoformat(),
            "end_iso": end_dt.isoformat(),
            "attendees": attendees,
            "attendee_names": [a["name"] for a in attendees],
            "attendee_first_names": attendee_first_names,
        })

    meetings.sort(key=lambda m: m["start"])
    return meetings


def main():
    arg = sys.argv[1] if len(sys.argv) > 1 else None
    target = parse_target_date(arg)
    date_str = target.strftime("%Y-%m-%d")
    day_name = target.strftime("%A")

    meetings = fetch_events(target)

    output = {
        "date": date_str,
        "day": day_name,
        "fetched_at": datetime.now().isoformat(),
        "meeting_count": len(meetings),
        "meetings": meetings,
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(output, indent=2))
    print(f"Wrote {len(meetings)} meetings for {day_name} {date_str} to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()

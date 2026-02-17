"""
Shared utilities for AI-Context sync scripts.

Provides:
- Rate limiting for API calls
- Retry decorator for transient failures
- ISO timestamp utilities
- Config file management
"""

import functools
import json
import threading
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, TypeVar

import requests

T = TypeVar("T")

# Paths
SYNC_DIR = Path(__file__).parent
CONFIG_FILE = SYNC_DIR / "config.json"
DATA_DIR = SYNC_DIR.parent / "Synced-Data"
SLACK_DIR = DATA_DIR / "Slack"
JIRA_DIR = DATA_DIR / "Jira"
GITHUB_DIR = DATA_DIR / "GitHub"
CURATED_DIR = SYNC_DIR.parent / "Curated-Context"


def iso_now() -> str:
    """Return current UTC time as ISO 8601 string with Z suffix."""
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_config() -> dict[str, Any]:
    """Load config from config.json, or return empty dict if missing."""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_config(config: dict[str, Any]) -> None:
    """Save config to config.json with consistent formatting."""
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)
        f.write("\n")


def save_json(data: dict[str, Any], path: Path) -> None:
    """Save data to JSON file, creating parent directories if needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


class RateLimiter:
    """
    Thread-safe rate limiter using minimum interval between calls.
    
    Usage:
        limiter = RateLimiter(calls_per_second=1.0)
        for item in items:
            limiter.wait()
            make_api_call(item)
    """

    def __init__(self, calls_per_second: float = 1.0):
        self.min_interval = 1.0 / calls_per_second
        self.last_call = 0.0
        self._lock = threading.Lock()

    def wait(self) -> None:
        """Wait if necessary to respect rate limit."""
        with self._lock:
            now = time.time()
            elapsed = now - self.last_call
            if elapsed < self.min_interval:
                time.sleep(self.min_interval - elapsed)
            self.last_call = time.time()


def with_retry(
    max_attempts: int = 3,
    backoff_factor: float = 2.0,
    initial_delay: float = 1.0,
    retryable_exceptions: tuple = (ConnectionError, TimeoutError, requests.exceptions.RequestException),
    retryable_status_codes: tuple = (429, 500, 502, 503, 504),
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """
    Decorator that retries a function on transient failures.
    
    Uses exponential backoff between retry attempts.
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            delay = initial_delay
            last_exception: Exception | None = None
            
            for attempt in range(1, max_attempts + 1):
                try:
                    result = func(*args, **kwargs)
                    
                    # Check if result is a Response with retryable status
                    if isinstance(result, requests.Response):
                        if result.status_code in retryable_status_codes:
                            retry_after = result.headers.get("Retry-After")
                            if retry_after:
                                try:
                                    delay = float(retry_after)
                                except ValueError:
                                    pass
                            
                            if attempt < max_attempts:
                                print(f"  Attempt {attempt} got {result.status_code}. Retrying in {delay:.1f}s...")
                                time.sleep(delay)
                                delay *= backoff_factor
                                continue
                    
                    return result
                    
                except retryable_exceptions as e:
                    last_exception = e
                    if attempt < max_attempts:
                        print(f"  Attempt {attempt} failed: {e}. Retrying in {delay:.1f}s...")
                        time.sleep(delay)
                        delay *= backoff_factor
                    else:
                        raise
            
            if last_exception:
                raise last_exception
            raise RuntimeError("Retry loop exited unexpectedly")
        
        return wrapper
    return decorator

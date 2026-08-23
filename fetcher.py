"""
Fetcher module for retrieving and caching web pages.
"""

import logging
import random
import time

import requests_cache
from requests import Request
from requests.adapters import HTTPAdapter
from urllib3 import Retry

import config

log = logging.getLogger("fetcher")

# Sentinel: 0.0 means no requests have been made yet, it relies on time.monotonic()
# never returning a value near zero in order to avoid delaying the first request.
_last_request_ts = 0.0

retry_strategy = Retry(
    total=4,
    backoff_factor=1,
    backoff_jitter=1,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET"],
    respect_retry_after_header=True,
)

adapter = HTTPAdapter(max_retries=retry_strategy)

session = requests_cache.CachedSession(
    config.CACHE_DB_PATH,
    backend="sqlite",
    allowable_methods=["GET"],
    allowable_codes=[200, 302],
    headers={"User-Agent": config.USER_AGENT},
)

session.mount("http://", adapter)
session.mount("https://", adapter)


def _refresh_cache(url: str, force_refresh: bool = False) -> None:
    """Delete a URL from the cache, if it exists."""
    key = session.cache.create_key(Request("GET", url))
    cached_response = session.cache.get_response(key)

    if not cached_response:
        return

    if cached_response.status_code == 200 or force_refresh:
        session.cache.delete(key)
        log.debug("Deleted %s from cache", url)
    else:
        log.debug("Refresh skipped for %s (cached %s)", url, cached_response.status_code)


def _rate_limit():
    """Enforce a delay between un-cached requests."""
    global _last_request_ts
    elapsed = time.monotonic() - _last_request_ts

    delay = random.uniform(
        config.REQUEST_MIN_DELAY_SECONDS, config.REQUEST_MAX_DELAY_SECONDS
    )

    wait = delay - elapsed
    if wait > 0:
        time.sleep(wait)

    _last_request_ts = time.monotonic()


def fetch(url: str, refresh_cache: bool = False, force_refresh: bool = False) -> tuple[str | None, bool]:
    """Fetch a URL and return the HTML content and a boolean indicating if the ID is valid."""
    if refresh_cache or force_refresh:
        _refresh_cache(url, force_refresh=force_refresh)

    cached = session.cache.contains(url=url)
    if not cached:
        log.info("Fetching %s (not cached)", url)
        _rate_limit()

    resp = session.get(
        url, timeout=config.REQUEST_TIMEOUT_SECONDS, allow_redirects=False
    )

    # Site only ever returns 200 (ID exists) or 302 (ID doesn't exist,
    # redirects to search). Anything else is unexpected and should abort
    # the scrape rather than be silently handled.
    match resp.status_code:
        case 200:
            log.debug("Fetched %s (from_cache=%s)", url, resp.from_cache)
            return resp.text, True
        case 302:
            log.debug("Redirected %s (from_cache=%s)", url, resp.from_cache)
            return None, False
        case _:
            raise RuntimeError(
                f"Unexpected status code {resp.status_code} for URL: {url}"
            )

"""
Application configuration.

Values may be overridden through environment variables loaded from `.env`.
"""

import os
from importlib.metadata import PackageNotFoundError, version

import dotenv

dotenv.load_dotenv()

try:
    APP_VERSION = version("wiki-data-generator")
except PackageNotFoundError:
    APP_VERSION = "0.0.0-dev"


# --------------------------------------------------------------------------------------
# Database configuration
# --------------------------------------------------------------------------------------
DB_PATH = os.environ.get("DATABASE_URL", "sqlite:///./parsed_data.sqlite")

# --------------------------------------------------------------------------------------
# Fetcher configuration
# --------------------------------------------------------------------------------------
BASE_URL = os.environ["FETCHER_BASE_URL"]
ITEM_URL_TEMPLATE = f"{BASE_URL}/Item.asp?id={{id}}"
MONSTER_URL_TEMPLATE = f"{BASE_URL}/Monster.asp?id={{id}}"

ITEM_START_ID = int(os.environ.get("ITEM_START_ID", "1"))
ITEM_END_ID = int(os.environ.get("ITEM_END_ID", "6000"))
MONSTER_START_ID = int(os.environ.get("MONSTER_START_ID", "1"))
MONSTER_END_ID = int(os.environ.get("MONSTER_END_ID", "5000"))

USER_AGENT_SUFFIX = os.environ.get(
    "FETCHER_USER_AGENT_SUFFIX", "(personal wiki-data project)"
)
USER_AGENT = f"wiki-data-fetcher/{APP_VERSION} {USER_AGENT_SUFFIX}"

# requests-cache backend file -- one sqlite db holds the whole HTML cache
CACHE_DB_PATH = os.environ.get("FETCHER_CACHE_DB", "./fetcher_cache.sqlite")

# Seconds between requests. requests-cache only slows down actual
# network hits, not cache hits, so this only bites on first-fetch.
REQUEST_MIN_DELAY_SECONDS = 2.0
REQUEST_MAX_DELAY_SECONDS = 4.0

REQUEST_TIMEOUT_SECONDS = 30.0

# --------------------------------------------------------------------------------------
# Parser configuration
# --------------------------------------------------------------------------------------
# Some monster data is obfuscated/redacted, so we need to stop those monsters from being parsed.
IGNORED_MONSTER_IDS = [2371]

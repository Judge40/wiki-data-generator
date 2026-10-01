"""
Application configuration.

Values may be overridden through environment variables loaded from `.env`.
"""

import os
from importlib.metadata import PackageNotFoundError, version

import dotenv

from db_model import MoralEnum

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
ITEM_END_ID = int(os.environ.get("ITEM_END_ID", "7000"))
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
IGNORED_MONSTER_IDS = {2371}

# --------------------------------------------------------------------------------------
# Monster enrichment configuration
# --------------------------------------------------------------------------------------
BOSS_ONLY_ITEM_IDS = {5909}
BOSS_OVERRIDE_IDS = {285, 1075, 1103, 4282, 4321, 4322}
NPC_OVERRIDE_IDS = {202, 204, 4334}
# Monsters whose stats exactly match any of these templates are NPCs. Keys are Monster attributes.
NPC_STAT_TEMPLATES = [
    {
        "hp": 20,
        "mp": 12,
        "strength": 10,
        "intelligence": 23,
        "wisdom": 10,
        "dexterity": 10,
        "moral": MoralEnum.VERY_POOR,
    },
]

# --------------------------------------------------------------------------------------
# Export configuration
# --------------------------------------------------------------------------------------
EXPORT_DIR = os.environ.get("EXPORT_DIR", "./export")

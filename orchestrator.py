import logging

import config
from fetcher import fetch
from parser import parse_stats
from repository import save_monster

log = logging.getLogger("orchestrator")

URL_TEMPLATES = {
    "item": config.ITEM_URL_TEMPLATE,
    "monster": config.MONSTER_URL_TEMPLATE,
}


def scrape(fetch_type: str, fetch_id: int) -> dict | None:
    """Fetch and parse an item/monster.
    Returns the parsed stats, or None if no entity exists for the given id.
    """
    url = URL_TEMPLATES[fetch_type].format(id=fetch_id)

    html, is_valid = fetch(url)
    if not is_valid:
        log.info("No %s found for id %s", fetch_type, fetch_id)
        return None

    log.info("Found %s %s", fetch_type, fetch_id)

    return parse_stats(fetch_id, fetch_type, html)

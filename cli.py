import argparse
import json
import logging

import config
from fetcher import fetch
from parser import parse_stats

log = logging.getLogger("cli")

URL_TEMPLATES = {
    "item": config.ITEM_URL_TEMPLATE,
    "monster": config.MONSTER_URL_TEMPLATE,
}

argument_parser = argparse.ArgumentParser(
    description="Fetch an item or monster by ID and cache the result."
)
argument_parser.add_argument(
    "fetch_type", choices=["item", "monster"], help="The kind of entity to fetch"
)
argument_parser.add_argument("fetch_id", type=int, help="The ID of the entity to fetch")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s.%(msecs)03d | %(levelname)s | %(name)s | %(message)s",
        datefmt="%H:%M:%S",
    )

    args = argument_parser.parse_args()
    fetch_type = args.fetch_type
    fetch_id = args.fetch_id

    url = URL_TEMPLATES[fetch_type].format(id=fetch_id)

    html, is_valid = fetch(url)

    if not is_valid:
        log.info("No %s found for id %s", fetch_type, fetch_id)
        raise SystemExit(1)

    log.info("Found %s %s", fetch_type, fetch_id)

    stats = parse_stats(fetch_id, fetch_type, html)

    log.info("Stats: %s", json.dumps(stats, indent=2))

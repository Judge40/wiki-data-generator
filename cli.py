import argparse
import json
import logging

from orchestrator import scrape

log = logging.getLogger("cli")

argument_parser = argparse.ArgumentParser(
    description="Fetch an item or monster by ID and cache the result."
)
argument_parser.add_argument(
    "fetch_type", choices=["item", "monster"], help="The kind of entity to fetch"
)
argument_parser.add_argument("fetch_id", type=int, help="The ID of the entity to fetch")
argument_parser.add_argument(
    "-r", "--refresh", action="store_true", help="Refresh the cache for this entity"
)
argument_parser.add_argument(
    "-f", "--force", action="store_true", help="Force refresh the cache for this entity"
)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s.%(msecs)03d | %(levelname)s | %(name)s | %(message)s",
        datefmt="%H:%M:%S",
    )

    args = argument_parser.parse_args()
    stats = scrape(
        args.fetch_type,
        args.fetch_id,
        refresh_cache=args.refresh,
        force_refresh=args.force,
    )

    if stats is None:
        raise SystemExit(1)

    log.info("Stats: %s", json.dumps(stats, indent=2))

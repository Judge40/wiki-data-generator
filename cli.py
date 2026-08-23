import argparse
import json
import logging

from orchestrator import scrape, scrape_many

log = logging.getLogger("cli")

argument_parser = argparse.ArgumentParser(
    description="Fetch item(s) or monster(s) and cache the result(s)."
)
subparsers = argument_parser.add_subparsers(dest="command", required=True)


def _add_cache_flags(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "-r", "--refresh", action="store_true", help="Refresh the cache for this entity"
    )
    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="Force refresh the cache for this entity",
    )


item_parser = subparsers.add_parser("item", help="Fetch a single item by ID")
item_parser.add_argument("fetch_id", type=int, help="The ID of the item to fetch")
_add_cache_flags(item_parser)

items_parser = subparsers.add_parser("items", help="Fetch a range of items")
items_parser.add_argument(
    "start_id", type=int, nargs="?", help="First item ID (defaults to config value)"
)
items_parser.add_argument(
    "end_id", type=int, nargs="?", help="Last item ID (defaults to config value)"
)
_add_cache_flags(items_parser)


monster_parser = subparsers.add_parser("monster", help="Fetch a single monster by ID")
monster_parser.add_argument("fetch_id", type=int, help="The ID of the monster to fetch")
_add_cache_flags(monster_parser)

monsters_parser = subparsers.add_parser("monsters", help="Fetch a range of monsters")
monsters_parser.add_argument(
    "start_id", type=int, nargs="?", help="First monster ID (defaults to config value)"
)
monsters_parser.add_argument(
    "end_id", type=int, nargs="?", help="Last monster ID (defaults to config value)"
)
_add_cache_flags(monsters_parser)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s.%(msecs)03d | %(levelname)s | %(name)s | %(message)s",
        datefmt="%H:%M:%S",
    )

    args = argument_parser.parse_args()

    if args.command in ("item", "monster"):
        stats = scrape(
            args.command,
            args.fetch_id,
            refresh_cache=args.refresh,
            force_refresh=args.force,
        )

        if stats is None:
            raise SystemExit(1)

        log.info("Stats: %s", json.dumps(stats, indent=2))
    else:
        fetch_type = args.command[:-1]  # "items" -> "item", "monsters" -> "monster"
        results = scrape_many(
            fetch_type,
            start_id=args.start_id,
            end_id=args.end_id,
            refresh_cache=args.refresh,
            force_refresh=args.force,
        )

        log.info("Scraped %s %s(s) with %s invalid", results[0], fetch_type, results[1])

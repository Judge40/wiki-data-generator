import logging

import config
from db_model import Monster, MonsterTypeEnum, MoralEnum, RaceEnum
from fetcher import fetch
from parser import parse_stats
from repository import get_all_monsters, save_item, save_monster, update_monster

log = logging.getLogger("orchestrator")

URL_TEMPLATES = {
    "item": config.ITEM_URL_TEMPLATE,
    "monster": config.MONSTER_URL_TEMPLATE,
}

DEFAULT_ID_RANGES = {
    "item": (config.ITEM_START_ID, config.ITEM_END_ID),
    "monster": (config.MONSTER_START_ID, config.MONSTER_END_ID),
}


def scrape(
    fetch_type: str,
    fetch_id: int,
    refresh_cache: bool = False,
    force_refresh: bool = False,
) -> dict | None:
    """Fetch and parse an item/monster.
    Returns the parsed stats, or None if no entity exists for the given id.
    """
    url = URL_TEMPLATES[fetch_type].format(id=fetch_id)

    html, is_valid = fetch(
        url, refresh_cache=refresh_cache, force_refresh=force_refresh
    )
    if not is_valid:
        log.debug("No %s found for id %s", fetch_type, fetch_id)
        return None

    log.debug("Found %s %s", fetch_type, fetch_id)

    try:
        stats = parse_stats(fetch_id, fetch_type, html)
    except RuntimeError as e:
        if fetch_type == "monster" and fetch_id in config.IGNORED_MONSTER_IDS:
            log.info(
                "Skipping monster %s due to known obfuscation/redaction: %s",
                fetch_id,
                e,
            )
            return None
        else:
            raise

    if fetch_type == "monster":
        save_monster(stats)
    elif fetch_type == "item":
        save_item(stats)

    return stats


def scrape_many(
    fetch_type: str,
    start_id: int | None = None,
    end_id: int | None = None,
    refresh_cache: bool = False,
    force_refresh: bool = False,
) -> tuple[int, int]:
    """Scrape a range of ids for the given entity type.

    start_id/end_id default to the configured range for fetch_type when omitted.
    Returns a tuple of (number found, number invalid).
    """
    default_start, default_end = DEFAULT_ID_RANGES[fetch_type]
    start_id = default_start if start_id is None else start_id
    end_id = default_end if end_id is None else end_id
    target_range = range(start_id, end_id + 1)

    found = 0
    invalid = 0
    for fetch_id in target_range:
        stats = scrape(
            fetch_type,
            fetch_id,
            refresh_cache=refresh_cache,
            force_refresh=force_refresh,
        )
        if stats is not None:
            found += 1
        else:
            invalid += 1

    log.debug(
        "Scraped %s %s(s) (with %s invalid) in range %s-%s",
        found,
        fetch_type,
        invalid,
        target_range.start,
        target_range.stop - 1,
    )
    return found, invalid


def _get_monster_race(monster: Monster) -> RaceEnum | None:
    races = set()

    if not monster.maps and not monster.monster_items:
        return None

    for map in monster.maps:
        races.add(map.race)

    for item in monster.monster_items:
        races.add(item.item.race)

    # Remove neutral so we can identify human or devil races more accurately.
    races.discard(RaceEnum.NEUTRAL)
    return races.pop() if len(races) == 1 else RaceEnum.NEUTRAL


def _get_monster_type(monster: Monster) -> MonsterTypeEnum:
    if any(item.item_id in config.BOSS_ONLY_ITEM_IDS for item in monster.monster_items):
        return MonsterTypeEnum.BOSS

    if monster.moral == MoralEnum.NONE and not monster.monster_items:
        return MonsterTypeEnum.NPC

    return MonsterTypeEnum.MONSTER


def enrich_monsters():
    log.info("Enriching monsters...")
    monsters = get_all_monsters()
    for monster in monsters:
        update_monster(
            monster.id,
            race=_get_monster_race(monster),
            type=_get_monster_type(monster),
        )

    log.info("Enriched %s monster(s)", len(monsters))

import logging
import re

from bs4 import BeautifulSoup

log = logging.getLogger("parser")

ITEM_INFO_SELECTOR = "#pagecontent .iteminfo"
MONSTER_INFO_SELECTOR = "#pagecontent #monsterinfo"
NAME_SELECTOR = f"{MONSTER_INFO_SELECTOR} .name"

NEUTRAL_RACE = "Human & Devil"

REQUIRED_MONSTER_STATS = ("str", "intel", "offensive_dex", "defensive_dex", "moral")


def parse_stats(id: int, type: str, html: str) -> dict:
    """Given an HTML page for an item or monster, return a dict of stats."""
    log.debug("Parsing stats for %s %s", type, id)
    soup = BeautifulSoup(html, "lxml")

    if type == "item":
        return _parse_item_stats(id, soup)
    elif type == "monster":
        return _parse_monster_stats(id, soup)
    else:
        raise RuntimeError("Unknown type, unable to parse.")


def _parse_item_stats(id: int, soup: BeautifulSoup) -> dict:
    """Given a BeautifulSoup object for an item page, return a dict of item stats."""

    name_el = soup.select_one(NAME_SELECTOR)
    if name_el is None:
        raise RuntimeError(f"Item page {id} is missing required field: name")

    itemdata_elements = soup.select(f"{ITEM_INFO_SELECTOR} .itemdata")
    item_type = (
        itemdata_elements[0].get_text(strip=True) if itemdata_elements[0] else None
    )

    match = (
        re.search(f"^(Human|Devil|{NEUTRAL_RACE}) ([a-z A-Z]+)$", item_type)
        if item_type
        else None
    )
    if match is None:
        raise RuntimeError(f"Unrecognised item {id} race/type text: {item_type!r}")

    race = "Neutral" if match.group(1) == NEUTRAL_RACE else match.group(1)

    stats = _parse_label_value_block(itemdata_elements[1])
    if "weight" not in stats:
        raise RuntimeError(f"Item page {id} is missing required stat: weight")

    reqs_el = soup.select_one(f"{ITEM_INFO_SELECTOR} .itemreq")
    reqs = _parse_label_value_block(reqs_el)

    result = {
        "id": id,
        "name": name_el.get_text(strip=True),
        "race": race,
        "type": match.group(2),
    }
    result.update(stats.items())
    result.update(reqs.items())

    log.debug("Parsed item %s: %r", id, result)
    return result


def _parse_monster_stats(id: int, soup: BeautifulSoup) -> dict:
    """Given a BeautifulSoup object for an monster page, return a dict of monster stats."""

    name_el = soup.select_one(NAME_SELECTOR)
    if name_el is None:
        raise RuntimeError(f"Monster page {id} is missing required field: name")

    hp_el = soup.select_one(f"{MONSTER_INFO_SELECTOR} #overview #hp")
    mp_el = soup.select_one(f"{MONSTER_INFO_SELECTOR} #overview #mp")

    stat_elements = soup.select(f"{MONSTER_INFO_SELECTOR} .stat .stat-req")
    stats = _parse_label_value_elements(stat_elements)

    missing = [stat for stat in REQUIRED_MONSTER_STATS if stat not in stats]
    if hp_el is None:
        missing.append("hp")
    if mp_el is None:
        missing.append("mp")
    if missing:
        raise RuntimeError(
            f"Monster page {id} is missing required stat(s): {', '.join(missing)}"
        )

    # hp/mp presence is already guaranteed above, narrow for the type checker.
    assert hp_el is not None
    assert mp_el is not None

    locations = soup.select("#pagecontent #monstermap ul li")

    result = {
        "id": id,
        "name": name_el.get_text(strip=True),
        "hp": _extract_number(hp_el.get_text(strip=True)),
        "mp": _extract_number(mp_el.get_text(strip=True)),
        "strength": stats["str"],
        "intelligence": stats["intel"],
        "offensive_dexterity": stats["offensive_dex"],
        "defensive_dexterity": stats["defensive_dex"],
        "moral": stats["moral"],
        "maps": [location.get_text(strip=True) for location in locations],
    }

    log.debug("Parsed monster %s: %r", id, result)
    return result


def _extract_number(text: str | None) -> int | None:
    """'124 hp' -> 124. Handles None gracefully for missing elements."""
    if text is None:
        return None
    match = re.search(r"\d+", text)
    return int(match.group()) if match else None


def _parse_label_value_line(text: str) -> tuple[str, str] | None:
    """'Str :  320' -> ('str', '320'). Returns None if the line isn't a label:value pair."""
    text = text.strip()
    if not text or ":" not in text:
        return None
    label, _, value = text.partition(":")
    key = label.strip().lower().replace(". ", "_").replace(" ", "_")
    return key, value.strip()


def _parse_label_value_block(element) -> dict:
    """For item pages: one element, lines joined by <br>."""
    if element is None:
        return {}
    text = element.get_text(separator="\n", strip=True)
    result = {}
    for line in text.splitlines():
        parsed = _parse_label_value_line(line)
        if parsed:
            key, value = parsed
            result[key] = value
    return _expand_ranges(result)


def _parse_label_value_elements(elements) -> dict:
    """For monster pages: one element per line, e.g. .stat .stat-req spans."""
    result = {}
    for el in elements:
        parsed = _parse_label_value_line(el.get_text(strip=True))
        if parsed:
            key, value = parsed
            result[key] = value
    return _expand_ranges(result)


def _split_range(value: str) -> tuple[int, int] | int:
    """'63~83' -> (63, 83). Plain '18' -> 18 (unchanged, not everything is a range)."""
    if "~" in value:
        low, _, high = value.partition("~")
        return int(low.strip()), int(high.strip())
    return int(value) if value.isdigit() else value


def _expand_ranges(stats: dict) -> dict:
    """Any key holding a '~' range gets split into <key>_min/<key>_max,
    everything else passes through unchanged."""
    result = {}
    for key, value in stats.items():
        split = _split_range(value)
        if isinstance(split, tuple):
            result[f"{key}_min"] = split[0]
            result[f"{key}_max"] = split[1]
        else:
            result[key] = split
    return result

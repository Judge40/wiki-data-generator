import logging
import re

from bs4 import BeautifulSoup

log = logging.getLogger("parser")

ITEM_INFO_SELECTOR = "#pagecontent .iteminfo"
MONSTER_INFO_SELECTOR = "#pagecontent #monsterinfo"
MONSTER_ITEMS_SELECTOR = "#pagecontent #monsteritems"
ITEM_DROP_SELECTOR = f"{MONSTER_ITEMS_SELECTOR} li"
MONSTER_MODEL_SELECTOR = "#pagecontent #monstermodel"
CRAFT_RECIPE_SELECTOR = "#pagecontent #itemcraftrecipe"
NAME_SELECTOR = f"{MONSTER_INFO_SELECTOR} .name"
UPGRADE_INFO_SELECTOR = "#pagecontent #itemupgradeused"

NOT_UPGRADE_TEXT = "not used to upgrade"

NEUTRAL_RACE = "Human & Devil"

REQUIRED_MONSTER_STATS = (
    "str",
    "offensive_str",
    "defensive_str",
    "intel",
    "offensive_intel",
    "defensive_intel",
    "wisdom",
    "dex",
    "offensive_dex",
    "defensive_dex",
    "moral",
)

ITEM_REQ_FIELDS = {
    "req_str": "required_strength",
    "req_int": "required_intelligence",
    "req_wis": "required_wisdom",
    "req_dex": "required_dexterity",
    "req_con": "required_constitution",
    "req_skill": "required_skill",
}


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
    item_type = match.group(2)

    stats = _parse_label_value_block(itemdata_elements[1])
    if "weight" not in stats:
        raise RuntimeError(f"Item page {id} is missing required stat: weight")

    reqs_el = soup.select_one(f"{ITEM_INFO_SELECTOR} .itemreq")
    reqs = _parse_label_value_block(reqs_el)
    reqs = {ITEM_REQ_FIELDS[k]: v for k, v in reqs.items() if k in ITEM_REQ_FIELDS}

    max_upgrades, requires_skill = _parse_upgrade_info(id, soup)

    if max_upgrades is not None and requires_skill is not None:
        item_type = "Upgrade"
    craft_recipe = _parse_craft_recipe(id, soup)

    result = {
        "id": id,
        "name": name_el.get_text(strip=True),
        "race": race,
        "type": item_type,
        "max_upgrades": max_upgrades,
        "requires_skill": requires_skill,
    }
    result.update(stats.items())
    result.update(reqs.items())
    if craft_recipe:
        result.update(craft_recipe)

    sources = []
    if "craft_recipes" in result:
        sources.append("Crafted")
    if soup.select_one(ITEM_DROP_SELECTOR) is not None:
        sources.append("Drop")
    if sources:
        result["sources"] = sources

    log.debug("Parsed item %s: %r", id, result)
    return result


def _parse_upgrade_info(id: int, soup: BeautifulSoup) -> tuple[int | None, bool | None]:
    """Return (max_upgrades, requires_skill), or (None, None) if not an upgrade."""
    list_els = soup.select(f"{UPGRADE_INFO_SELECTOR} ul")
    text = " ".join(el.get_text(" ", strip=True) for el in list_els).strip()
    if not text or NOT_UPGRADE_TEXT in text.lower():
        return None, None

    max_match = re.search(r"up to \+(\d+)", text, re.IGNORECASE)
    if max_match is None:
        raise RuntimeError(f"Unrecognised item {id} upgrade max text: {text!r}")

    if re.search(r"\buses a skill\b", text, re.IGNORECASE):
        requires_skill = True
    elif re.search(r"\bunaffected by crafting skills?\b", text, re.IGNORECASE):
        requires_skill = False
    else:
        raise RuntimeError(f"Unrecognised item {id} upgrade skill text: {text!r}")

    return int(max_match.group(1)), requires_skill


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

    model_img_el = soup.select_one(f"{MONSTER_MODEL_SELECTOR} img")
    locations = soup.select("#pagecontent #monstermap ul li")

    result = {
        "id": id,
        "name": name_el.get_text(strip=True),
        "hp": _extract_int(hp_el.get_text(strip=True)),
        "mp": _extract_int(mp_el.get_text(strip=True)),
        "strength": stats["str"],
        "offensive_strength": stats["offensive_str"],
        "defensive_strength": stats["defensive_str"],
        "intelligence": stats["intel"],
        "offensive_intelligence": stats["offensive_intel"],
        "defensive_intelligence": stats["defensive_intel"],
        "wisdom": stats["wisdom"],
        "dexterity": stats["dex"],
        "offensive_dexterity": stats["offensive_dex"],
        "defensive_dexterity": stats["defensive_dex"],
        "moral": stats["moral"],
        "model_id": _extract_int(model_img_el.get("src", "")) if model_img_el else None,
        "maps": [location.get_text(strip=True) for location in locations],
        "drops": _parse_monster_drops(id, soup),
    }

    log.debug("Parsed monster %s: %r", id, result)
    return result


def _select_text(soup, selector: str, *, strip: bool = True) -> str | None:
    """Select a single element and get its text, or None if not found."""
    element = soup.select_one(selector)
    if element is None:
        return None
    return element.get_text(strip=strip)


def _parse_monster_drops(id: int, soup: BeautifulSoup) -> list[dict]:
    """Flatten the drop table into a list of
    {monster_id, item_id, map, drop_rate} dicts, one per item/map pairing.
    """
    drops = []
    current_map = None
    for el in soup.select(
        f"{MONSTER_ITEMS_SELECTOR} .mapname, {MONSTER_ITEMS_SELECTOR} li"
    ):
        if "mapname" in el.get("class", []):
            current_map = el.get_text(strip=True)
            continue

        link_el = el.select_one(".monstername a")
        rate_el = el.select_one(".drop-info span")
        if link_el is None or rate_el is None or current_map is None:
            continue

        item_id = _extract_id_reference(link_el.get("href", ""))
        if item_id is None:
            continue

        drops.append(
            {
                "monster_id": id,
                "item_id": item_id,
                "map": current_map,
                "drop_rate": _extract_float(
                    rate_el.get_text(strip=True) if rate_el else None
                ),
            }
        )
    return drops


def _extract_id_reference(href: str) -> int | None:
    """'https://example.com/item.asp?id=123' -> 123."""
    match = re.search(r"[?&]id=(\d+)", href)
    return int(match.group(1)) if match else None


def _extract_float(text: str | None) -> float | None:
    """'13.50%' -> 13.5. Handles None gracefully for missing elements."""
    if text is None:
        return None
    match = re.search(r"[\d.]+", text)
    return float(match.group()) if match else None


def _extract_int(text: str | None) -> int | None:
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


def _split_on_first_repeat(id: int, entries: list[tuple]) -> list[list[tuple]] | None:
    """Split (key, quantity) entries into equal-length recipes at the first repeated key.

    Returns None if the entries can't be split evenly.
    """
    keys = [key for key, _ in entries]
    length = next((i for i, key in enumerate(keys) if key in keys[:i]), None)
    if length is None:
        return [entries] if entries else []

    if len(entries) % length != 0:
        log.warning("Item %s has uneven craft recipes, ignoring.", id)
        return None
    return [entries[i : i + length] for i in range(0, len(entries), length)]


def _parse_craft_materials(id: int, soup: BeautifulSoup) -> list[dict]:
    """
    Parse crafting materials from item page.

    Returns a list of recipes, each a dict with "general" and "specific" material dicts.
    Identical recipes are collapsed; an unsplittable list returns [].
    """
    general_material_entries = []
    general_elements = soup.select(
        f"{CRAFT_RECIPE_SELECTOR} li:has(span.item-general-count)"
    )
    for el in general_elements:
        name = _select_text(el, "div.item-info")
        quantity = _select_text(el, "span.item-general-count")

        if name and quantity:
            general_material_entries.append((name, _extract_int(quantity)))

    specific_entries = []
    specific_elements = soup.select(f"{CRAFT_RECIPE_SELECTOR} li:has(span.item-count)")

    for el in specific_elements:
        item_id = None
        link = el.select_one("div.item-info a")
        if link and link.attrs and "href" in link.attrs:
            match = re.search(r"id=(\d+)", link["href"])
            if match:
                item_id = int(match.group(1))
        quantity = _select_text(el, "span.item-count")

        if item_id and quantity:
            specific_entries.append((item_id, _extract_int(quantity)))

    general_recipes = _split_on_first_repeat(id, general_material_entries)
    specific_recipes = _split_on_first_repeat(id, specific_entries)
    if general_recipes is None or specific_recipes is None:
        return []
    if general_recipes and specific_recipes and len(general_recipes) != len(
        specific_recipes
    ):
        log.warning("Item %s has mismatched craft recipes, ignoring.", id)
        return []

    recipes = []
    for i in range(max(len(general_recipes), len(specific_recipes))):
        recipe = {
            "general": dict(general_recipes[i]) if general_recipes else {},
            "specific": dict(specific_recipes[i]) if specific_recipes else {},
        }
        if recipe not in recipes:
            recipes.append(recipe)
    return recipes


def _parse_craft_recipe(id: int, soup: BeautifulSoup) -> dict | None:
    """
    Parse crafting recipe from item page.

    Returns dict with keys:
    - craft_skill_type: str (Accessory, Armor, Cooking, Potion, Weapon)
    - craft_skill: int (required skill level)
    - craft_item_type: str (item type, e.g., Shoes, Ring)
    - craft_recipes: list of dicts with keys "general" and "specific", each mapping to a dict of materials and quantities

    Returns None if item cannot be crafted.
    """
    # Check if item cannot be crafted
    recipe_li = _select_text(soup, f"{CRAFT_RECIPE_SELECTOR} li")
    if recipe_li and "Cannot be crafted" in recipe_li:
        return None

    skill_type = None
    req_skill = 0
    item_type = _select_text(soup, f"{CRAFT_RECIPE_SELECTOR} span.craft-type")
    if item_type:
        item_type = " ".join(item_type.split())
    if item_type in {"Prepare Skill", "Smelt Skill", "Synthesis Skill"}:
        skill_type = item_type.removesuffix(" Skill")
        item_type = "Material"
    else:
        # Parse craft skill requirement: "Req. Armor Skill : 5".
        skill_req = _select_text(soup, f"{CRAFT_RECIPE_SELECTOR} span.craft-skill-req")
        if skill_req:
            match = re.search(r"Req\.\s+(\w+)\s+Skill\s*:\s*(-?\d+)", skill_req)
            if match:
                skill_type = match.group(1)
                req_skill = int(match.group(2))

    if skill_type is None:
        return None

    recipes = [
        r for r in _parse_craft_materials(id, soup) if r["general"] or r["specific"]
    ]
    if not recipes:
        return None

    return {
        "craft_skill_type": skill_type,
        "craft_skill": req_skill,
        "craft_item_type": item_type,
        "craft_recipes": recipes,
    }

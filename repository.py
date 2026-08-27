import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

import config
from db_model import (
    Armour,
    Base,
    Item,
    ItemTypeEnum,
    Map,
    Monster,
    MoralEnum,
    RaceEnum,
    Weapon,
)

log = logging.getLogger("repository")

engine = create_engine(config.DB_PATH)
Base.metadata.create_all(engine)

ITEM_TYPE_MODELS = {
    ItemTypeEnum.ARMOUR: Armour,
    ItemTypeEnum.AXE: Weapon,
    ItemTypeEnum.BOW: Weapon,
    ItemTypeEnum.KNUCKLE: Weapon,
    ItemTypeEnum.SPEAR: Weapon,
    ItemTypeEnum.STAFF: Weapon,
    ItemTypeEnum.SWORD: Weapon,
}


def _filter_to_columns(model, data: dict) -> dict:
    """Drop any keys that aren't mapped columns on the given model."""
    columns = {c.key for c in model.__mapper__.columns}
    return {key: value for key, value in data.items() if key in columns}


def save_item(item_data: dict) -> None:
    """Upsert parsed item stats."""
    item_type = ItemTypeEnum(item_data["type"])
    item_data = {
        **item_data,
        "race": RaceEnum(item_data["race"]),
        "type": item_type,
    }
    model = ITEM_TYPE_MODELS.get(item_type, Item)
    item_data = _filter_to_columns(model, item_data)
    with Session(engine) as session:
        session.merge(model(**item_data))
        session.commit()
    log.debug("Saved item %s", item_data["id"])


def _prompt_for_map_race(map_name: str) -> RaceEnum | None:
    """Prompt the user to select a race for the given map."""
    options = list(RaceEnum)
    choices = ", ".join(f"{i + 1}={race.value}" for i, race in enumerate(options))
    choices = f"0=Unknown, {choices}"

    while True:
        answer = input(
            f"Map '{map_name}' is new. Select race ({choices}) [default: 0]: "
        ).strip()
        if not answer or answer == "0":
            return None
        if answer.isdigit() and 1 <= int(answer) <= len(options):
            return options[int(answer) - 1]
        print(f"Invalid selection: {answer!r}")


def _get_or_create_map(session: Session, map_name: str) -> Map:
    """Fetch the Map row for map_name, creating it if it doesn't exist."""
    map_obj = session.query(Map).filter_by(name=map_name).one_or_none()
    if map_obj is None:
        map_race = _prompt_for_map_race(map_name)
        map_obj = Map(name=map_name, race=map_race)
        session.add(map_obj)
        session.flush()
    return map_obj


def save_monster(monster_data: dict) -> None:
    """Upsert parsed monster stats and its map associations."""
    map_names = monster_data.get("maps", [])
    monster_data = {**monster_data, "moral": MoralEnum(monster_data["moral"])}
    monster_data = _filter_to_columns(Monster, monster_data)
    with Session(engine) as session:
        monster = session.merge(Monster(**monster_data))
        monster.maps = [_get_or_create_map(session, name) for name in map_names]
        session.commit()
    log.debug(
        "Saved monster %s with maps [%s]", monster_data["id"], ", ".join(map_names)
    )

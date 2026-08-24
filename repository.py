import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

import config
from db_model import (
    Armour,
    Base,
    Item,
    ItemTypeEnum,
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


def save_monster(monster_data: dict) -> None:
    """Upsert parsed monster stats."""
    monster_data = {**monster_data, "moral": MoralEnum(monster_data["moral"])}
    monster_data = _filter_to_columns(Monster, monster_data)
    with Session(engine) as session:
        session.merge(Monster(**monster_data))
        session.commit()
    log.debug("Saved monster %s", monster_data["id"])

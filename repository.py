import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, joinedload

import config
from db_model import (
    Armour,
    Base,
    CraftItemTypeEnum,
    CraftSkillTypeEnum,
    Item,
    ItemRecipe,
    ItemTypeEnum,
    Map,
    Monster,
    MonsterItem,
    MoralEnum,
    RaceEnum,
    Upgrade,
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
    ItemTypeEnum.UPGRADE: Upgrade,
}


def _filter_to_columns(model, data: dict) -> dict:
    """Drop any keys that aren't mapped columns on the given model."""
    columns = {c.key for c in model.__mapper__.columns}
    return {key: value for key, value in data.items() if key in columns}


def _map_specific_materials(specific_materials: dict) -> dict:
    """Convert a dict of specific materials into the format expected by ItemRecipe."""
    mapped = {}
    for i, (material_id, quantity) in enumerate(specific_materials.items(), start=1):
        mapped[f"specific_id_{i}"] = material_id
        mapped[f"specific_quantity_{i}"] = quantity

    return mapped


def save_item(item_data: dict) -> None:
    """Upsert parsed item stats."""
    craft_materials = item_data.get("craft_materials", {})
    general_materials = {
        material.lower(): quantity
        for material, quantity in craft_materials.get("general", {}).items()
    }

    item_type = ItemTypeEnum(item_data["type"])
    craft_skill_type = (
        CraftSkillTypeEnum(item_data["craft_skill_type"])
        if item_data.get("craft_skill_type")
        else None
    )
    craft_item_type = (
        CraftItemTypeEnum(item_data["craft_item_type"])
        if item_data.get("craft_item_type")
        else None
    )
    item_data = {
        **item_data,
        "race": RaceEnum(item_data["race"]),
        "type": item_type,
        "craft_skill_type": craft_skill_type,
        "craft_item_type": craft_item_type,
    }
    model = ITEM_TYPE_MODELS.get(item_type, Item)
    item_data = _filter_to_columns(model, item_data)
    with Session(engine) as session:
        item = session.merge(model(**item_data))
        session.query(ItemRecipe).filter_by(item_id=item.id).delete()

        if craft_skill_type:
            session.add(
                ItemRecipe(
                    item_id=item.id,
                    **general_materials,
                    **_map_specific_materials(craft_materials.get("specific", {})),
                )
            )
        session.commit()
    log.debug("Saved item %s", item_data["id"])


def _get_or_create_map(session: Session, map_name: str) -> Map:
    """Fetch the Map row for map_name, creating it if it doesn't exist."""
    map_obj = session.query(Map).filter_by(name=map_name).one_or_none()
    if map_obj is None:
        map_obj = Map(name=map_name)
        session.add(map_obj)
        session.flush()
    return map_obj


def save_monster(monster_data: dict) -> None:
    """Upsert parsed monster stats, its map associations, and its item drops."""
    map_names = monster_data.get("maps", [])
    drops = monster_data.get("drops", [])
    monster_data = {**monster_data, "moral": MoralEnum(monster_data["moral"])}
    monster_data = _filter_to_columns(Monster, monster_data)
    with Session(engine) as session:
        monster = session.merge(Monster(**monster_data))
        monster.maps = [_get_or_create_map(session, name) for name in map_names]
        monster.monster_items = [
            MonsterItem(
                map_id=_get_or_create_map(session, drop["map"]).id,
                item_id=drop["item_id"],
                drop_rate=drop["drop_rate"],
            )
            for drop in drops
        ]
        session.commit()
    log.debug(
        "Saved monster %s with maps [%s]", monster_data["id"], ", ".join(map_names)
    )


def get_all_monsters() -> list[Monster]:
    """Return every monster, with its maps and item drops eagerly loaded."""
    with Session(engine) as session:
        monsters = (
            session.query(Monster)
            .options(
                joinedload(Monster.maps),
                joinedload(Monster.monster_items).joinedload(MonsterItem.item),
            )
            .all()
        )
        session.expunge_all()
    return monsters


def update_monster(monster_id: int, **fields) -> None:
    """Persist derived/enrichment columns for an already-saved monster."""
    with Session(engine) as session:
        monster = session.get(Monster, monster_id)
        for key, value in fields.items():
            setattr(monster, key, value)
        session.commit()

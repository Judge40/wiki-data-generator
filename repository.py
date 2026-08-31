import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, joinedload

import config
from db_model import (
    Armour,
    Base,
    Item,
    ItemTypeEnum,
    Map,
    Monster,
    MonsterItem,
    MoralEnum,
    RaceEnum,
    RequirementKindEnum,
    Spell,
    SpellLevel,
    SpellRequirement,
    Weapon,
)
from spell_schema import Requirement
from spell_schema import Spell as SpellSchema

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


def _get_or_create_map(session: Session, map_name: str) -> Map:
    """Fetch the Map row for map_name, creating it if it doesn't exist."""
    map_obj = session.query(Map).filter_by(name=map_name).one_or_none()
    if map_obj is None:
        map_obj = Map(name=map_name)
        session.add(map_obj)
        session.flush()
    return map_obj


def _to_requirement_row(req: Requirement, spell_level_id: int) -> SpellRequirement:
    """Recursively convert a validated all/any requirement clause into a row."""
    if req.any is not None:
        return SpellRequirement(
            spell_level_id=spell_level_id,
            kind=RequirementKindEnum.ANY,
            children=[_to_requirement_row(child, spell_level_id) for child in req.any],
        )
    if req.all is not None:
        return SpellRequirement(
            spell_level_id=spell_level_id,
            kind=RequirementKindEnum.ALL,
            children=[_to_requirement_row(child, spell_level_id) for child in req.all],
        )
    if req.level is not None:
        return SpellRequirement(
            spell_level_id=spell_level_id, kind=RequirementKindEnum.LEVEL, value=req.level
        )
    if req.intelligence is not None:
        return SpellRequirement(
            spell_level_id=spell_level_id,
            kind=RequirementKindEnum.INTELLIGENCE,
            value=req.intelligence,
        )
    if req.skill is not None:
        return SpellRequirement(
            spell_level_id=spell_level_id, kind=RequirementKindEnum.SKILL, value=req.skill
        )
    if req.barr is not None:
        return SpellRequirement(
            spell_level_id=spell_level_id, kind=RequirementKindEnum.BARR, value=req.barr
        )
    if req.moral is not None:
        return SpellRequirement(
            spell_level_id=spell_level_id,
            kind=RequirementKindEnum.MORAL,
            value=req.moral,
        )
    return SpellRequirement(
        spell_level_id=spell_level_id,
        kind=RequirementKindEnum.ITEM,
        item_id=req.item.id,
        value=req.item.quantity,
    )


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


def save_spell(spell: SpellSchema) -> None:
    """Upsert a validated spell and its levels."""
    with Session(engine) as session:
        spell_obj = (
            session.query(Spell)
            .filter_by(name=spell.name, race=spell.race)
            .one_or_none()
        )
        if spell_obj is None:
            spell_obj = Spell(name=spell.name, race=spell.race)
            session.add(spell_obj)
        else:
            spell_obj.levels = []
            session.flush()  # delete old levels before inserting the new ones
        spell_obj.school = spell.school
        level_objs = [
            SpellLevel(
                level=level.level,
                range=level.range,
                duration=level.duration,
                power=level.power,
                mp=level.mp,
            )
            for level in spell.levels
        ]
        spell_obj.levels = level_objs
        session.flush()  # assign level_objs their ids so requirements can reference them
        for level, level_obj in zip(spell.levels, level_objs):
            if level.requirements is not None:
                requirements = (
                    level.requirements
                    if isinstance(level.requirements, list)
                    else level.requirements.all
                )
                level_obj.requirements = [
                    _to_requirement_row(req, level_obj.id)
                    for req in requirements
                ]
        session.commit()
    log.debug("Saved spell %s (%s)", spell.name, spell.race.value)

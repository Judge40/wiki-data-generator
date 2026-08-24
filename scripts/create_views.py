"""
Creates/refreshes weapon_view and armour_view for browsing with DB tools.
Not wired into the app - just run this whenever you want the views to exist
or need to pick up a schema change.

Usage:
    python create_views.py
"""

from sqlalchemy import String, cast, literal, select, text

import config
from db_model import Armour, Item, Monster, Weapon
from repository import engine


def create_view(name: str, selectable) -> None:
    sql = selectable.compile(engine, compile_kwargs={"literal_binds": True})
    with engine.begin() as conn:
        conn.execute(text(f"DROP VIEW IF EXISTS {name}"))
        conn.execute(text(f"CREATE VIEW {name} AS {sql}"))
    print(f"Created {name}")


item_url_prefix, item_url_suffix = config.ITEM_URL_TEMPLATE.split("{id}", maxsplit=1)
item_url = literal(item_url_prefix) + cast(Item.id, String) + literal(item_url_suffix)

monster_url_prefix, monster_url_suffix = config.MONSTER_URL_TEMPLATE.split(
    "{id}", maxsplit=1
)
monster_url = (
    literal(monster_url_prefix) + cast(Monster.id, String) + literal(monster_url_suffix)
)


armour_view = select(
    Item.id,
    Item.name,
    Item.race,
    Item.weight,
    Item.type,
    Armour.defense_min,
    Armour.defense_max,
    Armour.durability,
    item_url.label("url"),
).select_from(Item.__table__.join(Armour.__table__, Armour.id == Item.id))


monster_view = select(
    Monster.id,
    Monster.name,
    Monster.hp,
    Monster.mp,
    Monster.strength,
    Monster.intelligence,
    Monster.offensive_dexterity,
    Monster.defensive_dexterity,
    Monster.moral,
    monster_url.label("url"),
).select_from(Monster.__table__)


weapon_view = select(
    Item.id,
    Item.name,
    Item.race,
    Item.weight,
    Item.type,
    Weapon.attack_min,
    Weapon.attack_max,
    Weapon.speed,
    Weapon.durability,
    item_url.label("url"),
).select_from(Item.__table__.join(Weapon.__table__, Weapon.id == Item.id))


if __name__ == "__main__":
    create_view("armour_view", armour_view)
    create_view("monster_view", monster_view)
    create_view("weapon_view", weapon_view)

"""
Creates/refreshes weapon_view and armour_view for browsing with DB tools.
Not wired into the app - just run this whenever you want the views to exist
or need to pick up a schema change.

Usage:
    python create_views.py
"""

from sqlalchemy import String, cast, func, literal, select, text

import config
from db_model import Armour, Item, Map, Monster, MonsterItem, MonsterMap, Weapon
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
monster_maps = (
    select(func.group_concat(Map.name, ", "))
    .select_from(Map)
    .join(MonsterMap, MonsterMap.map_id == Map.id)
    .where(MonsterMap.monster_id == Monster.id)
    .correlate(Monster)
    .scalar_subquery()
)

armour_view = select(Armour, item_url.label("url"))


monster_view = select(Monster, monster_maps.label("maps"), monster_url.label("url"))
monster_drop_view = (
    select(
        Monster.id.label("monster_id"),
        Monster.name.label("monster_name"),
        Map.name.label("map"),
        Item.id.label("item_id"),
        Item.name.label("item_name"),
        (func.min(100, MonsterItem.drop_rate)).label("drop_rate_base"),
        (func.min(100, MonsterItem.drop_rate * 1.1)).label("drop_rate_conti"),
        (func.min(100, MonsterItem.drop_rate * 1.2)).label("drop_rate_ctf"),
        (func.min(100, MonsterItem.drop_rate * 1.3)).label("drop_rate_conti_ctf"),
        item_url.label("item_url"),
    )
    .select_from(MonsterItem)
    .join(MonsterItem.monster)
    .join(MonsterItem.map)
    .join(MonsterItem.item)
)


weapon_view = select(Weapon, item_url.label("url"))


if __name__ == "__main__":
    create_view("armour_view", armour_view)
    create_view("monster_view", monster_view)
    create_view("monster_drop_view", monster_drop_view)
    create_view("weapon_view", weapon_view)

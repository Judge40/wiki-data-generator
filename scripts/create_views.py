"""
Creates/refreshes weapon_view and armour_view for browsing with DB tools.
Not wired into the app - just run this whenever you want the views to exist
or need to pick up a schema change.

Usage:
    python scripts/create_views.py
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


def create_raw_view(name: str, sql: str) -> None:
    """Like create_view, but for hand-written SQL too complex for the SQLAlchemy DSL."""
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


spell_view_sql = """
WITH goods_leaf AS (
    SELECT sr.spell_level_id AS level_id, sr.parent_id, sr.id,
           CASE sr.kind
               WHEN 'BARR' THEN sr.value || ' Barr'
               WHEN 'ITEM' THEN sr.value || ' ' || i.name
           END AS text
    FROM spell_requirement sr
    LEFT JOIN item i ON i.id = sr.item_id
    WHERE sr.kind IN ('BARR', 'ITEM')
),
any_groups AS (
    SELECT sr.spell_level_id AS level_id, sr.id AS ord,
           '(' || GROUP_CONCAT(gl.text, ' or ') || ')' AS text
    FROM spell_requirement sr
    JOIN goods_leaf gl ON gl.parent_id = sr.id
    WHERE sr.kind = 'ANY' AND sr.parent_id IS NULL
    GROUP BY sr.id
),
goods_parts AS (
    SELECT level_id, id AS ord, text FROM goods_leaf WHERE parent_id IS NULL
    UNION ALL
    SELECT level_id, ord, text FROM any_groups
),
goods AS (
    SELECT level_id, GROUP_CONCAT(text, ' and ') AS req_goods
    FROM (SELECT * FROM goods_parts ORDER BY ord)
    GROUP BY level_id
)
SELECT
    spell.name,
    spell.race,
    spell.school,
    spell_level.level,
    spell_level.range,
    spell_level.duration,
    spell_level.power,
    spell_level.mp,
        CASE WHEN spell_level.power > 1
            THEN ROUND(CAST(spell_level.power AS REAL) / NULLIF(spell_level.mp, 0), 2)
        END AS power_per_mp,
    (SELECT value FROM spell_requirement
        WHERE spell_level_id = spell_level.id AND kind = 'LEVEL' AND parent_id IS NULL
    ) AS req_level,
    (SELECT value FROM spell_requirement
        WHERE spell_level_id = spell_level.id AND kind = 'INTELLIGENCE' AND parent_id IS NULL
    ) AS req_intelligence,
    (SELECT value FROM spell_requirement
        WHERE spell_level_id = spell_level.id AND kind = 'SKILL' AND parent_id IS NULL
    ) AS req_skill,
    (SELECT value FROM spell_requirement
        WHERE spell_level_id = spell_level.id AND kind = 'MORAL' AND parent_id IS NULL
    ) AS req_moral,
    goods.req_goods
FROM spell
JOIN spell_level ON spell_level.spell_id = spell.id
LEFT JOIN goods ON goods.level_id = spell_level.id
"""


if __name__ == "__main__":
    create_view("armour_view", armour_view)
    create_view("monster_view", monster_view)
    create_view("monster_drop_view", monster_drop_view)
    create_view("weapon_view", weapon_view)

    create_raw_view("spell_view", spell_view_sql)

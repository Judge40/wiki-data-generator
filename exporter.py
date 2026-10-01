"""Convert database entities into Lua data modules for the wiki."""

import enum
import logging
from pathlib import Path
from typing import Any

import luadata

import config
from db_model import Map, Monster, MonsterTypeEnum

log = logging.getLogger("exporter")

MONSTER_EXCLUDED_FIELDS = {}
MONSTER_EXCLUDED_TYPES = {MonsterTypeEnum.EVENT, MonsterTypeEnum.NPC}


def _plain_value(value: Any) -> Any:
    """Unwrap enum members so luadata serializes them as their string value."""
    if isinstance(value, list):
        return [_plain_value(v) for v in value]
    if isinstance(value, Map):
        return value.name
    return value.value if isinstance(value, enum.Enum) else value


def _to_lua_table(entities: list[Any], fields: list[str]) -> dict[int, dict[str, Any]]:
    return {
        entity.id: {field: _plain_value(getattr(entity, field)) for field in fields}
        for entity in entities
    }


def _write(filename: str, entities: list[Any], fields: list[str]) -> Path:
    output_dir = Path(config.EXPORT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / filename
    table = _to_lua_table(entities, fields)
    content = "return " + luadata.serialize(table, indent="    ") + "\n"
    path.write_text(content, encoding="utf-8")
    log.info("Wrote %s", path)
    return path


def export_monsters(monsters: list[Monster]) -> Path:
    fields = [
        column.key
        for column in Monster.__mapper__.columns
        if column.key not in MONSTER_EXCLUDED_FIELDS
    ] + ["maps"]
    monsters = [m for m in monsters if m.type not in MONSTER_EXCLUDED_TYPES]
    return _write("MonsterData.lua", monsters, fields)

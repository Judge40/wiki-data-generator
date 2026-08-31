"""Pydantic schema for validating the hand-authored spells.yml file."""

from pathlib import Path

import yaml
from pydantic import BaseModel, Field, model_validator

from db_model import RaceEnum, SchoolEnum


class ItemRequirement(BaseModel):
    id: int
    quantity: int


class Requirement(BaseModel):
    """A single all/any requirement clause.

    Exactly one of the leaf fields (level/intelligence/skill/barr/moral/item)
    or a nested group (any/all) must be set.
    """

    level: int | None = None
    intelligence: int | None = None
    skill: int | None = None
    barr: int | None = None
    moral: int | None = None
    item: ItemRequirement | None = None
    any: list["Requirement"] | None = None
    all: list["Requirement"] | None = None

    @model_validator(mode="after")
    def _check_single_field(self) -> "Requirement":
        set_fields = [
            name
            for name in (
                "level",
                "intelligence",
                "skill",
                "barr",
                "moral",
                "item",
                "any",
                "all",
            )
            if getattr(self, name) is not None
        ]
        if len(set_fields) != 1:
            raise ValueError(
                f"Requirement clause must set exactly one field, got {set_fields}"
            )
        return self


class RequirementGroup(BaseModel):
    """Legacy wrapper for requirements written with an explicit ``all`` key."""

    all: list[Requirement]


class SpellLevel(BaseModel):
    level: int = Field(ge=1, le=4)
    range: int
    duration: int | None = None
    power: int
    mp: int
    requirements: list[Requirement] | RequirementGroup | None = None


class Spell(BaseModel):
    name: str
    race: RaceEnum
    school: SchoolEnum
    levels: list[SpellLevel]


class SpellsFile(BaseModel):
    spells: list[Spell]


def load_spells_file(path: str | Path) -> list[Spell]:
    """Load and validate the spells defined in the given YAML file."""
    with open(path, encoding="utf-8") as f:
        raw = yaml.safe_load(f)
    return SpellsFile.model_validate(raw).spells

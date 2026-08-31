import enum
from typing import Any, ClassVar

from sqlalchemy import Enum, ForeignKey, String, UniqueConstraint, case
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class MoralEnum(enum.Enum):
    NONE = "None"
    VERY_POOR = "Very Poor"
    POOR = "Poor"
    GOOD = "Good"
    VERY_GOOD = "Very Good"
    EXCELLENT = "Excellent"


class RaceEnum(enum.Enum):
    HUMAN = "Human"
    DEVIL = "Devil"
    NEUTRAL = "Neutral"


class SchoolEnum(enum.Enum):
    BLUE = "Blue"
    WHITE = "White"
    BLACK = "Black"


class RequirementKindEnum(enum.Enum):
    ALL = "All"
    ANY = "Any"
    LEVEL = "Level"
    INTELLIGENCE = "Intelligence"
    SKILL = "Skill"
    BARR = "Barr"
    MORAL = "Moral"
    ITEM = "Item"


class ItemTypeEnum(enum.Enum):
    ACCESSORY = "Accessory"
    ARMOUR = "Armour"
    AXE = "Axe"
    BOW = "Bow"
    COOKED_DISH = "Cooked Dish"
    KNUCKLE = "Knuckle"
    MATERIAL = "Material"
    MISCELLANEOUS = "Miscellaneous"
    MONEY = "Money"
    STAFF = "Staff"
    SPEAR = "Spear"
    SUNDRY = "Sundry"
    SWORD = "Sword"
    UNTRADEABLE = "Untradeable"


WEAPON_TYPES = {
    ItemTypeEnum.AXE,
    ItemTypeEnum.BOW,
    ItemTypeEnum.KNUCKLE,
    ItemTypeEnum.SPEAR,
    ItemTypeEnum.STAFF,
    ItemTypeEnum.SWORD,
}


class MonsterTypeEnum(enum.Enum):
    MONSTER = "Monster"
    BOSS = "Boss"
    NPC = "NPC"


class Item(Base):
    __tablename__ = "item"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    name: Mapped[str] = mapped_column(nullable=False)
    race: Mapped[RaceEnum] = mapped_column(
        Enum(RaceEnum, create_constraint=True), nullable=False
    )
    type: Mapped[ItemTypeEnum] = mapped_column(
        Enum(ItemTypeEnum, create_constraint=True), nullable=False
    )
    weight: Mapped[int] = mapped_column(nullable=False)

    monster_items: Mapped[list["MonsterItem"]] = relationship(back_populates="item")

    __mapper_args__: ClassVar[dict[str, Any]] = {
        "polymorphic_on": case(
            (type.in_(WEAPON_TYPES), "WEAPON"),
            (type == ItemTypeEnum.ARMOUR, "ARMOUR"),
            else_="ITEM",
        ),
        "polymorphic_identity": "ITEM",
    }


class Equipment:
    """Mixin for fields shared by equippable item categories (armour, weapons)."""

    durability: Mapped[int] = mapped_column(nullable=False)
    required_strength: Mapped[int] = mapped_column(nullable=True)
    required_intelligence: Mapped[int] = mapped_column(nullable=True)
    required_wisdom: Mapped[int] = mapped_column(nullable=True)
    required_dexterity: Mapped[int] = mapped_column(nullable=True)
    required_constitution: Mapped[int] = mapped_column(nullable=True)


class Armour(Item, Equipment):
    __tablename__ = "armour"

    id: Mapped[int] = mapped_column(ForeignKey("item.id"), primary_key=True)
    defense_min: Mapped[int] = mapped_column(nullable=True)
    defense_max: Mapped[int] = mapped_column(nullable=True)

    __mapper_args__: ClassVar[dict[str, Any]] = {
        "polymorphic_identity": "ARMOUR",
    }


class Weapon(Item, Equipment):
    __tablename__ = "weapon"

    id: Mapped[int] = mapped_column(ForeignKey("item.id"), primary_key=True)
    attack_min: Mapped[int] = mapped_column(nullable=False)
    attack_max: Mapped[int] = mapped_column(nullable=False)
    speed: Mapped[str] = mapped_column(nullable=True)
    required_skill: Mapped[int] = mapped_column(nullable=True)

    __mapper_args__: ClassVar[dict[str, Any]] = {"polymorphic_identity": "WEAPON"}


class Map(Base):
    __tablename__ = "map"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    race: Mapped[RaceEnum] = mapped_column(
        Enum(RaceEnum, create_constraint=True), nullable=True
    )

    monsters: Mapped[list["Monster"]] = relationship(
        secondary="monster_map", back_populates="maps"
    )

    monster_items: Mapped[list["MonsterItem"]] = relationship(back_populates="map")


class Monster(Base):
    __tablename__ = "monster"

    # Parsed fields.
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    hp: Mapped[int] = mapped_column(nullable=False)
    mp: Mapped[int] = mapped_column(nullable=False)
    strength: Mapped[int] = mapped_column(nullable=False)
    offensive_strength: Mapped[int] = mapped_column(nullable=False)
    defensive_strength: Mapped[int] = mapped_column(nullable=False)
    intelligence: Mapped[int] = mapped_column(nullable=False)
    offensive_intelligence: Mapped[int] = mapped_column(nullable=False)
    defensive_intelligence: Mapped[int] = mapped_column(nullable=False)
    wisdom: Mapped[int] = mapped_column(nullable=False)
    dexterity: Mapped[int] = mapped_column(nullable=False)
    offensive_dexterity: Mapped[int] = mapped_column(nullable=False)
    defensive_dexterity: Mapped[int] = mapped_column(nullable=False)
    moral: Mapped[MoralEnum] = mapped_column(
        Enum(MoralEnum, create_constraint=True), nullable=False
    )

    maps: Mapped[list["Map"]] = relationship(
        secondary="monster_map", back_populates="monsters"
    )

    monster_items: Mapped[list["MonsterItem"]] = relationship(
        back_populates="monster", cascade="all, delete-orphan"
    )

    # Derived fields.
    race: Mapped[RaceEnum] = mapped_column(
        Enum(RaceEnum, create_constraint=True), nullable=True
    )
    type: Mapped[MonsterTypeEnum] = mapped_column(
        Enum(MonsterTypeEnum, create_constraint=True), nullable=True
    )


class MonsterMap(Base):
    __tablename__ = "monster_map"

    monster_id: Mapped[int] = mapped_column(ForeignKey("monster.id"), primary_key=True)
    map_id: Mapped[int] = mapped_column(ForeignKey("map.id"), primary_key=True)


class MonsterItem(Base):
    __tablename__ = "monster_item"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    monster_id: Mapped[int] = mapped_column(ForeignKey("monster.id"), nullable=False)
    map_id: Mapped[int] = mapped_column(ForeignKey("map.id"), nullable=False)
    item_id: Mapped[int] = mapped_column(ForeignKey("item.id"), nullable=False)
    drop_rate: Mapped[float] = mapped_column(nullable=False)

    monster: Mapped["Monster"] = relationship(back_populates="monster_items")
    map: Mapped["Map"] = relationship(back_populates="monster_items")
    item: Mapped["Item"] = relationship(back_populates="monster_items")


class Spell(Base):
    __tablename__ = "spell"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    race: Mapped[RaceEnum] = mapped_column(
        Enum(RaceEnum, create_constraint=True), nullable=False
    )
    school: Mapped[SchoolEnum] = mapped_column(
        Enum(SchoolEnum, create_constraint=True), nullable=False
    )

    __table_args__ = (
        UniqueConstraint("name", "race", name="unique_spell_name_per_race"),
    )

    levels: Mapped[list["SpellLevel"]] = relationship(
        back_populates="spell", cascade="all, delete-orphan"
    )


class SpellLevel(Base):
    __tablename__ = "spell_level"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    spell_id: Mapped[int] = mapped_column(ForeignKey("spell.id"), nullable=False)
    level: Mapped[int] = mapped_column(nullable=False)
    range: Mapped[int] = mapped_column(nullable=False)
    duration: Mapped[int | None] = mapped_column(nullable=True)
    power: Mapped[int] = mapped_column(nullable=False)
    mp: Mapped[int] = mapped_column(nullable=False)

    __table_args__ = (UniqueConstraint("spell_id", "level", name="unique_spell_level"),)

    spell: Mapped["Spell"] = relationship(back_populates="levels")
    requirements: Mapped[list["SpellRequirement"]] = relationship(
        back_populates="spell_level", cascade="all, delete-orphan"
    )


class SpellRequirement(Base):
    """A single node in a spell level's all/any requirement tree.

    Top-level rows (parent_id is None) are implicitly AND-ed together. A row
    with kind=ANY (or ALL) is a container whose children are its operands.
    """

    __tablename__ = "spell_requirement"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    spell_level_id: Mapped[int] = mapped_column(
        ForeignKey("spell_level.id"), nullable=False
    )
    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey("spell_requirement.id"), nullable=True
    )
    kind: Mapped[RequirementKindEnum] = mapped_column(
        Enum(RequirementKindEnum, create_constraint=True), nullable=False
    )
    value: Mapped[int | None] = mapped_column(nullable=True)
    item_id: Mapped[int | None] = mapped_column(ForeignKey("item.id"), nullable=True)

    spell_level: Mapped["SpellLevel"] = relationship(back_populates="requirements")
    parent: Mapped["SpellRequirement | None"] = relationship(
        remote_side=[id], back_populates="children"
    )
    children: Mapped[list["SpellRequirement"]] = relationship(
        back_populates="parent", cascade="all, delete-orphan"
    )

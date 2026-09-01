import enum
from typing import Any, ClassVar

from sqlalchemy import Enum, ForeignKey, String, case
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

    __mapper_args__: ClassVar[dict[str, Any]] = {"polymorphic_identity": "WEAPON"}


class Map(Base):
    __tablename__ = "map"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)

    monsters: Mapped[list["Monster"]] = relationship(
        secondary="monster_map", back_populates="maps"
    )


class Monster(Base):
    __tablename__ = "monster"

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


class MonsterMap(Base):
    __tablename__ = "monster_map"

    monster_id: Mapped[int] = mapped_column(ForeignKey("monster.id"), primary_key=True)
    map_id: Mapped[int] = mapped_column(ForeignKey("map.id"), primary_key=True)

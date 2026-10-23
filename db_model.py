import enum
from typing import Any, ClassVar

from sqlalchemy import Enum, ForeignKey, String, case
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class CraftSkillTypeEnum(enum.Enum):
    ACCESSORY = "Accessory"
    ARMOUR = "Armor"
    COOKING = "Cooking"
    PREPARE = "Prepare"
    POTION = "Potion"
    SMELT = "Smelt"
    SYNTHESIS = "Synthesis"
    WEAPON = "Weapon"


class CraftItemTypeEnum(enum.Enum):
    """Craft item types, grouped by the skill that creates them."""

    MATERIAL = "Material"

    # Accessory
    BRACELET = "Bracelet"
    RING = "Ring"
    NECKLACE = "Necklace"
    EARRING = "Earring"

    # Armour
    ARMOUR_TOP = "Armor Top"
    ARMOUR_BOTTOM = "Armor Bottom"
    ARMOUR_BOOTS = "Armor Boots"
    HELMET = "Helmet"
    SHIELD = "Shield"
    ROBE = "Robe"
    GARMENT_TOP = "Garment Top"
    GARMENT_BOTTOM = "Garment Bottom"
    SHOES = "Shoes"

    # Weapon
    SWORD = "1 Handed Sword"
    AXE = "Axe"
    BOW = "Bow"
    STAFF = "Staff"
    SPEAR = "Spear"
    KNUCKLE = "Knuckle"

    # Cooking
    FOOD = "Food"

    # Potion
    POTION = "Potion"


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
    UPGRADE = "Upgrade"


WEAPON_TYPES = {
    ItemTypeEnum.AXE,
    ItemTypeEnum.BOW,
    ItemTypeEnum.KNUCKLE,
    ItemTypeEnum.SPEAR,
    ItemTypeEnum.STAFF,
    ItemTypeEnum.SWORD,
}


class MonsterTypeEnum(enum.Enum):
    BOSS = "Boss"
    EVENT = "Event"
    MONSTER = "Monster"
    NPC = "NPC"


class ItemSourceEnum(enum.Enum):
    CRAFTED = "Crafted"
    DROP = "Drop"


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

    craft_skill_type: Mapped[CraftSkillTypeEnum | None] = mapped_column(
        Enum(CraftSkillTypeEnum, create_constraint=True), nullable=True
    )
    craft_skill: Mapped[int] = mapped_column(nullable=True)
    craft_item_type: Mapped[CraftItemTypeEnum | None] = mapped_column(
        Enum(CraftItemTypeEnum, create_constraint=True),
        nullable=True,
    )

    recipes: Mapped[list["ItemRecipe"]] = relationship(
        back_populates="item", cascade="all, delete-orphan"
    )

    __mapper_args__: ClassVar[dict[str, Any]] = {
        "polymorphic_on": case(
            (type.in_(WEAPON_TYPES), "WEAPON"),
            (type == ItemTypeEnum.ARMOUR, "ARMOUR"),
            (type == ItemTypeEnum.UPGRADE, "UPGRADE"),
            else_="ITEM",
        ),
        "polymorphic_identity": "ITEM",
    }


class ItemRecipe(Base):
    __tablename__ = "item_recipe"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    item_id: Mapped[int] = mapped_column(ForeignKey(Item.id), nullable=False)
    bone: Mapped[int] = mapped_column(nullable=True)
    cloth: Mapped[int] = mapped_column(nullable=True)
    leather: Mapped[int] = mapped_column(nullable=True)
    meat: Mapped[int] = mapped_column(nullable=True)
    metal: Mapped[int] = mapped_column(nullable=True)
    spice: Mapped[int] = mapped_column(nullable=True)
    wood: Mapped[int] = mapped_column(nullable=True)

    specific_id_1: Mapped[int] = mapped_column(nullable=True)
    specific_quantity_1: Mapped[int] = mapped_column(nullable=True)
    specific_id_2: Mapped[int] = mapped_column(nullable=True)
    specific_quantity_2: Mapped[int] = mapped_column(nullable=True)
    specific_id_3: Mapped[int] = mapped_column(nullable=True)
    specific_quantity_3: Mapped[int] = mapped_column(nullable=True)
    specific_id_4: Mapped[int] = mapped_column(nullable=True)
    specific_quantity_4: Mapped[int] = mapped_column(nullable=True)
    specific_id_5: Mapped[int] = mapped_column(nullable=True)
    specific_quantity_5: Mapped[int] = mapped_column(nullable=True)

    item: Mapped["Item"] = relationship(back_populates="recipes")


class ItemSource(Base):
    __tablename__ = "item_source"

    item_id: Mapped[int] = mapped_column(ForeignKey(Item.id), primary_key=True)
    source: Mapped[ItemSourceEnum] = mapped_column(
        Enum(ItemSourceEnum, create_constraint=True), primary_key=True
    )


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

    id: Mapped[int] = mapped_column(ForeignKey(Item.id), primary_key=True)
    defense_min: Mapped[int] = mapped_column(nullable=True)
    defense_max: Mapped[int] = mapped_column(nullable=True)

    __mapper_args__: ClassVar[dict[str, Any]] = {"polymorphic_identity": "ARMOUR"}


class Weapon(Item, Equipment):
    __tablename__ = "weapon"

    id: Mapped[int] = mapped_column(ForeignKey(Item.id), primary_key=True)
    attack_min: Mapped[int] = mapped_column(nullable=False)
    attack_max: Mapped[int] = mapped_column(nullable=False)
    speed: Mapped[str] = mapped_column(nullable=True)
    required_skill: Mapped[int] = mapped_column(nullable=True)

    __mapper_args__: ClassVar[dict[str, Any]] = {"polymorphic_identity": "WEAPON"}


class Upgrade(Item):
    __tablename__ = "upgrade"

    id: Mapped[int] = mapped_column(ForeignKey("item.id"), primary_key=True)
    max_upgrades: Mapped[int] = mapped_column(nullable=False)
    requires_skill: Mapped[bool] = mapped_column(nullable=False)

    __mapper_args__: ClassVar[dict[str, Any]] = {"polymorphic_identity": "UPGRADE"}


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

    model_id: Mapped[int] = mapped_column(nullable=False)

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

    monster_id: Mapped[int] = mapped_column(ForeignKey(Monster.id), primary_key=True)
    map_id: Mapped[int] = mapped_column(ForeignKey(Map.id), primary_key=True)


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

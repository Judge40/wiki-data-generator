import enum

from sqlalchemy import Enum, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class MoralEnum(enum.Enum):
    NONE = "None"
    VERY_POOR = "Very Poor"
    POOR = "Poor"
    GOOD = "Good"
    VERY_GOOD = "Very Good"
    EXCELLENT = "Excellent"


class Monster(Base):
    __tablename__ = "monster"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    hp: Mapped[int] = mapped_column(nullable=False)
    mp: Mapped[int] = mapped_column(nullable=False)
    strength: Mapped[int] = mapped_column(nullable=False)
    intelligence: Mapped[int] = mapped_column(nullable=False)
    offensive_dexterity: Mapped[int] = mapped_column(nullable=False)
    defensive_dexterity: Mapped[int] = mapped_column(nullable=False)
    moral: Mapped[MoralEnum] = mapped_column(
        Enum(MoralEnum, create_constraint=True), nullable=False
    )

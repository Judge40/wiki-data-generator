import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

import config
from db_model import Base, Monster, MoralEnum

log = logging.getLogger("repository")

engine = create_engine(config.DB_PATH)
Base.metadata.create_all(engine)


def save_monster(monster_data: dict) -> None:
    """Upsert parsed monster stats, converting the moral string to MoralEnum."""
    monster_data = {**monster_data, "moral": MoralEnum(monster_data["moral"])}
    with Session(engine) as session:
        session.merge(Monster(**monster_data))
        session.commit()
    log.debug("Saved monster %s", monster_data["id"])

from datetime import datetime
from pony.orm import Database, Required, Optional, PrimaryKey, Set
from kara.entities.config import get_config

config = get_config("data/config.json")

db = Database()
db.bind(provider="sqlite", filename=config.db_location, create_db=True)


class Snowflake(db.Entity):
    id = PrimaryKey(str, 18)


class Punishment(db.Entity):
    id = PrimaryKey(int, auto=True)
    given_by = Required(str, 18)
    reason = Optional(str)
    user = Required('User')


class User(Snowflake):
    punishments = Set(Punishment)


class Mute(Punishment):
    start = Required(datetime)
    end = Required(datetime)
    active = Required(bool)


class Warn(Punishment):
    when = Required(datetime)


class Guild(Snowflake):
    mod_role = Optional(str, 18)
    mute_role = Optional(str, 18)


db.generate_mapping(create_tables=True)

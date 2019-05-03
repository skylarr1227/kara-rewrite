import codecs
from discord import Activity, ActivityType
from json import load


def get_status(filename: str) -> Activity:
    with codecs.open(filename, "r") as f:
        config = load(f)
        assert config.get("type") in range(4)

        return Activity(state=config["state"],
                        name=config["name"],
                        details=config["details"],
                        url=config["url"],
                        type=config["type"])

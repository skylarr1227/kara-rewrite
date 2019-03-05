from discord import Activity, ActivityType
from json import load
# from typing import Optional


# class Status:
#     state: str
#     name: str
#     details: str
#     url: Optional[str]
#     activity: Activity
#
#     def __init__(self, state, name, details, url, activity):
#         self.state = state
#         self.name = name
#         self.details = details
#         self.url = url
#         self.activity = activity


def from_filename(filename: str) -> Activity:
    with open(filename, "r") as f:
        config = load(f)
        assert config.get("type") in range(4)

        return Activity(state=config["state"],
                        name=config["name"],
                        details=config["details"],
                        url=config["url"],
                        type=config["type"])

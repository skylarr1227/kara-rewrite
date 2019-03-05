from json import load
from typing import List


class Config:
    name: str
    lang: str
    prefix: str
    token: str
    start_cogs: List[str]

    def __init__(self, name, lang, prefix, token, start_cogs):
        self.name = name
        self.lang = lang
        self. prefix = prefix
        self.token = token
        self.start_cogs = start_cogs


def from_filename(filename: str, bot_name: str) -> Config:
    with open(filename, "r") as f:
        file = load(f)
        assert file.get(bot_name)
        config = file.get(bot_name)

        return Config(name=config["name"],
                      lang=config["lang"],
                      prefix=config["prefix"],
                      token=config["token"],
                      start_cogs=config["start_cogs"])

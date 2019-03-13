from sys import argv
from kara.entities.config import get_config, Config
from kara import CustomClient

if __name__ == "__main__":
    if len(argv) == 1:
        config = get_config("data/config.json")
    else:
        config = get_config("data/config.json", argv[1])
    client = CustomClient(config)
    client.startup(client)

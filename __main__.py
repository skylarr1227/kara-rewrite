from sys import argv
from kara.entities.config import from_filename
from kara import CustomClient


if __name__ == "__main__":
    config = from_filename("data/config.json", argv[1])
    client = CustomClient(config)
    client.startup(client)

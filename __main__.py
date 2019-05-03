import i18n as loc
from sys import argv
from kara.entities.config import get_config
from kara import CustomClient

loc.set("file_format", "json")
loc.set("available_locales", ["en", "pl"])
loc.set("fallback", "en")
loc.set("filename_format", "{locale}.{format}")
loc.set('skip_locale_root_data', True)
loc.load_path.append("data/locale")

if __name__ == "__main__":
    if len(argv) == 1:
        config = get_config("data/config.json")
    else:
        config = get_config("data/config.json", argv[1])
    client = CustomClient(config)
    loc.set("locale", client.config.lang)
    client.startup(client)

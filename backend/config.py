import json


CONFIG_FILE = "config.json"


def load_config():
    """config.json을 읽는다."""

    with open(CONFIG_FILE, "r", encoding="utf-8") as file:
        config = json.load(file)

    return config


def save_config(config):
    """config.json에 설정을 저장한다."""

    with open(CONFIG_FILE, "w", encoding="utf-8") as file:
        json.dump(config, file, ensure_ascii=False, indent=4)
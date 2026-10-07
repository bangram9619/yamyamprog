import json
import os


CONFIG_FILE = "config.json"

# config.json이 없거나 값이 빠졌을 때 쓰는 기본값
DEFAULT_CONFIG = {
    "lastMode": "운동",
    "weight": 75,
    "dataDir": "./data",
    "kcalPerGram": {
        "carbs": 4,
        "protein": 4,
        "fat": 9
    },
    "modes": {
        "운동": {
            "carbs": 5.0,
            "protein": 1.6,
            "fat": 0.9
        },
        "다이어트": {
            "carbs": 3.0,
            "protein": 1.8,
            "fat": 0.7
        }
    }
}


def load_config():
    """config.json을 읽는다. 없거나 깨졌으면 기본값으로 새로 만든다."""

    # 1) 파일이 없으면 기본값으로 만든다.
    if not os.path.exists(CONFIG_FILE):
        print("[안내] config.json이 없어 기본 설정으로 새로 만듭니다.")
        save_config(DEFAULT_CONFIG)
        return dict(DEFAULT_CONFIG)

    # 2) 파일 내용이 깨졌으면 기본값으로 다시 만든다.
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as file:
            config = json.load(file)
    except json.JSONDecodeError:
        print("[안내] config.json 형식이 잘못되어 기본 설정으로 다시 만듭니다.")
        save_config(DEFAULT_CONFIG)
        return dict(DEFAULT_CONFIG)

    # 3) 빠진 항목이 있으면 기본값으로 채우고 저장한다.
    missing = False

    for key, value in DEFAULT_CONFIG.items():
        if key not in config:
            config[key] = value
            missing = True

    if missing:
        print("[안내] config.json에 빠진 항목을 기본값으로 채웠습니다.")
        save_config(config)

    return config


def save_config(config):
    """config.json에 설정을 저장한다."""

    with open(CONFIG_FILE, "w", encoding="utf-8") as file:
        json.dump(config, file, ensure_ascii=False, indent=4)
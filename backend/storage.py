import json
import os
from datetime import date, timedelta, datetime

from backend.config import load_config


# 식단 파일을 저장할 폴더 (config.json의 dataDir)
data_dir = load_config()["dataDir"]


def get_today_file():
    """오늘 날짜에 해당하는 JSON 파일을 찾는다."""

    os.makedirs(data_dir, exist_ok=True)

    today_text = date.today().strftime("%Y%m%d")

    files = os.listdir(data_dir)

    today_files = []

    for filename in files:
        if filename.startswith(today_text + "_") and filename.endswith(".json"):
            today_files.append(filename)

    if today_files:
        today_files.sort()
        return os.path.join(data_dir, today_files[0])

    # 오늘 파일이 없으면 새로 만든다.
    time_text = datetime.now().strftime("%H%M%S")
    filename = f"{today_text}_{time_text}.json"

    return os.path.join(data_dir, filename)


def find_date_file(selected_date):
    """입력한 날짜의 JSON 파일을 찾는다."""

    os.makedirs(data_dir, exist_ok=True)

    files = os.listdir(data_dir)

    date_files = []

    for filename in files:
        if filename.startswith(selected_date + "_") and filename.endswith(".json"):
            date_files.append(filename)

    if not date_files:
        return None

    date_files.sort()

    return os.path.join(data_dir, date_files[0])


def load_meal_data(file_path):
    """식단 JSON 파일을 읽는다."""

    if not os.path.exists(file_path):
        return {}

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def save_meal_data(file_path, data):
    """식단 데이터를 JSON 파일에 저장한다."""

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def get_next_meal_id(data):
    """다음 식단 번호를 결정한다."""

    if not data:
        return "1"

    ids = []

    for key in data.keys():
        ids.append(int(key))

    next_id = max(ids) + 1

    return str(next_id)


def get_daily_total(selected_date):
    """특정 날짜의 영양소 총합을 계산한다."""

    file_path = find_date_file(selected_date)

    if file_path is None:
        return None

    data = load_meal_data(file_path)

    total = {
        "carbs": 0,
        "protein": 0,
        "fat": 0,
        "calories": 0
    }

    for meal_data in data.values():
        total["carbs"] += meal_data["carbs"]
        total["protein"] += meal_data["protein"]
        total["fat"] += meal_data["fat"]
        total["calories"] += meal_data["calories"]

    return total


def get_weekly_total():
    """최근 7일간의 영양소 총합을 계산한다."""

    today = date.today()

    total = {
        "carbs": 0,
        "protein": 0,
        "fat": 0,
        "calories": 0
    }

    for i in range(7):
        target_date = today - timedelta(days=i)
        selected_date = target_date.strftime("%Y%m%d")

        daily_total = get_daily_total(selected_date)

        if daily_total is None:
            continue

        total["carbs"] += daily_total["carbs"]
        total["protein"] += daily_total["protein"]
        total["fat"] += daily_total["fat"]
        total["calories"] += daily_total["calories"]

    return total
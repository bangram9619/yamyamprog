import json
import os
from datetime import date, timedelta, datetime


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


# 프로그램 설정 불러오기
config = load_config()

current_mode = config["lastMode"]
weight = config["weight"]
data_dir = config["dataDir"]

currentMenu = 0
selectedDate = ""
selectedId = ""
editTargetNum = 0
analysisPeriod = 0

def show_main_menu():
    """메인 화면을 보여준다."""

    today = date.today()

    print()
    print("┌── [ 영양 관리 프로그램 - " + current_mode + " 모드 ] ─────────────────────┐")
    print(
        f"│  오늘 날짜: {today.year}년 {today.month:02d}월 {today.day:02d}일                             │"
    )
    print("└──────────────────────────────────────────────────────────┘")
    print()
    print("  1. 모드 설정")
    print("  2. 영양소 기록 저장")
    print("  3. 영양 기록 (조회 / 수정 / 삭제)")
    print("  4. 영양 비교 분석")
    print("  0. 프로그램 종료")
    print()


def mode_setting():
    """운동 / 다이어트 모드를 선택한다."""

    global current_mode
    global config

    print()
    print("┌ 모드 설정 ────────────────┐")
    print("│  1. 운동                  │")
    print("│  2. 다이어트              │")
    print("└───────────────────────────┘")

    choice = input("선택: ")

    if choice == "1":
        current_mode = "운동"

    elif choice == "2":
        current_mode = "다이어트"

    else:
        print()
        print("[오류] 잘못된 선택입니다.")
        return

    config["lastMode"] = current_mode
    save_config(config)

    print()
    print("[안내] 모드 설정이 완료되었습니다. 메인 화면 상단에 즉시 반영됩니다.")
    input("엔터를 누르면 메인 메뉴로 돌아갑니다...")


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


def meal_save():
    """영양소 기록을 저장한다."""

    print()
    print("[ 영양소 기록 저장 ]")
    print()

    meal = input("▶ 식단명 입력        : ")

    while True:
        try:
            carbs = int(input("▶ 탄수화물 입력 (g)  : "))
            break
        except ValueError:
            print("[오류] 숫자로 입력해주세요.")

    while True:
        try:
            protein = int(input("▶ 단백질 입력 (g)    : "))
            break
        except ValueError:
            print("[오류] 숫자로 입력해주세요.")

    while True:
        try:
            fat = int(input("▶ 지방 입력 (g)      : "))
            break
        except ValueError:
            print("[오류] 숫자로 입력해주세요.")

    while True:
        try:
            calories = int(input("▶ 칼로리 입력 (kcal) : "))
            break
        except ValueError:
            print("[오류] 숫자로 입력해주세요.")

    file_path = get_today_file()

    data = load_meal_data(file_path)

    meal_id = get_next_meal_id(data)

    data[meal_id] = {
        "meal": meal,
        "carbs": carbs,
        "protein": protein,
        "fat": fat,
        "calories": calories
    }

    save_meal_data(file_path, data)

    print()
    print(f"[완료] 특정 식단 번호({meal_id}번)로 오늘 파일에 정상 저장되었습니다.")
    input("아무 키나 누르면 메인 메뉴로 돌아갑니다...")

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


def show_meal_records():
    """날짜별 영양 기록을 조회한다."""

    global selectedDate

    print()
    print("[ 날짜별 영양 기록 조회 및 관리 ]")
    print()

    selectedDate = input(
        "조회할 날짜 입력 (YYYYMMDD 형식, 미입력 시 엔터치면 오늘): "
    )

    if selectedDate == "":
        selectedDate = date.today().strftime("%Y%m%d")

    # 날짜 형식 확인
    if len(selectedDate) != 8 or not selectedDate.isdigit():
        print()
        print("[오류] 날짜는 YYYYMMDD 형식으로 입력해주세요.")
        input("엔터를 누르면 이전 메뉴로 돌아갑니다...")
        return

    file_path = find_date_file(selectedDate)

    if file_path is None:
        print()
        print("[안내] 기록된 식단이 없습니다. 새로 등록해 주세요.")
        input("엔터를 누르면 이전 메뉴로 돌아갑니다...")
        return

    data = load_meal_data(file_path)

    print()
    print(f"파일 로드 성공: {os.path.basename(file_path)}")
    print()
    print("-" * 80)
    print("[식단 번호] 식단 요약       탄수화물       단백질     지방     칼로리")
    print("-" * 80)

    total_carbs = 0
    total_protein = 0
    total_fat = 0
    total_calories = 0

    for meal_id, meal_data in data.items():

        print(
            f"{meal_id:>3}    "
            f"{meal_data['meal']:<18} "
            f"{meal_data['carbs']:>5}g      "
            f"{meal_data['protein']:>5}g     "
            f"{meal_data['fat']:>4}g    "
            f"{meal_data['calories']:>5}kcal"
        )

        total_carbs += meal_data["carbs"]
        total_protein += meal_data["protein"]
        total_fat += meal_data["fat"]
        total_calories += meal_data["calories"]

    print("-" * 80)
    print(
    f"{'[당일 누적 총합 영양소]':<20}"
    f"{total_carbs:>5}g      "
    f"{total_protein:>5}g     "
    f"{total_fat:>4}g    "
    f"{total_calories:>5}kcal"
    )
    print("-" * 80)

    while True:

        print()
        print("  1. 영양 기록 수정")
        print("  2. 영양 기록 삭제")
        print("  0. 이전 메뉴로 이동")

        work = input("\n작업 선택: ")

        if work == "1":
            edit_meal(data, file_path)

        elif work == "2":
            delete_meal(data, file_path)

        elif work == "0":
            return

        else:
            print()
            print("[오류] 0~2 중에서 선택해주세요.")


def edit_meal(data, file_path):
    """특정 식단의 영양소를 수정한다."""

    global selectedId
    global editTargetNum

    selectedId = input("수정할 식단 번호 입력: ")

    if selectedId not in data:
        print()
        print("존재하지 않는 식단 번호입니다.")
        return

    print()
    print(f"[{selectedId}번 식단 수정 모드] 바꾸실 영양소를 선택하세요.")
    print(" 1. 탄수화물  2. 단백질  3. 지방  4. 칼로리")

    while True:
        try:
            editTargetNum = int(input("선택: "))
            break
        except ValueError:
            print("[오류] 숫자로 입력해주세요.")

    if editTargetNum == 1:

        while True:
            try:
                value = int(input("▶ 변경할 탄수화물 입력 (g): "))
                break
            except ValueError:
                print("[오류] 숫자로 입력해주세요.")

        data[selectedId]["carbs"] = value

        print()
        print(
            f"[완료] {selectedId}번 식단의 탄수화물이 "
            f"{value}g으로 성공적으로 수정 및 업데이트되었습니다."
        )

    elif editTargetNum == 2:

        while True:
            try:
                value = int(input("▶ 변경할 단백질 입력 (g): "))
                break
            except ValueError:
                print("[오류] 숫자로 입력해주세요.")

        data[selectedId]["protein"] = value

        print()
        print(
            f"[완료] {selectedId}번 식단의 단백질이 "
            f"{value}g으로 성공적으로 수정 및 업데이트되었습니다."
        )

    elif editTargetNum == 3:

        while True:
            try:
                value = int(input("▶ 변경할 지방 입력 (g): "))
                break
            except ValueError:
                print("[오류] 숫자로 입력해주세요.")

        data[selectedId]["fat"] = value

        print()
        print(
            f"[완료] {selectedId}번 식단의 지방이 "
            f"{value}g으로 성공적으로 수정 및 업데이트되었습니다."
        )

    elif editTargetNum == 4:

        while True:
            try:
                value = int(input("▶ 변경할 칼로리 입력 (kcal): "))
                break
            except ValueError:
                print("[오류] 숫자로 입력해주세요.")

        data[selectedId]["calories"] = value

        print()
        print(
            f"[완료] {selectedId}번 식단의 칼로리가 "
            f"{value}kcal으로 성공적으로 수정 및 업데이트되었습니다."
        )

    else:
        print()
        print("[오류] 1~4 중에서 선택해주세요.")
        return

    save_meal_data(file_path, data)


def delete_meal(data, file_path):
    """특정 식단을 삭제한다."""

    global selectedId

    selectedId = input("삭제할 식단 번호 입력: ")

    if selectedId not in data:
        print()
        print("존재하지 않는 식단 번호입니다.")
        return

    del data[selectedId]

    save_meal_data(file_path, data)

    print()
    print(
        f"[완료] {selectedId}번 식단이 정상적으로 삭제되었습니다."
    )

def get_target_nutrients():
    """현재 모드의 추천 영양소 목표값을 반환한다."""

    global targetCarbs
    global targetProtein
    global targetFat
    global targetCalories

    if current_mode == "운동":
        targetCarbs = 338
        targetProtein = 135
        targetFat = 75
        targetCalories = 2565

        return {
            "carbs": targetCarbs,
            "protein": targetProtein,
            "fat": targetFat,
            "calories": targetCalories
        }

    elif current_mode == "다이어트":
        targetCarbs = 225
        targetProtein = 135
        targetFat = 53
        targetCalories = 1917

        return {
            "carbs": targetCarbs,
            "protein": targetProtein,
            "fat": targetFat,
            "calories": targetCalories
        }

    return None


def classify_nutrient(intake, target):
    """섭취량을 추천량과 비교한다."""

    percentage = (intake / target) * 100

    if percentage < 85:
        return percentage, "부족", "▲"

    elif percentage <= 110:
        return percentage, "적절", "="

    else:
        return percentage, "과다", "▼"

def pad_name(name, width=10):
    """한글 영양소 이름을 터미널 화면 폭에 맞춰 정렬한다."""
    return name + " " * (width - len(name) * 2)

def make_bar(percentage):
    """10칸 텍스트 막대그래프를 만든다."""

    filled = int(percentage / 10)

    if filled > 10:
        filled = 10

    if filled < 0:
        filled = 0

    empty = 10 - filled

    sky_blue = "\033[96m"
    reset = "\033[0m"

    return sky_blue + "■" * filled + reset + "□" * empty


def analyze_one_nutrient(name, intake, target, unit):
    """영양소 하나의 비교 결과를 출력한다."""

    percentage, status, symbol = classify_nutrient(
        intake,
        target
    )

    bar = make_bar(percentage)

    if status == "부족":
        status_color = "\033[91m"
    elif status == "적절":
        status_color = "\033[92m"
    else:
        status_color = "\033[93m"

    reset = "\033[0m"

    colored_status = status_color + status + reset
    colored_symbol = status_color + symbol + reset

    print(
        f"{pad_name(name)}"
        f"[{bar}] "
        f"{percentage:>3.0f}% "
        f"({intake:>4} / {target:>4} {unit}) "
        f"-> [{colored_status}] {name} {colored_symbol}"
    )

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


def daily_analysis():
    """하루 기준 영양 비교 분석."""

    global analysisPeriod

    analysisPeriod = 1

    targets = get_target_nutrients()

    if targets is None:
        print()
        print("[안내] 목적을 먼저 설정하세요.")
        input("엔터를 누르면 이전 메뉴로 돌아갑니다...")
        return

    selected_date = input(
        "분석할 날짜 입력 (YYYYMMDD 형식, 미입력 시 엔터치면 오늘): "
    )

    if selected_date == "":
        selected_date = date.today().strftime("%Y%m%d")

    if len(selected_date) != 8 or not selected_date.isdigit():
        print()
        print("[오류] 날짜는 YYYYMMDD 형식으로 입력해주세요.")
        input("엔터를 누르면 이전 메뉴로 돌아갑니다...")
        return

    total = get_daily_total(selected_date)

    if total is None:
        print()
        print("[안내] 기록된 식단이 없습니다. 새로 등록해 주세요.")
        input("엔터를 누르면 이전 메뉴로 돌아갑니다...")
        return

    print()
    print("[ 모드별 기준 vs 사용자 섭취 영양 비교 분석 (하루 기준) ]")
    print(
        f"(대상 기준: {current_mode} 모드 / "
        f"{selected_date} 당일 누적 데이터 합산 기준)"
    )
    print()

    analyze_one_nutrient(
        "탄수화물",
        total["carbs"],
        targets["carbs"],
        "g"
    )

    analyze_one_nutrient(
        "단백질",
        total["protein"],
        targets["protein"],
        "g"
    )

    analyze_one_nutrient(
        "지방",
        total["fat"],
        targets["fat"],
        "g"
    )

    percentage = (
        total["calories"] / targets["calories"]
    ) * 100

    bar = make_bar(percentage)

    print(
    f"{pad_name('칼로리')}"
    f"[{bar}] "
    f"{percentage:>3.0f}% "
    f"({total['calories']:>4} / "
    f"{targets['calories']:>4} kcal)"
    )

    print()
    input("엔터를 누르면 이전 메뉴로 돌아갑니다...")

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


def weekly_analysis():
    """일주일(7일) 누적 영양 비교 분석."""

    global analysisPeriod

    analysisPeriod = 2

    targets = get_target_nutrients()

    if targets is None:
        print()
        print("[안내] 목적을 먼저 설정하세요.")
        input("엔터를 누르면 이전 메뉴로 돌아갑니다...")
        return

    weekly_target = {
        "carbs": targets["carbs"] * 7,
        "protein": targets["protein"] * 7,
        "fat": targets["fat"] * 7,
        "calories": targets["calories"] * 7
    }

    total = get_weekly_total()

    print()
    print("[ 모드별 기준 vs 사용자 섭취 영양 비교 분석 (일주일 기준) ]")
    print(
        f"(대상 기준: {current_mode} 모드 / "
        f"최근 1주일(7일) 누적 데이터 합산 기준)"
    )
    print()

    analyze_one_nutrient(
        "탄수화물",
        total["carbs"],
        weekly_target["carbs"],
        "g"
    )

    analyze_one_nutrient(
        "단백질",
        total["protein"],
        weekly_target["protein"],
        "g"
    )

    analyze_one_nutrient(
        "지방",
        total["fat"],
        weekly_target["fat"],
        "g"
    )

    percentage = (
        total["calories"] / weekly_target["calories"]
    ) * 100

    bar = make_bar(percentage)

    print(
    f"{pad_name('칼로리')}"
    f"[{bar}] "
    f"{percentage:>3.0f}% "
    f"({total['calories']:>4} / "
    f"{weekly_target['calories']:>4} kcal)"
    )

    print()
    input("엔터를 누르면 이전 메뉴로 돌아갑니다...")

def main():
    """프로그램 시작점."""

    global currentMenu

    while True:

        currentMenu = 0
        show_main_menu()

        choice = input("선택 (숫자 입력 후 Enter): ")

        if choice == "1":

            currentMenu = 1
            mode_setting()

        elif choice == "2":

            currentMenu = 2
            meal_save()

        elif choice == "3":

            currentMenu = 3
            show_meal_records()

        elif choice == "4":

            currentMenu = 4

            print()
            print("[ 영양 비교 분석 ]")
            print()
            print(" 분석 단위를 선택해 주세요.")
            print(" 1. 하루 기준 분석")
            print(" 2. 일주일(7일) 누적 기준 분석")
            print(" 0. 메인 메뉴로 돌아가기")

            analysis_choice = input("\n선택: ")

            if analysis_choice == "1":

                daily_analysis()

            elif analysis_choice == "2":

                weekly_analysis()

            elif analysis_choice == "0":

                pass

            else:

                print()
                print("[오류] 0~2 중에서 선택해주세요.")

        elif choice == "0":

            print()
            print("프로그램을 종료합니다.")
            break

        else:

            print()
            print("[오류] 0~4 중에서 선택해주세요.")


if __name__ == "__main__":
    main()
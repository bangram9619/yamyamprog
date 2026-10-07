import os

from datetime import date

from backend.config import load_config, save_config
from backend.storage import (
    get_today_file,
    find_date_file,
    load_meal_data,
    save_meal_data,
    get_next_meal_id,
    get_daily_total,
    get_weekly_total,
)
from backend.nutrition import get_target_nutrients
from frontend.display import (                                         
    clear_screen,
    analyze_one_nutrient,
    ljust_kr,
    rjust_kr,
    cut_kr,
)

# 프로그램 설정 불러오기
config = load_config()

current_mode = config["lastMode"]
currentMenu = 0
selectedDate = ""
selectedId = ""
editTargetNum = 0
analysisPeriod = 0


def input_number(prompt):
    """0 이상의 정수를 입력받는다. 잘못 입력하면 다시 묻는다."""

    while True:
        text = input(prompt).strip()

        if text.isdigit():
            return int(text)

        print("[오류] 0 이상의 숫자로 입력해주세요.")


def show_main_menu():
    """메인 화면을 보여준다."""

    clear_screen()
    today = date.today()

    print()
    print("┌── [ 영양 관리 프로그램 - " + current_mode + " 모드 ] ────────────────────┐")
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

    clear_screen()
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
        input("엔터를 누르면 메인 메뉴로 돌아갑니다...")
        return

    config["lastMode"] = current_mode
    save_config(config)

    print()
    print("[안내] 모드 설정이 완료되었습니다. 메인 화면 상단에 즉시 반영됩니다.")
    input("엔터를 누르면 메인 메뉴로 돌아갑니다...")


def meal_save():
    """영양소 기록을 저장한다."""

    clear_screen()
    print()
    print("[ 영양소 기록 저장 ]")
    print()

    meal = input("▶ 식단명 입력        : ").strip()

    while meal == "":
        print("[오류] 식단명을 입력해주세요.")
        meal = input("▶ 식단명 입력        : ").strip()

    carbs = input_number("▶ 탄수화물 입력 (g)  : ")
    protein = input_number("▶ 단백질 입력 (g)    : ")
    fat = input_number("▶ 지방 입력 (g)      : ")
    calories = input_number("▶ 칼로리 입력 (kcal) : ")

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


def show_meal_records():
    """날짜별 영양 기록을 조회한다."""

    global selectedDate

    clear_screen()
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

    line = "-" * 70

    print(line)
    print(
        ljust_kr("[번호] 식단 요약", 30)
        + rjust_kr("탄수화물", 9)
        + rjust_kr("단백질", 9)
        + rjust_kr("지방", 9)
        + rjust_kr("칼로리", 12)
    )
    print(line)

    total_carbs = 0
    total_protein = 0
    total_fat = 0
    total_calories = 0

    for meal_id, meal_data in data.items():

        meal_name = cut_kr(meal_data["meal"], 22)

        print(
            rjust_kr(meal_id, 4)
            + "   "
            + ljust_kr(meal_name, 23)
            + rjust_kr(f"{meal_data['carbs']}g", 9)
            + rjust_kr(f"{meal_data['protein']}g", 9)
            + rjust_kr(f"{meal_data['fat']}g", 9)
            + rjust_kr(f"{meal_data['calories']}kcal", 12)
        )

        total_carbs += meal_data["carbs"]
        total_protein += meal_data["protein"]
        total_fat += meal_data["fat"]
        total_calories += meal_data["calories"]

    print(line)
    print(
        ljust_kr("[당일 누적 총합 영양소]", 30)
        + rjust_kr(f"{total_carbs}g", 9)
        + rjust_kr(f"{total_protein}g", 9)
        + rjust_kr(f"{total_fat}g", 9)
        + rjust_kr(f"{total_calories}kcal", 12)
    )
    print(line)

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

    editTargetNum = input_number("선택: ")

    if editTargetNum == 1:

        value = input_number("▶ 변경할 탄수화물 입력 (g): ")

        data[selectedId]["carbs"] = value

        print()
        print(
            f"[완료] {selectedId}번 식단의 탄수화물이 "
            f"{value}g으로 성공적으로 수정 및 업데이트되었습니다."
        )

    elif editTargetNum == 2:

        value = input_number("▶ 변경할 단백질 입력 (g): ")

        data[selectedId]["protein"] = value

        print()
        print(
            f"[완료] {selectedId}번 식단의 단백질이 "
            f"{value}g으로 성공적으로 수정 및 업데이트되었습니다."
        )

    elif editTargetNum == 3:

        value = input_number("▶ 변경할 지방 입력 (g): ")

        data[selectedId]["fat"] = value

        print()
        print(
            f"[완료] {selectedId}번 식단의 지방이 "
            f"{value}g으로 성공적으로 수정 및 업데이트되었습니다."
        )

    elif editTargetNum == 4:

        value = input_number("▶ 변경할 칼로리 입력 (kcal): ")

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


def daily_analysis():
    """하루 기준 영양 비교 분석."""

    global analysisPeriod

    analysisPeriod = 1

    targets = get_target_nutrients(config, current_mode)

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

    analyze_one_nutrient(
        "칼로리",
        total["calories"],
        targets["calories"],
        "kcal"
    )

    print()
    input("엔터를 누르면 이전 메뉴로 돌아갑니다...")


def weekly_analysis():
    """일주일(7일) 누적 영양 비교 분석."""

    global analysisPeriod

    analysisPeriod = 2

    targets = get_target_nutrients(config, current_mode)

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

    analyze_one_nutrient(
        "칼로리",
        total["calories"],
        weekly_target["calories"],
        "kcal"
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
            clear_screen()

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
                input("엔터를 누르면 메인 메뉴로 돌아갑니다...")

        elif choice == "0":

            print()
            print("프로그램을 종료합니다.")
            break

        else:

            print()
            print("[오류] 0~4 중에서 선택해주세요.")
            input("엔터를 누르면 메인 메뉴로 돌아갑니다...")
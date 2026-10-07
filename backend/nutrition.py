# 추천 영양소 계산 결과 (명세서 ④ 키)
targetCarbs = 0
targetProtein = 0
targetFat = 0
targetCalories = 0


def round_half_up(value):
    """소수 첫째 자리에서 반올림한다. (예: 67.5 -> 68, 52.5 -> 53)

    파이썬 기본 round()는 52.5를 52로 내리기 때문에 따로 만든다.
    """

    return int(value + 0.5)


def get_target_nutrients(config, current_mode):
    """config.json의 체중과 모드별 기준값으로 추천 영양소를 계산한다.

    탄수화물 / 단백질 / 지방 = 체중 x 체중 1kg당 g  (정수로 반올림)
    칼로리 = 탄수화물 x 4 + 단백질 x 4 + 지방 x 9  (반올림 전 g으로 계산, 10kcal 단위 반올림)
    """

    global targetCarbs
    global targetProtein
    global targetFat
    global targetCalories

    modes = config["modes"]

    if current_mode not in modes:
        return None

    weight = config["weight"]
    ratio = modes[current_mode]
    kcal = config["kcalPerGram"]

    carbs = weight * ratio["carbs"]
    protein = weight * ratio["protein"]
    fat = weight * ratio["fat"]

    calories = (
        carbs * kcal["carbs"]
        + protein * kcal["protein"]
        + fat * kcal["fat"]
    )

    targetCarbs = round_half_up(carbs)
    targetProtein = round_half_up(protein)
    targetFat = round_half_up(fat)
    targetCalories = round_half_up(calories / 10) * 10

    return {
        "carbs": targetCarbs,
        "protein": targetProtein,
        "fat": targetFat,
        "calories": targetCalories
    }


def classify_nutrient(intake, target):
    """섭취량을 추천량과 비교한다."""

    percentage = (intake / target) * 100

    if percentage < 85:
        return percentage, "부족", "▲"

    elif percentage <= 110:
        return percentage, "적절", "="

    else:
        return percentage, "과다", "▼"
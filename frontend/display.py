import os

from backend.nutrition import classify_nutrient


def clear_screen():
    """터미널 화면을 지운다. (Windows: cls, Mac/Linux: clear)"""

    os.system("cls" if os.name == "nt" else "clear")


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
        f"({intake:>5} / {target:>5} {unit}) "
        f"-> [{colored_status}] {name} {colored_symbol}"
    )
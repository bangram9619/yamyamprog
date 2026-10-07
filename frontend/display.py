import os
import unicodedata   

from backend.nutrition import classify_nutrient


def clear_screen():
    """터미널 화면을 지운다. (Windows: cls, Mac/Linux: clear)"""

    os.system("cls" if os.name == "nt" else "clear")

def display_width(text):
    """터미널에 보이는 글자 폭을 센다. (한글은 2칸, 영어·숫자는 1칸)"""

    width = 0

    for ch in str(text):
        if unicodedata.east_asian_width(ch) in ("W", "F"):
            width += 2
        else:
            width += 1

    return width


def ljust_kr(text, width):
    """한글 폭을 고려해 왼쪽 정렬한다. (남는 칸은 오른쪽을 공백으로 채움)"""

    text = str(text)
    return text + " " * max(0, width - display_width(text))


def rjust_kr(text, width):
    """한글 폭을 고려해 오른쪽 정렬한다. (남는 칸은 왼쪽을 공백으로 채움)"""

    text = str(text)
    return " " * max(0, width - display_width(text)) + text


def cut_kr(text, width):
    """화면 폭을 넘는 긴 글자는 잘라서 '..'을 붙인다."""

    text = str(text)

    if display_width(text) <= width:
        return text

    result = ""

    for ch in text:
        if display_width(result + ch) > width - 2:
            break
        result += ch

    return result + ".."

def pad_name(name, width=10):
    """한글 영양소 이름을 터미널 화면 폭에 맞춰 정렬한다."""
    return ljust_kr(name, width) 


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
# ==============================
# FUNCTION IMPORTS
# ==============================

import os
import subprocess

# ==============================
# CONSTANTS
# ==============================

from utils.constants import (
    INVALID_INPUT,
    CHOOSE_OPTION,
)


def blank_lines(number):
    print("\n" * number, end="")


def format_currency(amount: int | float) -> str:
    if round(amount % 1, 2) == 0:
        return f"€{int(amount)},-"

    return f"€{amount:.2f}".replace(".", ",")


def clear_terminal():
    command = "cls" if os.name == "nt" else "clear"
    subprocess.run(command, shell=True, check=False)


def get_confirmation(action):
    confirmation = True

    while True:
        confirmation_choice = input(f"Weet u zeker dat u wilt {action}? (Ja/Nee) ").lower()

        if confirmation_choice not in ("ja", "nee"):
            print()
            print(INVALID_INPUT)
            print()
            continue

        if confirmation_choice == "nee":
            confirmation = False

        blank_lines(2)
        return confirmation

def get_menu_choice(valid_choices):
    while True:
        try:
            menu_choice = int(input(CHOOSE_OPTION))
        except ValueError:
            print(INVALID_INPUT)
            continue

        if menu_choice not in valid_choices:
            print(INVALID_INPUT)
            continue

        return menu_choice
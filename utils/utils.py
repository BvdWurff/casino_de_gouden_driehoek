# ==============================
# FUNCTION IMPORTS
# ==============================

import os
import subprocess


# ==============================
# CONSTANTS
# ==============================

from utils.constants import (
    CHOOSE_OPTION,
    INVALID_INPUT,
)


# ==============================
# GENERAL UTILITIES
# ==============================

def blank_lines(number):
    """
    Prints the specified number of blank lines.

    Args:
        number (int): The number of blank lines to print.
    """
    print("\n" * number, end="")


def clear_terminal():
    """
    Clears the terminal based on the operating system.
    """
    command = "cls" if os.name == "nt" else "clear"
    subprocess.run(command, shell=True, check=False)


def format_currency(amount):
    """
    Formats a numeric amount as a euro currency string.

    Args:
        amount (int or float): The amount to format.

    Returns:
        str: The formatted euro amount.
    """
    if round(amount % 1, 2) == 0:
        return f"€{int(amount)},-"

    return f"€{amount:.2f}".replace(".", ",")


# ==============================
# USER INPUT AND VALIDATION
# ==============================

def get_confirmation(action):
    """
    Requests confirmation for an action.

    Args:
        action (str): The action the user is asked to confirm.

    Returns:
        bool: True when the action is confirmed, otherwise False.
    """
    while True:
        confirmation_choice = input(
            f"Weet u zeker dat u wilt {action}? (Ja/Nee) "
        ).lower()

        if confirmation_choice not in ("ja", "nee"):
            print()
            print(INVALID_INPUT)
            print()
            continue

        blank_lines(2)

        return confirmation_choice == "ja"


def get_menu_choice(valid_choices):
    """
    Requests and validates a numeric menu choice.

    Args:
        valid_choices: The collection of allowed menu choices.

    Returns:
        int: The validated menu choice.
    """
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
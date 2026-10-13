# ==============================
# FUNCTION IMPORTS
# ==============================

import os
import subprocess
import time

from rich.console import Console
from rich.padding import Padding
from rich.panel import Panel
from rich.live import Live
from rich.spinner import Spinner

# ==============================
# CONSTANTS
# ==============================

from utils.constants import (
    CHOOSE_OPTION,
    INVALID_INPUT,
)

# ==============================
# CONFIGURATION
# ==============================

console = Console(width=100)


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
        confirmation_choice = get_input(f"Weet u zeker dat u wilt {action}? (Ja/Nee) ").lower()

        if confirmation_choice not in ("ja", "nee"):
            print_message(INVALID_INPUT, "red")
            continue

        return confirmation_choice == "ja"


def get_menu_choice(valid_choices):
    """
    Requests and validates a numeric menu choice.

    Args:
        valid_choices (range or collection): The allowed menu choices.

    Returns:
        int: The validated menu choice.
    """
    while True:
        try:
            menu_choice = int(get_input(f"{CHOOSE_OPTION}"))

        except ValueError:
            print_message(INVALID_INPUT, "red")
            continue

        if menu_choice not in valid_choices:
            print_message(INVALID_INPUT, "red")
            continue

        print()
        return menu_choice


def print_message(message, color=""):
    """
    Prints a formatted message with optional text and background colors.

    Args:
        message (str): The message to display.
        color (str): The optional text color.
    """

    console.print(
        Padding(f"{message}", (0, 5)),
        style=f"{color}",
    )


def get_input(message, color="bright_white"):
    return console.input(f"{' ' * 5}[{color}]{message}[/]")


def get_password(message, color="bright_white"):
    return console.input(f"{' ' * 5}[{color}]{message}[/]", password=True)


def display_page(location, title, content):
    clear_terminal()

    console.print(
        Padding(
            Panel(
                f"{content}",
                title=f"[bold bright_yellow]{location}[/] [bold bright_white]- {title}[/]",
                border_style="bright_yellow",
                padding=(1, 2),
            ),
            (1, 5))
    )

def display_panel(content, border_style="bright_yellow", title_color="bright_white", title="", title_align="left" ):
    console.print(
        Padding(
            Panel(
                f"{content}",
                border_style=border_style,
                title=f"[bold {title_color}]{title}[/]",
                title_align=title_align,
                padding=(1, 2),
            ),
            (0, 5)
        )
    )
    print()

def display_spinner(text, style="dots"):
    with Live(
            Padding.indent(
                Spinner(
                    style,
                    text=f"[bright_yellow]{text}, even geduld...[/]",
                    style="bright_yellow"
                ),
                5
            ),
            console=console,
            transient=True
    ):
        time.sleep(2)



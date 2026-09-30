import os
import subprocess


SEPARATOR = "-" * 50
CASINO_NAME = "Casino de Gouden Driehoek"
INVALID_INPUT = "\nOngeldige invoer. Probeer het opnieuw.\n"


def blank_lines(number):
    print("\n" * number, end="")


def format_currency(amount: int | float) -> str:
    if round(amount % 1, 2) == 0:
        return f"€{int(amount)},-"

    return f"€{amount:.2f}".replace(".", ",")


def clear_terminal():
    command = "cls" if os.name == "nt" else "clear"
    subprocess.run(command, shell=True, check=False)


def get_confirmation(playing_balance, action):
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
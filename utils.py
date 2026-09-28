import os
import subprocess


def blank_lines(number):
    print("\n" * number, end="")


def format_currency(amount: int | float) -> str:
    if round(amount % 1, 2) == 0:
        return f"€{int(amount)},-"

    return f"€{amount:.2f}".replace(".", ",")


def clear_terminal():
    command = "cls" if os.name == "nt" else "clear"
    subprocess.run(command, shell=True, check=False)
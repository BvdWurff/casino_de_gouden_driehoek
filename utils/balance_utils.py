# ==============================
# FUNCTION IMPORTS
# ==============================

import time

from rich.console import Console
from rich.padding import Padding
from rich.panel import Panel
from rich.live import Live
from rich.spinner import Spinner
from rich.console import Group

from utils.utils import (
    blank_lines,
    clear_terminal,
    format_currency,
    get_menu_choice,
    print_message,
    get_input,
)


# ==============================
# CONSTANTS
# ==============================

from utils.constants import (
    CASINO_NAME,
    CONTINUE_PROMPT,
    INVALID_INPUT,
    SEPARATOR,
    ADMISSION_PRICE,
    SERVICE_FEE,
    MANDATORY_DRINK_PRICE,
    VAT_RATE,
)


# ==============================
# CONFIGURATION
# ==============================

console = Console(width=100)


# ==============================
# BALANCE MANAGEMENT
# ==============================

def manage_balance(current_user, fixed_costs=0.0, trigger="") -> str:
    """
    Displays the balance menu and handles deposits and withdrawals.

    Args:
        current_user (dict): The profile of the current user.
        fixed_costs (int or float): The total fixed casino costs.
        trigger (str): Indicates why or from where the balance menu was opened.

    Returns:
        str: The action to perform.
    """
    while True:
        clear_terminal()

        page_name = "Saldo-overzicht"

        console.print(
            Padding(
                Panel(
                    "1. Saldo storten\n"
                    "2. Saldo opnemen\n\n"
                    "0. Terug",
                    title=f"[bold bright_yellow]{CASINO_NAME}[/] [bold bright_white]- {page_name}[/]",
                    border_style="bright_yellow",
                    padding=(1, 2),
                ),
                (1, 5))
        )

        menu_choice = get_menu_choice(range(0, 3))
        print()

        if menu_choice == 1:
            while True:
                try:
                    amount = round(float(get_input("Hoeveel wilt u storten? € ")), 2)
                except ValueError:
                    print_message(INVALID_INPUT, "red")
                    continue

                if amount < 0:
                    print_message(INVALID_INPUT, "red")
                    continue

                if amount == 0:
                    print_message("U keert terug naar het saldo-overzicht.")
                    blank_lines(2)
                    time.sleep(1)
                    break

                current_user["playing_balance"] = round(current_user["playing_balance"] + amount, 2)

                print()

                with Live(
                        Padding.indent(
                            Spinner(
                                "dots",
                                text="[bright_yellow]Verwerken, even geduld...[/]",
                                style="bright_yellow"
                            ),
                            5
                        ),
                        console=console,
                        transient=True
                ):
                    time.sleep(2)

                print_message("Het bedrag is succesvol gestort.", "green")
                print()
                get_input("Druk op Enter om terug te keren naar het saldo-overzicht.")
                break

        elif menu_choice == 2:
            if current_user["playing_balance"] <= 0:
                print()
                print_message("U heeft onvoldoende saldo voor deze opname.", "red")
                print()
                get_input(CONTINUE_PROMPT)

            else:
                while True:
                    try:
                        amount = round(float(get_input("Hoeveel wilt u opnemen? € ")), 2)
                    except ValueError:
                        print_message(INVALID_INPUT, "red")
                        continue

                    if amount < 0:
                        print_message(INVALID_INPUT, "red")
                        continue

                    if amount == 0:
                        print()
                        print_message("U keert terug naar het saldo-overzicht.")
                        time.sleep(1)
                        break

                    if amount > current_user["playing_balance"]:
                        print()
                        print_message("U heeft onvoldoende saldo voor deze opname.", "red")
                        print()
                        get_input(CONTINUE_PROMPT)
                        continue

                    current_user["playing_balance"] = round(current_user["playing_balance"] - amount, 2)

                    print()

                    with Live(
                            Padding.indent(
                                Spinner(
                                    "dots",
                                    text="[bright_yellow]Verwerken, even geduld...[/]",
                                    style="bright_yellow"
                                ),
                                5
                            ),
                            console=console,
                            transient=True
                    ):
                        time.sleep(2)

                    print_message("Het bedrag is succesvol opgenomen.", "green")
                    print()
                    get_input("Druk op Enter om terug te keren naar het saldo-overzicht.")
                    break

        elif menu_choice == 0:
            # Refund fixed costs when the guest leaves due to insufficient starting balance.
            if trigger == "insufficient_starting_balance":
                if current_user["playing_balance"] < 0:
                    current_user["playing_balance"] = round(current_user["playing_balance"] + fixed_costs, 2)
                    print_message("De vaste kosten zijn teruggestort.", "green")

                    return "end_program"

                print_message("Uw budget is voldoende voor toegang tot het casino.", "green")
                print()
                get_input("Druk op Enter om verder te gaan naar de lobby.")

                return "continue"

            print()

            return "continue"


def calculate_costs():
    """
    Calculates the VAT amount and total fixed casino costs.

    Returns:
        tuple: The VAT amount and total fixed costs.
    """
    subtotal = ADMISSION_PRICE + SERVICE_FEE + MANDATORY_DRINK_PRICE
    vat_amount = round(subtotal * (VAT_RATE / 100), 2)
    fixed_costs = round(subtotal + vat_amount, 2)

    return vat_amount, fixed_costs


def determine_balance_status(current_user):
    """
    Determines whether the playing balance is sufficient.

    Args:
        current_user (dict): The profile of the current user.

    Returns:
        tuple: The internal balance status and its Dutch display text.
    """
    if current_user["playing_balance"] >= 0:
        return "sufficient", "voldoende"

    return "insufficient", "onvoldoende"
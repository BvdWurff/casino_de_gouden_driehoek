# ==============================
# FUNCTION IMPORTS
# ==============================

import time

from utils.utils import (
    blank_lines,
    clear_terminal,
    format_currency,
    get_menu_choice,
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
# BALANCE MANAGEMENT
# ==============================

def manage_balance(current_user, fixed_costs=0.0, trigger="") -> str:
    """
    Displays the balance menu and handles deposits and withdrawals.

    Args:
        current_user (dict): The profile of the current user.
        fixed_costs (int or float): The fixed casino costs.
        trigger (str): Indicates why or from where the balance menu was opened.

    Returns:
        str: The action to perform.
    """
    while True:
        clear_terminal()

        print(f"""
{CASINO_NAME} - Saldo-overzicht
{SEPARATOR}
Huidig saldo: {format_currency(current_user["playing_balance"])}

1. Saldo storten
2. Saldo opnemen
0. Terug
{SEPARATOR}""")

        menu_choice = get_menu_choice(range(0, 3))
        print()

        if menu_choice == 1:
            while True:
                try:
                    amount = round(float(input("Hoeveel wilt u storten? € ")), 2)
                except ValueError:
                    print(INVALID_INPUT)
                    continue

                if amount < 0:
                    print(INVALID_INPUT)
                    continue

                if amount == 0:
                    print("U keert terug naar het saldo-overzicht.")
                    blank_lines(2)
                    time.sleep(1)
                    break

                current_user["playing_balance"] = round(current_user["playing_balance"] + amount, 2)

                time.sleep(1)
                print()
                print("...")
                time.sleep(1)
                print()
                print("Het bedrag is succesvol gestort.")
                blank_lines(2)
                input("Druk op Enter om terug te keren naar het saldo-overzicht.")
                break

        elif menu_choice == 2:
            if current_user["playing_balance"] <= 0:
                print()
                print("U heeft onvoldoende saldo voor deze opname.")
                print()
                input(CONTINUE_PROMPT)
                blank_lines(2)

            else:
                while True:
                    try:
                        amount = round(float(input("Hoeveel wilt u opnemen? € ")), 2)
                    except ValueError:
                        print(INVALID_INPUT)
                        continue

                    if amount < 0:
                        print(INVALID_INPUT)
                        continue

                    if amount == 0:
                        print()
                        print("U keert terug naar het saldo-overzicht.")
                        blank_lines(2)
                        time.sleep(1)
                        break

                    if amount > current_user["playing_balance"]:
                        print()
                        print("U heeft onvoldoende saldo voor deze opname.")
                        print()
                        input(CONTINUE_PROMPT)
                        continue

                    current_user["playing_balance"] = round(current_user["playing_balance"] - amount, 2)

                    time.sleep(1)
                    print()
                    print("...")
                    time.sleep(1)
                    print()
                    print("Het bedrag is succesvol opgenomen.")
                    blank_lines(2)
                    input("Druk op Enter om terug te keren naar het saldo-overzicht.")
                    break

        elif menu_choice == 0:
            # Refund fixed costs when the guest leaves due to insufficient starting balance.
            if trigger == "insufficient_starting_balance":
                if current_user["playing_balance"] < 0:
                    current_user["playing_balance"] = round(current_user["playing_balance"] + fixed_costs, 2)
                    print("De vaste kosten zijn teruggestort.")
                    blank_lines(2)

                    return "end_program"

                print("U heeft voldoende budget voor toegang tot het casino!")
                print(SEPARATOR)
                print()
                input("Druk op Enter om verder te gaan naar het hoofdmenu.")
                blank_lines(2)

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
        playing_balance (int or float): The current playing balance.

    Returns:
        tuple: The internal balance status and its Dutch display text.
    """
    if current_user["playing_balance"] >= 0:
        return "sufficient", "voldoende"

    return "insufficient", "onvoldoende"
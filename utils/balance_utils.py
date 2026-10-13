# ==============================
# FUNCTION IMPORTS
# ==============================

import time

from utils.utils import (
    format_currency,
    get_menu_choice,
    print_message,
    get_input,
    display_page,
    display_spinner,
)


# ==============================
# CONSTANTS
# ==============================

from utils.constants import (
    CASINO_NAME,
    CONTINUE_PROMPT,
    INVALID_INPUT,
    ADMISSION_PRICE,
    SERVICE_FEE,
    MANDATORY_DRINK_PRICE,
    VAT_RATE,
)


# ==============================
# BALANCE MANAGEMENT
# ==============================

def manage_balance(current_user, fixed_costs=0.0, trigger=""):
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
        page_content = f"""Uw huidige saldo bedraagt {format_currency(current_user["playing_balance"])}
        
1. Saldo storten
2. Saldo opnemen

0. Terug"""

        display_page(location=CASINO_NAME,
                     title="Saldo-overzicht",
                     content=page_content
                     )

        menu_choice = get_menu_choice(range(0, 3))

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
                    print()
                    print_message("U keert terug naar het saldo-overzicht.", "green")
                    time.sleep(1)
                    break

                current_user["playing_balance"] = round(current_user["playing_balance"] + amount, 2)

                print()
                display_spinner("Verwerken")

                print_message("Het bedrag is succesvol gestort.", "green")
                print()
                get_input(CONTINUE_PROMPT)
                break

        elif menu_choice == 2:
            if current_user["playing_balance"] <= 0:
                print()
                print_message("U heeft onvoldoende saldo voor een opname.", "red")
                print()
                get_input(CONTINUE_PROMPT)
                break

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
                        print_message("U keert terug naar het saldo-overzicht.", "green")
                        time.sleep(1)
                        break

                    if amount > current_user["playing_balance"]:
                        print()
                        print_message("U heeft onvoldoende saldo voor deze opname.", "red")
                        print()
                        continue

                    current_user["playing_balance"] = round(current_user["playing_balance"] - amount, 2)

                    print()
                    display_spinner("Verwerken")

                    print_message("Het bedrag is succesvol opgenomen.", "green")
                    print()
                    get_input(CONTINUE_PROMPT)
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
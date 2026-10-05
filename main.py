# ==============================
# FUNCTION IMPORTS
# ==============================

import datetime

from game_selection import (
    choose_game,
)
from utils.balance_utils import (
    manage_balance,
)
from profiles import (
    login,
    create_profile,
    show_profile,
)
from utils.utils import (
    blank_lines,
    clear_terminal,
    format_currency,
    get_confirmation,
    get_menu_choice,
)


# ==============================
# CONSTANTS
# ==============================

from utils.constants import (
    ADMISSION_PRICE,
    CASINO_NAME,
    MANDATORY_DRINK_PRICE,
    MIN_AGE,
    SEPARATOR,
    SERVICE_FEE,
    VAT_RATE,
)


# ==============================
# CONFIGURATION
# ==============================

TEST_MODE = False


# ==============================
# REGISTRATION AND ACCOUNT
# ==============================

def check_age(birth_date):
    """
    Checks whether the guest meets the minimum age requirement.

    Args:
        birth_date (datetime.datetime): The guest's birthdate.

    Returns:
        datetime.datetime: The birthdate if the age requirement is met.
    """
    current_date = datetime.datetime.now()
    minimum_age_year = birth_date.year + MIN_AGE

    # A February 29 birthdate may not exist in the year the minimum age is reached.
    # In that case, February 28 is used as the minimum-age birthday.
    if birth_date.day == 29 and birth_date.month == 2:
        minimum_age_birthday = datetime.datetime(minimum_age_year, 2, 28)
    else:
        minimum_age_birthday = birth_date.replace(year=minimum_age_year)

    if current_date < minimum_age_birthday:
        print(f"""
{SEPARATOR}
De minimale leeftijd voor {CASINO_NAME} is {MIN_AGE} jaar.
U heeft deze leeftijd nog niet bereikt.

U bent van harte welkom vanaf {minimum_age_birthday.strftime("%d-%m-%Y")}.
{SEPARATOR}""")

        exit(1)

    return birth_date


# ==============================
# COSTS AND BALANCE
# ==============================

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


def determine_balance_status(playing_balance):
    """
    Determines whether the playing balance is sufficient.

    Args:
        playing_balance (int or float): The current playing balance.

    Returns:
        tuple: The internal balance status and its Dutch display text.
    """
    if playing_balance >= 0:
        return "sufficient", "voldoende"

    return "insufficient", "onvoldoende"


# ==============================
# OUTPUT
# ==============================

def show_welcome_message():
    """
    Displays the casino welcome message.

    Returns:
        tuple: The current user, starting balance and trigger.
    """
    clear_terminal()

    trigger = "startpagina"
    starting_balance = 0.0
    current_user = {}

    print(f"""
{CASINO_NAME} - Startpagina
{SEPARATOR}
Welkom bij {CASINO_NAME}.

Voor de beste weergave wordt aangeraden het programma in een terminal uit te voeren
of in PyCharm “Emulate terminal in output console” in te schakelen.
""")

    while True:
        print(f"""{SEPARATOR}
1. Inloggen
2. Account aanmaken
0. Stoppen
{SEPARATOR}
""")

        menu_choice = get_menu_choice(range(0, 3))

        if menu_choice == 1:
            logged_in_user, starting_balance = login()

            if logged_in_user is None:
                continue

            current_user = logged_in_user
            trigger = "login"
            break

        elif menu_choice == 2:
            create_profile()
            trigger = "create_profile"
            continue

        elif menu_choice == 0:
            confirmation = get_confirmation("stoppen")

            if confirmation:
                blank_lines(2)
                show_parting_message(trigger=trigger)
                exit(0)

            blank_lines(2)

    return current_user, starting_balance, trigger


def show_registration_summary(
    current_user,
    starting_balance,
    vat_amount,
    fixed_costs,
    balance_status,
    balance_status_text,
    trigger,
):
    """
    Displays the guest's registration and cost summary.

    Args:
        current_user (dict): The profile of the user.
        starting_balance (int or float): The guest's initial budget.
        vat_amount (int or float): The VAT amount included in the fixed costs.
        fixed_costs (int or float): The total fixed casino costs.
        balance_status (str): The internal balance status.
        balance_status_text (str): The Dutch display text for the balance status.
        trigger (str): Location that triggered the function.
    """
    clear_terminal()

    print("Welkom", end="")

    if trigger == "login":
        print(" terug", end="")

    print(f""", {current_user["salutation"]}!

{CASINO_NAME} - Kostenoverzicht
{SEPARATOR}
Speelbudget:          {format_currency(starting_balance)}

Vaste kosten:
- Toegangskosten:   - {format_currency(ADMISSION_PRICE)}
- Servicekosten:    - {format_currency(SERVICE_FEE)}
- Consumptie:       - {format_currency(MANDATORY_DRINK_PRICE)}
- BTW ({VAT_RATE:.0f}%):        - {format_currency(vat_amount)}
Totaal:             - {format_currency(fixed_costs)}

Saldo:                {format_currency(current_user["playing_balance"])}
{SEPARATOR}
U heeft {balance_status_text} budget voor toegang tot het casino.
""")

    if balance_status == "insufficient":
        destination = "saldo-overzicht"
    else:
        destination = "hoofdmenu"

    input(f"Druk op Enter om door te gaan naar het {destination}.")
    blank_lines(2)


def show_parting_message(current_user=None, trigger=""):
    """
    Displays the checkout message and final playing balance.

    Args:
        current_user (dict or None): The profile of the current user.
        trigger (str): Location the function is triggered from.
    """
    clear_terminal()

    print(f"""
{CASINO_NAME} - Vertrek
{SEPARATOR}""")

    if trigger == "startpagina":
        print(f"""U verlaat het casino.
Bedankt voor uw bezoek aan {CASINO_NAME} en graag tot ziens!
{SEPARATOR}
""")

    elif current_user is not None:
        print(f"""U verlaat het casino met een eindsaldo van {format_currency(current_user["playing_balance"])}.

Bedankt voor uw bezoek aan {CASINO_NAME} en graag tot ziens!
{SEPARATOR}
""")


# ==============================
# MENUS
# ==============================

def main_menu(current_user):
    """
    Displays the main menu and handles the selected menu options.

    Args:
        current_user (dict): The profile of the user.
    """
    while True:
        clear_terminal()

        print(f"""
{CASINO_NAME} - Hoofdmenu
{SEPARATOR}
1. Spellen
2. Saldo
3. Profiel
0. Stoppen
{SEPARATOR}""")

        menu_choice = get_menu_choice(range(0, 4))

        if menu_choice == 1:
            if current_user["playing_balance"] <= 0:
                print()
                print("U heeft onvoldoende saldo om te spelen.")
                blank_lines(2)

                manage_balance(current_user)

            else:
                blank_lines(2)
                choose_game(current_user)

        elif menu_choice == 2:
            blank_lines(2)
            manage_balance(current_user)

        elif menu_choice == 3:
            blank_lines(2)
            show_profile(current_user)

        elif menu_choice == 0:
            confirmation = get_confirmation("stoppen")

            if confirmation:
                blank_lines(2)
                break

            blank_lines(2)


# ==============================
# PROGRAM FLOW
# ==============================

def main():
    """
    Controls the main program flow.
    """
    current_user, starting_balance, trigger = show_welcome_message()

    vat_amount, fixed_costs = calculate_costs()
    current_user["playing_balance"] = round(starting_balance - fixed_costs, 2)
    balance_status, balance_status_text = determine_balance_status(current_user["playing_balance"])

    show_registration_summary(
        current_user,
        starting_balance,
        vat_amount,
        fixed_costs,
        balance_status,
        balance_status_text,
        trigger,
    )

    while True:
        if balance_status == "sufficient":
            main_menu(current_user)
            break

        trigger = "insufficient_starting_balance"

        action = manage_balance(current_user, fixed_costs=fixed_costs, trigger=trigger)

        if action == "end_program":
            break

        balance_status, _ = determine_balance_status(current_user["playing_balance"])

    show_parting_message(current_user)
    exit(0)


if __name__ == "__main__":
    main()
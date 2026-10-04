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
    INVALID_INPUT,
    MANDATORY_DRINK_PRICE,
    MIN_AGE,
    SEPARATOR,
    SERVICE_FEE,
    VAT_RATE,
)


# ==============================
# REGISTRATION AND ACCOUNT
# ==============================

def get_user_input():
    """
    Collects and validates the guest's registration information.

    Returns:
        tuple: The guest's first name, surname, birthdate, gender
        and starting balance.
    """
    test_mode = False

    birth_date = None
    starting_balance = 0.0

    if test_mode:
        blank_lines(2)
        first_name = "Bart"
        surname = "van der Wurff"
        birth_date = datetime.datetime(1985, 8, 26)
        gender = "man"
        starting_balance = 100.00

    else:
        clear_terminal()

        print(f"""
Vul onderstaande gegevens in om toegang te krijgen.
{SEPARATOR}
""")

        while True:
            first_name = input("Wat is uw voornaam? ").title()

            if first_name.isalpha():
                break

            print(INVALID_INPUT)

        while True:
            surname_prefix = input(
                "Wat zijn uw tussenvoegsels? "
                "(druk op Enter indien niet van toepassing) "
            )

            if not surname_prefix or surname_prefix.replace(" ", "").isalpha():
                break

            print(INVALID_INPUT)

        while True:
            surname = input("Wat is uw achternaam? ").title()

            if surname.isalpha():
                break

            print(INVALID_INPUT)

        if surname_prefix:
            surname = f"{surname_prefix} {surname}"

        while True:
            birth_date_input = input("Wat is uw geboortedatum? (dd-mm-jjjj) ")

            try:
                birth_date = datetime.datetime.strptime(birth_date_input, "%d-%m-%Y")
            except ValueError:
                print(INVALID_INPUT)
                continue

            current_date = datetime.datetime.now()

            if current_date < birth_date:
                print(INVALID_INPUT)
                continue

            break

        while True:
            gender = input("Wat is uw geslacht? (Man/Vrouw/Anders) ").lower()

            if gender:
                break

            print(INVALID_INPUT)

        while True:
            try:
                starting_balance = round(float(input("Wat is uw speelbudget? € ")), 2)
            except ValueError:
                print(INVALID_INPUT)
                continue

            if starting_balance > 0:
                break

            print(INVALID_INPUT)

        print(SEPARATOR)
        print()

    return first_name, surname, birth_date, gender, starting_balance


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


def determine_salutation(first_name, surname, gender):
    """
    Determines the appropriate salutation for the guest.

    Args:
        first_name (str): The guest's first name.
        surname (str): The guest's surname.
        gender (str): The guest's gender.

    Returns:
        str: The salutation used to address the guest.
    """
    if gender == "man":
        salutation = f"meneer {surname}"
    elif gender == "vrouw":
        salutation = f"mevrouw {surname}"
    else:
        salutation = f"{first_name} {surname}"

    return salutation


def calculate_age(birth_date):
    """
    Calculates the guest's current age.

    Args:
        birth_date (datetime.datetime): The guest's birthdate.

    Returns:
        int: The guest's current age.
    """
    current_date = datetime.datetime.now()
    current_age = current_date.year - birth_date.year

    if (current_date.month, current_date.day) < (birth_date.month, birth_date.day):
        current_age -= 1

    return current_age


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


def calculate_starting_balance(starting_balance, fixed_costs) -> int | float:
    """
    Calculates the playing balance after deducting the fixed casino costs.

    Args:
        starting_balance (int or float): The guest's initial budget.
        fixed_costs (int or float): The total fixed casino costs.

    Returns:
        int or float: The initial playing balance.
    """
    playing_balance = starting_balance - fixed_costs
    return round(playing_balance, 2)


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
    """
    clear_terminal()

    print(f"""
{CASINO_NAME} - Startpagina
{SEPARATOR}
Welkom bij {CASINO_NAME}.

Voor de beste weergave wordt aangeraden het programma in een terminal uit te voeren
of in PyCharm “Emulate terminal in output console” in te schakelen.""")


def show_account(
    first_name,
    surname,
    gender,
    birth_date,
    age
):
    """
    Displays the guest's account information.

    Args:
        first_name (str): The guest's first name.
        surname (str): The guest's surname.
        gender (str): The guest's gender.
        birth_date (datetime.datetime): The guest's birthdate.
        age (int): The guest's current age.
    """
    clear_terminal()

    print(f"""
{CASINO_NAME} - Account
{SEPARATOR}
Naam:               {first_name} {surname}
Geslacht:           {gender.capitalize()}
Geboortedatum:      {birth_date.strftime("%d-%m-%Y")}
Leeftijd:           {age}
{SEPARATOR}
""")

    input("Druk op Enter om terug te gaan naar het hoofdmenu.")
    blank_lines(2)


def show_results(
    salutation,
    starting_balance,
    vat_amount,
    fixed_costs,
    playing_balance,
    balance_status,
    balance_status_text
):
    """
    Displays the guest's registration and cost summary.

    Args:
        salutation (str): The salutation used to address the guest.
        starting_balance (int or float): The guest's initial budget.
        vat_amount (int or float): The VAT amount included in the fixed costs.
        fixed_costs (int or float): The total fixed casino costs.
        playing_balance (int or float): The current playing balance.
        balance_status (str): The internal balance status.
        balance_status_text (str): The Dutch display text for the balance status.
    """
    clear_terminal()

    print(f"""
Welkom, {salutation}!

{CASINO_NAME} - Kostenoverzicht
{SEPARATOR}
Speelbudget:          {format_currency(starting_balance)}

Vaste kosten:
- Toegangskosten:   - {format_currency(ADMISSION_PRICE)}
- Servicekosten:    - {format_currency(SERVICE_FEE)}
- Consumptie:       - {format_currency(MANDATORY_DRINK_PRICE)}
- BTW ({VAT_RATE:.0f}%):        - {format_currency(vat_amount)}
Totaal:             - {format_currency(fixed_costs)}

Saldo:                {format_currency(playing_balance)}
{SEPARATOR}
U heeft {balance_status_text} budget voor toegang tot het casino.
""")

    if balance_status == "insufficient":
        destination = "saldo-overzicht"
    else:
        destination = "hoofdmenu"

    input(f"Druk op Enter om door te gaan naar het {destination}.")
    blank_lines(2)


def show_parting_message(playing_balance):
    """
    Displays the checkout message and final playing balance.

    Args:
        playing_balance (int or float): The guest's final playing balance.
    """
    clear_terminal()

    print(f"""
{CASINO_NAME} - Vertrek
{SEPARATOR}
U verlaat het casino met een eindsaldo van {format_currency(playing_balance)}.

Bedankt voor uw bezoek aan {CASINO_NAME} en graag tot ziens!
{SEPARATOR}
""")


# ==============================
# MENUS
# ==============================

def main_menu(
    playing_balance,
    first_name,
    surname,
    gender,
    birth_date,
    age
) -> int | float:
    """
    Displays the main menu and handles the selected menu options.

    Args:
        playing_balance (int or float): The current playing balance.
        first_name (str): The guest's first name.
        surname (str): The guest's surname.
        gender (str): The guest's gender.
        birth_date (datetime.datetime): The guest's birthdate.
        age (int): The guest's current age.

    Returns:
        int or float: The updated playing balance.
    """
    while True:
        clear_terminal()

        print(f"""
{CASINO_NAME} - Hoofdmenu
{SEPARATOR}
1. Spellen
2. Saldo
3. Account
0. Stoppen
{SEPARATOR}""")

        menu_choice = get_menu_choice(range(0, 4))

        if menu_choice == 1:
            if playing_balance <= 0:
                print()
                print("U heeft onvoldoende saldo om te spelen.")
                blank_lines(2)
                playing_balance, _ = manage_balance(playing_balance)
            else:
                blank_lines(2)
                playing_balance = choose_game(playing_balance)

        elif menu_choice == 2:
            blank_lines(2)
            playing_balance, _ = manage_balance(playing_balance)

        elif menu_choice == 3:
            blank_lines(2)
            show_account(first_name, surname, gender, birth_date, age)

        elif menu_choice == 0:
            confirmation = get_confirmation("stoppen")

            if confirmation:
                blank_lines(2)
                break

            blank_lines(2)

    return playing_balance


# ==============================
# PROGRAM FLOW
# ==============================

def main():
    """
    Controls the main program flow.
    """
    show_welcome_message()

    first_name, surname, birth_date, gender, starting_balance = get_user_input()
    birth_date = check_age(birth_date)
    salutation = determine_salutation(first_name, surname, gender)
    age = calculate_age(birth_date)

    vat_amount, fixed_costs = calculate_costs()
    playing_balance = calculate_starting_balance(starting_balance, fixed_costs)
    balance_status, balance_status_text = determine_balance_status(playing_balance)

    show_results(
        salutation,
        starting_balance,
        vat_amount,
        fixed_costs,
        playing_balance,
        balance_status,
        balance_status_text
    )

    while True:
        if balance_status == "sufficient":
            playing_balance = main_menu(
                playing_balance,
                first_name,
                surname,
                gender,
                birth_date,
                age
            )
            break

        trigger = "insufficient_starting_balance"
        playing_balance, action = manage_balance(playing_balance, fixed_costs=fixed_costs, trigger=trigger)

        if action == "end_program":
            break

        balance_status, _ = determine_balance_status(playing_balance)

    show_parting_message(playing_balance)
    exit(0)


if __name__ == "__main__":
    main()

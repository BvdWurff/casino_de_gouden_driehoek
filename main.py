import game_selection
from utils import blank_lines
import datetime
import time


# ==============================
# CONFIGURATION
# ==============================

SEPARATOR = "-" * 50
MIN_AGE = 18
INVALID_INPUT = "\nOngeldige invoer. Probeer het opnieuw.\n"
CASINO_NAME = "Casino de Gouden Driehoek"


# Fixed casino costs
ADMISSION_PRICE = 5.00
SERVICE_FEE = 3.50
MANDATORY_DRINK_PRICE = 2.70
VAT_RATE = 21.0


# ==============================
# REGISTRATION AND ACCOUNT
# ==============================

def show_welcome_message():
    print(f"""
{CASINO_NAME} - Startpagina
{SEPARATOR}
Welkom bij {CASINO_NAME}.""")


def get_user_input():
    """
    Collects and validates the guest's registration information.

    Returns:
        tuple: The guest's first name, surname, birth date, gender
        and starting balance.
    """
    print()
    test = input("Is dit een test run? (ja/nee) ").lower()
    if test == 'ja':
        blank_lines(2)
        first_name = 'Bart'
        surname = 'van der Wurff'
        birth_date = datetime.datetime(1985, 8, 26)
        gender = 'man'
        starting_balance = 100.00

    else:
        print(f"""
Vul onderstaande vragen in om toegang te krijgen.
{SEPARATOR}
""")
        while True:
            first_name = input("Wat is uw voornaam? ").title()

            if first_name.isalpha():
                break
            else:
                print(INVALID_INPUT)

        while True:
            surname_prefix = input("Wat zijn uw tussenvoegsels? (druk op Enter indien niet van toepassing) ")

            if not surname_prefix or surname_prefix.replace(" ", "").isalpha():
                break
            else:
                print(INVALID_INPUT)

        while True:
            surname = input("Wat is uw achternaam? ").title()

            if surname.isalpha():
                break
            else:
                print(INVALID_INPUT)

        if surname_prefix:
            surname = surname_prefix + " " + surname

        while True:
            try:
                date_of_birth = input("Wat is uw geboortedatum? (dd-mm-jjjj) ")
                birth_date = datetime.datetime.strptime(date_of_birth, "%d-%m-%Y")
                current_date = datetime.datetime.now()
                if current_date < birth_date:
                    print(INVALID_INPUT)
                else:
                    break
            except ValueError:
                print(INVALID_INPUT)

        while True:
            gender = input("Wat is uw geslacht? (Man / Vrouw / Anders) ").lower()

            if gender:
                break
            else:
                print(INVALID_INPUT)

        while True:
            try:
                starting_balance = float(input("Wat is uw speelbudget? € "))
                if starting_balance > 0:
                    break
                else:
                    print(INVALID_INPUT)
            except ValueError:
                print(INVALID_INPUT)

        print(SEPARATOR)
        print()

    return first_name, surname, birth_date, gender, starting_balance


def check_age(birth_date):
    """
    Checks whether the guest meets the minimum age requirement.

    Args:
        birth_date (datetime.datetime): The guest's date of birth.

    Returns:
        datetime.datetime: The birth date if the age requirement is met.
    """
    current_date = datetime.datetime.now()
    minimum_age_year = birth_date.year + MIN_AGE

    # For a birth date on February 29, the minimum age birthday may not exist,
    # because the corresponding year may not be a leap year.
    # In that case, use February 28 as the minimum age birthday
    if birth_date.day == 29 and birth_date.month == 2:
        minimum_age_birthday = datetime.datetime(minimum_age_year, 2, 28)
    else:
        minimum_age_birthday = birth_date.replace(year=minimum_age_year)

    if current_date < minimum_age_birthday:
        print(f"""
{SEPARATOR}
De minimale leeftijd voor {CASINO_NAME} is {MIN_AGE} jaar.
U heeft deze leeftijd nog niet bereikt.

U bent van harte welkom vanaf {minimum_age_birthday.day}-{minimum_age_birthday.month}-{minimum_age_birthday.year}.
{SEPARATOR}""")

        exit(1)
    else:
        return birth_date


def determine_salutation(first_name, surname, gender):
    if gender == "man":
        salutation = f"meneer {surname}"
    elif gender == "vrouw":
        salutation = f"mevrouw {surname}"
    else:
        salutation = f"{first_name} {surname}"
    return salutation


def calculate_age(birth_date):
    current_date = datetime.datetime.now()
    current_age = current_date.year - birth_date.year

    if (current_date.month, current_date.day) < (birth_date.month, birth_date.day):
        current_age -= 1

    return current_age


def show_account(first_name, surname, gender, birth_date, age):
    print(f"""{CASINO_NAME} - Account
{SEPARATOR}
Naam:               {first_name} {surname}
Geslacht:           {gender.capitalize()}
geboortedatum:      {birth_date.day}-{birth_date.month}-{birth_date.year}
leeftijd:           {age}
{SEPARATOR}
""")

    input("Druk op Enter om terug te gaan naar het hoofdmenu.")
    blank_lines(2)


# ==============================
# COSTS AND BALANCE
# ==============================

def calculate_costs():
    """
    Calculates the VAT amount and total fixed casino costs.

    Returns:
        tuple: The VAT amount and the total fixed costs.
    """
    subtotal = ADMISSION_PRICE + SERVICE_FEE + MANDATORY_DRINK_PRICE
    vat_amount = round(subtotal * (VAT_RATE / 100), 2)
    fixed_costs = subtotal + vat_amount

    return vat_amount, round(fixed_costs, 2)


def calculate_starting_balance(starting_balance, fixed_costs):
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
    else:
        return "insufficient", "onvoldoende"


def show_balance(playing_balance, fixed_costs=0.0, trigger=""):
    """
    Displays the balance menu and handles deposits and withdrawals.

    Args:
        playing_balance (int or float): The current playing balance.
        fixed_costs (int or float): The fixed casino costs.
        trigger (str): Indicates why the balance menu was opened.

    Returns:
        tuple: The updated playing balance and the action to perform.
    """
    while True:
        print(f"""{CASINO_NAME} - Saldo
{SEPARATOR}
Huidig saldo: € {playing_balance:.2f}

1. Saldo storten
2. Saldo opnemen
0. Terug
{SEPARATOR}""")

        try:
            choice = int(input("Kies een optie: "))
            print()
            if 0 <= choice <= 2:
                if choice == 1:
                    while True:
                        try:
                            amount = float(input("Hoeveel wilt u storten? € "))
                            if amount > 0:
                                playing_balance += amount
                                playing_balance = round(playing_balance, 2)
                                time.sleep(1)
                                print()
                                print("...")
                                time.sleep(1)
                                print()
                                print("Het bedrag is succesvol gestort.")
                                blank_lines(2)
                                time.sleep(1)
                                break
                            elif amount == 0:
                                print("U keert terug naar het Saldo menu")
                                blank_lines(2)
                                time.sleep(1)
                                break
                            else:
                                print(INVALID_INPUT)
                        except ValueError:
                            print(INVALID_INPUT)

                elif choice == 2:
                    if playing_balance <= 0:
                        print("U heeft onvoldoende saldo voor deze opname.")
                        blank_lines(2)
                    else:
                        while True:
                            try:
                                amount = float(input("Hoeveel wilt u opnemen? € "))
                                if amount > playing_balance:
                                    print()
                                    print("U heeft onvoldoende saldo voor deze opname.")
                                    print()
                                elif amount > 0:
                                    playing_balance -= amount
                                    playing_balance = round(playing_balance, 2)
                                    time.sleep(1)
                                    print()
                                    print("...")
                                    time.sleep(1)
                                    print()
                                    print("Het bedrag is succesvol opgenomen.")
                                    blank_lines(2)
                                    time.sleep(1)
                                    break
                                elif amount == 0:
                                    print()
                                    print("U keert terug naar het saldo-overzicht.")
                                    blank_lines(2)
                                    time.sleep(1)
                                    break
                                else:
                                    print(INVALID_INPUT)
                            except ValueError:
                                print(INVALID_INPUT)

                elif choice == 0:
                    # Refund fixed costs when the guest leaves due to insufficient starting balance
                    if trigger == "insufficient_starting_balance" and playing_balance < 0:
                        playing_balance += fixed_costs
                        print("De vaste kosten zijn teruggestort.")
                        blank_lines(2)
                        return playing_balance, "end_program"
                    elif trigger:
                        print(f"""U keert terug naar de {trigger}.


{CASINO_NAME} - {trigger.capitalize()}
{SEPARATOR}
Welkom terug bij de {trigger}.
""")
                        return playing_balance, "continue"

                    else:
                        print()
                        return playing_balance, "continue"
            else:
                print(INVALID_INPUT)
        except ValueError:
            print(INVALID_INPUT)
            print()
            time.sleep(1)


# ==============================
# MENUS AND OUTPUT
# ==============================

def show_results(salutation, starting_balance, vat_amount,
                 fixed_costs, playing_balance, balance_status_text):
    """
    Displays the guest's registration and cost summary.
    """
    print(f"""Welkom, {salutation}!


{CASINO_NAME} - Kostenoverzicht
{SEPARATOR}
Speelbudget:         €{starting_balance:.2f}

Vaste kosten:
- Toegangskosten:   -€{ADMISSION_PRICE:.2f}
- Service kosten:   -€{SERVICE_FEE:.2f}
- Consumptie:       -€{MANDATORY_DRINK_PRICE:.2f}
- BTW ({VAT_RATE:.0f}%):        -€{vat_amount:.2f}
Totaal:             -€{fixed_costs:.2f}

Saldo:               €{playing_balance:.2f}
{SEPARATOR}
U heeft {balance_status_text} budget voor toegang tot het casino.
""")
    input("Druk op Enter om door te gaan naar het hoofdmenu.")
    blank_lines(2)


def main_menu(playing_balance, first_name, surname, gender, birth_date, age):
    """
    Displays the main menu and handles the selected menu options.

    Args:
        playing_balance (int or float): The current playing balance.
        first_name (str): The guest's first name.
        surname (str): The guest's surname.
        gender (str): The guest's gender.
        birth_date (datetime.datetime): The guest's date of birth.
        age (int): The guest's current age.

    Returns:
        int or float: The updated playing balance.
    """
    while True:
        print(f"""{CASINO_NAME} - Hoofdmenu
{SEPARATOR}
1. Spellen
2. Saldo
3. Account
0. Stoppen
{SEPARATOR}""")
        try:
            choice = int(input("Kies een optie: "))
            blank_lines(2)
            if 0 <= choice <= 3:
                if choice == 1:
                    if playing_balance <= 0:
                        print("U heeft onvoldoende saldo om te spelen")
                        time.sleep(1)
                        playing_balance, _ = show_balance(playing_balance)
                    else:
                        playing_balance = game_selection.choose_game(playing_balance)
                elif choice == 2:
                    time.sleep(1)
                    playing_balance, _ = show_balance(playing_balance)
                elif choice == 3:
                    time.sleep(1)
                    show_account(first_name, surname, gender, birth_date, age)
                elif choice == 0:
                    return playing_balance
            else:
                print(INVALID_INPUT)
        except ValueError:
            print(INVALID_INPUT)
            print()
            time.sleep(1)


def show_parting_message(playing_balance):
    print(f"""{CASINO_NAME} - Checkout
{SEPARATOR}
U verlaat het casino met een eindsaldo van €{playing_balance:.2f}.

Bedankt voor uw bezoek aan {CASINO_NAME}
Graag tot ziens!
""")


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
    vat_amount, fixed_costs = calculate_costs()
    playing_balance = calculate_starting_balance(starting_balance, fixed_costs)
    balance_status, balance_status_text = determine_balance_status(playing_balance)
    age = calculate_age(birth_date)

    show_results(salutation, starting_balance, vat_amount,
                 fixed_costs, playing_balance, balance_status_text)

    while True:
        balance_status, balance_status_text = determine_balance_status(playing_balance)

        if balance_status == "sufficient":
            playing_balance = main_menu(playing_balance, first_name, surname, gender, birth_date, age)
            break
        else:
            time.sleep(1)
            trigger = "insufficient_starting_balance"
            playing_balance, action = show_balance(playing_balance, fixed_costs, trigger)
            if action == "end_program":
                break

    show_parting_message(playing_balance)
    exit(0)


if __name__ == "__main__":
    main()
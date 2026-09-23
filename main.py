import datetime
import game_selection

SEPARATOR = "-" * 32
MIN_AGE = 18
INVALID_ANSWER = "Ongeldige invoer. Probeer het opnieuw."
CASINO_NAME = "Casino de Gouden Driehoek"

# Vaste casino kosten
ADMISSION_PRICE = 5.00
SERVICE_FEE = 3.50
MANDATORY_DRINK_PRICE = 2.70
VAT_RATE = 21.0

def show_welcome_message():
    print(f'''
Welkom bij {CASINO_NAME}.
Vul onderstaande gegevens in om toegang te krijgen.
''')


def user_input():
    first_name = input("Wat is uw voornaam? ").title()
    while not first_name:
        print(INVALID_ANSWER)
        print()
        first_name = input("Wat is uw voornaam? ").title()
    infix = input("Wat zijn uw tussenvoegsels? (druk op Enter indien niet van toepassing) ")
    surname = input("Wat is uw achternaam? ").title()
    while not surname:
        print(INVALID_ANSWER)
        print()
        surname = input("Wat is uw achternaam? ").title()
    if infix:
        surname = infix + " " + surname
    date_of_birth = input("Wat is uw geboortedatum? (dd-mm-jjjj) ")
    while not date_of_birth:
        print(INVALID_ANSWER)
        print()
        date_of_birth = input("Wat is uw geboortedatum? (dd-mm-jjjj) ")
    birthdate = check_age(date_of_birth)
    gender = input("Wat is uw geslacht? (man/vrouw/anders) ").lower()
    while not gender:
        print(INVALID_ANSWER)
        print()
        gender = input("Wat is uw geslacht? (man/vrouw/anders) ").lower()
    while True:
        try:
            starting_balance = float(input("Wat is uw startbudget? €"))
            if starting_balance > 0:
                break
            else:
                print(INVALID_ANSWER)
        except ValueError:
            print(INVALID_ANSWER)

    return first_name, surname, birthdate, gender, starting_balance


def show_parting_message(playing_balance):
    print(f'''U verlaat het casino met een eindsaldo van €{playing_balance:.2f}.

Bedankt voor uw bezoek aan {CASINO_NAME}
Graag tot ziens!''')


def check_age(date_of_birth):
    # Huidige datum bepalen en geboortedatum omzetten naar een datetime-object
    current_date = datetime.datetime.now()
    birth_day, birth_month, birth_year = date_of_birth.split("-")
    birthdate = datetime.datetime(int(birth_year), int(birth_month), int(birth_day))

    # Datum berekenen waarop de gast de minimale leeftijd heeft
    minimum_age = birthdate.year + MIN_AGE

    # Bij een geboortedatum op 29-02 is er kans dat de datum van minimumleeftijd niet bestaat,
    # omdat het betreffende jaar geen schrikkeljaar is.
    # Gebruik in dat geval 28-02 als datum voor de minimumleeftijd
    if birthdate.day == 29 and birthdate.month == 2:
        minimum_age_birthday = datetime.datetime(minimum_age, 2, 28)
    else:
        minimum_age_birthday = birthdate.replace(year=minimum_age)

    if current_date < minimum_age_birthday:
        print(f'''
{SEPARATOR}{SEPARATOR}
De minimale leeftijd voor {CASINO_NAME} is {MIN_AGE} jaar.
U heeft deze leeftijd nog niet bereikt.

U bent van harte welkom vanaf {minimum_age_birthday.day}-{minimum_age_birthday.month}-{minimum_age_birthday.year}.
{SEPARATOR}{SEPARATOR}''')

        exit(1)
    else:
        return birthdate


def determine_salutation(first_name, surname, gender):
    # Bepaal aanspreekvorm
    if gender == "man":
        salutation = f"meneer {surname}"
    elif gender == "vrouw":
        salutation = f"mevrouw {surname}"
    else:
        salutation = f"{first_name} {surname}"
    return salutation


def hoofdmenu(playing_balance):
    print(f'''{CASINO_NAME} - Hoofdmenu
{SEPARATOR}
1. Spellen
2. Saldo
3. Account
0. Stop
''')

    while True:
        try:
            antwoord = int(input("Kies een optie: "))
            if 0 < antwoord <= 3:
                if antwoord == 1:
                    game_selection.choose_game(playing_balance)
                elif antwoord == 2:
                    show_balance(playing_balance)
                elif antwoord == 3:
                    account()
                elif antwoord == 0:
                    show_parting_message(playing_balance)
                    return
            else:
                print(INVALID_ANSWER)
        except ValueError:
            print(INVALID_ANSWER)


def account():
    pass

def show_results(salutation, starting_balance, vat_amount,
                 fixed_costs, playing_balance, balance_status):
    # Toon resultaat
    print(f'''
Welkom, {salutation}
{SEPARATOR}
Startbudget:         € {starting_balance:.2f}

Vaste kosten:
- Toegangskosten:    € {ADMISSION_PRICE:.2f}
- Service kosten:    € {SERVICE_FEE:.2f}
- Consumptie:        € {MANDATORY_DRINK_PRICE:.2f}
- BTW ({VAT_RATE:.0f}%):         € {vat_amount:.2f}
Totaal:              € {fixed_costs:.2f}

Saldo:               € {playing_balance:.2f}
{SEPARATOR}
U heeft {balance_status} budget voor toegang tot het casino.

''')

def calculate_costs():
    subtotal = ADMISSION_PRICE + SERVICE_FEE + MANDATORY_DRINK_PRICE
    vat_amount = round(subtotal * (VAT_RATE / 100), 2)
    fixed_costs = subtotal + vat_amount
    return vat_amount, fixed_costs

def calculate_playing_balance(starting_balance, fixed_costs):
    playing_balance = starting_balance - fixed_costs
    return playing_balance


def determine_balance_status(playing_balance):
    # Controleer of er voldoende budget is voor toegang tot het casino
    if playing_balance > 0:
        return "voldoende"
    else:
        return "onvoldoende"


def show_balance(playing_balance):
    print(f"Huidig saldo: € {playing_balance:.2f}")

def calculate_age(birthdate):
    current_date = datetime.datetime.now()
    current_age = current_date.year - birthdate.year

    if (current_date.month, current_date.day) < (birthdate.month, birthdate.day):
        current_age -= 1

    return current_age

def main():
    show_welcome_message()
    first_name, surname, birthdate, gender, starting_balance = user_input()
    salutation = determine_salutation(first_name, surname, gender)
    vat_amount, fixed_costs = calculate_costs()
    playing_balance = calculate_playing_balance(starting_balance, fixed_costs)
    balance_status = determine_balance_status(playing_balance)

    show_results(
        salutation,
        starting_balance,
        vat_amount,
        fixed_costs,
        playing_balance,
        balance_status
    )

    if determine_balance_status(playing_balance) == "voldoende":
        hoofdmenu(playing_balance)
    else:
        exit(0)

main()

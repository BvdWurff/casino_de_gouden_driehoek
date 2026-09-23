import datetime
import game_selection

SEPARATOR = "-" * 50
MIN_AGE = 18
INVALID_ANSWER = "Ongeldige invoer. Probeer het opnieuw.\n"
CASINO_NAME = "Casino de Gouden Driehoek"

# Vaste casino kosten
ADMISSION_PRICE = 5.00
SERVICE_FEE = 3.50
MANDATORY_DRINK_PRICE = 2.70
VAT_RATE = 21.0

def show_welcome_message():
    print(f'''
{CASINO_NAME} - Startpagina
{SEPARATOR}
Welkom bij {CASINO_NAME}.
Vul onderstaande vragen in om toegang te krijgen.

''')


def user_input():
    print(f'''{CASINO_NAME} - Registratie
{SEPARATOR}''')
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
    print(f'''{SEPARATOR}
''')

    return first_name, surname, birthdate, gender, starting_balance


def show_parting_message(playing_balance):
    print(f'''{CASINO_NAME} - Checkout
{SEPARATOR} 
U verlaat het casino met een eindsaldo van €{playing_balance:.2f}.

Bedankt voor uw bezoek aan {CASINO_NAME}
Graag tot ziens!
''')
    exit(0)


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
{SEPARATOR}
De minimale leeftijd voor {CASINO_NAME} is {MIN_AGE} jaar.
U heeft deze leeftijd nog niet bereikt.

U bent van harte welkom vanaf {minimum_age_birthday.day}-{minimum_age_birthday.month}-{minimum_age_birthday.year}.
{SEPARATOR}''')

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


def hoofdmenu(playing_balance, first_name, surname, gender, birthdate, age):
    while True:
        print(f'''{CASINO_NAME} - Hoofdmenu
{SEPARATOR}
1. Spellen
2. Saldo
3. Account
0. Stop
''')
        try:
            antwoord = int(input("Kies een optie: "))
            print()
            print()
            if 0 <= antwoord <= 3:
                if antwoord == 1:
                    if playing_balance <= 0:
                        print("U heeft onvoldoende saldo om te spelen")
                        playing_balance = show_balance(playing_balance)
                    else:
                        playing_balance = game_selection.choose_game(playing_balance)
                elif antwoord == 2:
                    playing_balance = show_balance(playing_balance)
                elif antwoord == 3:
                    account(first_name, surname, gender, birthdate, age)
                elif antwoord == 0:
                    return playing_balance
            else:
                print(INVALID_ANSWER)
        except ValueError:
            print(INVALID_ANSWER)


def account(first_name, surname, gender, birthdate, age):
    print(f'''{CASINO_NAME} - Account
{SEPARATOR}
Naam:               {first_name} {surname}
Geslacht:           {gender.capitalize()}
geboortedatum:      {birthdate.day}-{birthdate.month}-{birthdate.year}
leeftijd:           {age}   
{SEPARATOR}

''')


def show_results(salutation, starting_balance, vat_amount,
                 fixed_costs, playing_balance, balance_status):
    # Toon resultaat
    print(f'''Welkom, {salutation}!


{CASINO_NAME} - Kostenoverzicht
{SEPARATOR}
Startbudget:         €{starting_balance:.2f}

Vaste kosten:
- Toegangskosten:   -€{ADMISSION_PRICE:.2f}
- Service kosten:   -€{SERVICE_FEE:.2f}
- Consumptie:       -€{MANDATORY_DRINK_PRICE:.2f}
- BTW ({VAT_RATE:.0f}%):        -€{vat_amount:.2f}
Totaal:             -€{fixed_costs:.2f}

Saldo:               €{playing_balance:.2f}
{SEPARATOR}
U heeft {balance_status} budget voor toegang tot het casino.

''')

def calculate_costs():
    subtotal = ADMISSION_PRICE + SERVICE_FEE + MANDATORY_DRINK_PRICE
    vat_amount = round(subtotal * (VAT_RATE / 100), 2)
    fixed_costs = subtotal + vat_amount

    return vat_amount, round(fixed_costs, 2)

def calculate_starting_balance(starting_balance, fixed_costs):
    playing_balance = starting_balance - fixed_costs
    return round(playing_balance, 2)


def determine_balance_status(playing_balance):
    # Controleer of er voldoende budget is voor toegang tot het casino
    if playing_balance >= 0:
        return "voldoende"
    else:
        return "onvoldoende"


def show_balance(playing_balance, fixed_costs=0.0, trigger=""):
    while True:
        print(f'''{CASINO_NAME} - Saldo
{SEPARATOR} 
Huidig saldo: € {playing_balance:.2f}

1. Saldo storten
2. Saldo opnemen
0. Stop
''')

        try:
            antwoord = int(input("Kies een optie: "))
            print()
            if 0 <= antwoord <= 2:

                if antwoord == 1:
                    while True:
                        try:
                            amount = float(input("Hoeveel wilt u storten? € "))
                            if amount > 0:
                                playing_balance += amount
                                playing_balance = round(playing_balance, 2)
                                print("Het bedrag is succesvol gestort.")
                                print()
                                print()
                                break
                            elif amount == 0:
                                print("U keert terug naar het Saldo menu")
                                print()
                                print()
                                break
                            else:
                                print(INVALID_ANSWER)
                                print()
                        except ValueError:
                            print(INVALID_ANSWER)
                            print()

                elif antwoord == 2:
                    if playing_balance <= 0:
                        print('U heeft onvoldoende saldo voor deze opname.')
                        print()
                        print()
                    else:
                        while True:
                            try:
                                amount = float(input("Hoeveel wilt u opnemen? € "))
                                if  amount > playing_balance:
                                    print('U heeft onvoldoende saldo voor deze opname.')
                                    print()
                                elif amount > 0:
                                    playing_balance -= amount
                                    playing_balance = round(playing_balance, 2)
                                    print("Het bedrag is succesvol opgenomen")
                                elif amount == 0:
                                    print("U keert terug naar het Saldo menu")
                                    print()
                                    print()
                                    break
                                else:
                                    print(INVALID_ANSWER)
                            except ValueError:
                                print(INVALID_ANSWER)
                                print()

                elif antwoord == 0:
                    if trigger == "insufficient_starting_balance" and playing_balance < 0:

                        playing_balance += fixed_costs
                        print("De vaste kosten zijn teruggestort.")
                        print()
                        print()
                        show_parting_message(playing_balance)
                    else:
                        print()
                        return playing_balance
            else:
                print(INVALID_ANSWER)
                print()
        except ValueError:
            print(INVALID_ANSWER)
            print()

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

    playing_balance = calculate_starting_balance(starting_balance, fixed_costs)
    balance_status = determine_balance_status(playing_balance)
    age = calculate_age(birthdate)

    show_results(
        salutation,
        starting_balance,
        vat_amount,
        fixed_costs,
        playing_balance,
        balance_status
    )
    while True:
        balance_status = determine_balance_status(playing_balance)

        if balance_status == "voldoende":
            playing_balance = hoofdmenu(playing_balance, first_name, surname, gender, birthdate, age)
            break
        else:
            trigger = "insufficient_starting_balance"
            playing_balance = show_balance(playing_balance, fixed_costs, trigger)

    show_parting_message(playing_balance)

main()
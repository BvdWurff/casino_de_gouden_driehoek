import datetime
import game_selection

SEPARATOR = '-' * 32
MIN_AGE = 18
INVALID_ANSWER = "Ongeldige invoer. Probeer het opnieuw."

# Vaste casino kosten
ADMISSION_PRICE = 5.00
SERVICE_FEE = 3.50
MANDATORY_DRINK_PRICE = 2.70
VAT_RATE = 21.0

print()
print("Welkom bij Casino de Gouden Driehoek.")
print("Vul onderstaande gegevens in om toegang te krijgen.")
print()

# Invoer gebruikersgegevens + validatie of gegevens correct zijn ingevoerd.
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

# Huidige datum bepalen en geboortedatum omzetten naar een datetime-object
current_date = datetime.datetime.now()
birth_day, birth_month, birth_year = date_of_birth.split("-")
birth_date = datetime.datetime(int(birth_year), int(birth_month), int(birth_day))

# Datum berekenen waarop de gast de minimale leeftijd heeft
minimum_age = birth_date.year + MIN_AGE

# Bij een geboortedatum op 29-02 is er kans dat de datum van minimumleeftijd niet bestaat,
# omdat het betreffende jaar geen schrikkeljaar is.
# Gebruik in dat geval 28-02 als datum voor de minimumleeftijd
if birth_date.day == 29 and birth_date.month == 2:
    minimum_age_birthday = datetime.datetime(minimum_age, 2, 28)
else:
    minimum_age_birthday = birth_date.replace(year=minimum_age)

if current_date < minimum_age_birthday:
    print()
    print(f"De minimale leeftijd voor Casino de Gouden Driehoek is {MIN_AGE} jaar.")
    print("U heeft deze leeftijd nog niet bereikt.")
    print(f"U bent van harte welkom vanaf {minimum_age_birthday.day}-{minimum_age_birthday.month}-{minimum_age_birthday.year}.")
    exit(1)

# Bepaal aanspreekvorm
if gender == "man":
    salutation = f"meneer {surname}"
elif gender == "vrouw":
    salutation = f"mevrouw {surname}"
else:
    salutation = f"{first_name} {surname}"

# Bereken vaste kosten
subtotal = ADMISSION_PRICE + SERVICE_FEE + MANDATORY_DRINK_PRICE
vat_amount = round(subtotal * (VAT_RATE / 100), 2)
fixed_costs = subtotal + vat_amount

# Controleer of er voldoende budget is voor toegang tot het casino
playing_balance = starting_balance - fixed_costs
if playing_balance > 0:
    balance_status = "voldoende"
else:
    balance_status = "onvoldoende"

# Toon resultaat
print()
print()
print(f"Welkom, {salutation}")
print(SEPARATOR)
print(f"Startbudget:         € {starting_balance:.2f}")
print()
print("Vaste kosten:")
print(f"- Toegangskosten:    € {ADMISSION_PRICE:.2f}")
print(f"- Service kosten:    € {SERVICE_FEE:.2f}")
print(f"- Consumptie:        € {MANDATORY_DRINK_PRICE:.2f}")
print(f"- BTW ({VAT_RATE:.0f}%):         € {vat_amount:.2f}")
print(f"Totaal:              € {fixed_costs:.2f}")
print()
print(f"Saldo:               € {playing_balance:.2f}")
print(SEPARATOR)
print(f"U heeft {balance_status} budget voor toegang tot het casino.")
print()

if balance_status == "voldoende":
    game_selection.choose_game(playing_balance)

import json
import time
import datetime

from utils.utils import (
    clear_terminal,
    get_menu_choice,
    print_message,
    format_currency,
)

from utils.constants import (
    CASINO_NAME,
    CONTINUE_PROMPT,
    INVALID_INPUT,
    SEPARATOR,
    GREEN,
    RED,
    ADMISSION_PRICE,
    SERVICE_FEE,
    MANDATORY_DRINK_PRICE,
    VAT_RATE,
    MIN_AGE
)


with open("data/profiles.json", "r") as file:
    profiles = json.load(file)


def load_profiles():
    pass


def save_profiles(current_user):

    persistent_fields = {
        "password",
        "first_name",
        "surname_prefix",
        "surname",
        "birth_date",
        "gender",
        "playing_balance",
        "source",
        "role",
        "delete_requested",
        "visits",
        "played_games"
    }

    username = current_user["username"]

    if username not in profiles:
        profiles[username] = {}

    for field in persistent_fields:
        profiles[username][field] = current_user[field]

    with open("data/profiles.json", "w") as file:
        json.dump(profiles, file, indent=4)


def login(current_user):
    """
    Logs in to a user profile.

    Returns:
        tuple: The current user profile and starting balance.
    """
    while True:
        clear_terminal()
        profile = {}

        print(f"""
{CASINO_NAME} - Inlogpagina
{SEPARATOR}
""")

        while True:
            username = input("Gebruikersnaam: ").lower()

            if username:
                break

            print(INVALID_INPUT)

        while True:
            password = input("Wachtwoord: ")

            if password:
                break

            print(INVALID_INPUT)

        print()
        print(SEPARATOR)
        input("Druk op Enter om in te loggen.")

        print()
        time.sleep(1)
        print(".", end="")
        time.sleep(1)
        print(".", end="")
        time.sleep(1)
        print(".", end="\n")
        time.sleep(0.5)

        if username not in profiles:
            username = False
            print_message("Onbekende gebruikersnaam", RED)

        else:
            profile = profiles[username]

            if password != profile["password"]:
                password = False
                print_message("Ongeldig wachtwoord", RED)

        if username and password:
            if len(current_user) == 0:
                print_message("U bent succesvol ingelogd.", GREEN)
            else:
                save_profiles(current_user)
                print_message("U bent succesvol van profiel gewisseld.", GREEN)

            input(CONTINUE_PROMPT)
            break

        else:
            print(f"""{SEPARATOR}
1. Nogmaals proberen
2. Account aanmaken
0. Terug
{SEPARATOR}""")

            menu_choice = get_menu_choice(range(0, 3))

            if menu_choice == 1:
                continue

            elif menu_choice == 2:
                profile, username = create_profile()
                break

            elif menu_choice == 0:
                return None, 0.0

    current_user = build_player_profile(profile, username)
    starting_balance = current_user["playing_balance"]
    current_user["visits"] += 1

    show_welcome_message(current_user)

    return current_user, starting_balance


def create_profile():
    """
    Creates a new user profile.

    Returns:
        tuple: The newly created user profile and username.
    """
    birth_date = None
    starting_balance = 0.0

    clear_terminal()

    print(f"""
{CASINO_NAME} - Registreren
{SEPARATOR}

Vul onderstaande gegevens in om een profiel aan te maken.

{SEPARATOR}
""")

    while True:
        username = input("Kies een gebruikersnaam: ").lower()

        if username:
            if username in profiles:
                print_message("Gebruikersnaam al in gebruik.", RED)
                continue

            break

        print(INVALID_INPUT)

    while True:
        password = input("Geef een wachtwoord op: ")

        if password:
            confirm_password = input("Bevestig het wachtwoord: ")

            if password == confirm_password:
                break

            else:
                print_message("Wachtwoorden komen niet overeen.", RED)
                continue

    while True:
        first_name = input("Wat is uw voornaam? ").title()

        if first_name.replace("-", "").replace(" ", "").isalpha():
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

        if surname.replace("-", "").replace(" ", "").isalpha():
            break

        print(INVALID_INPUT)

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

        birth_date = birth_date.strftime("%d-%m-%Y")
        break

    while True:
        gender = input("Wat is uw geslacht? (bijv. Man/Vrouw/Anders) ").lower()

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

    current_user = {
        "username": username,
        "password": password,
        "first_name": first_name,
        "surname_prefix": surname_prefix,
        "surname": surname,
        "birth_date": birth_date,
        "gender": gender,
        "playing_balance": starting_balance,
        "source": "user",
        "role": "user",
        "delete_requested": False,
        "visits": 0,
        "played_games": {}
    }

    birth_date = datetime.datetime.strptime(birth_date_input, "%d-%m-%Y")
    check_age(birth_date)

    save_profiles(current_user)

    print_message("Account succesvol aangemaakt.", GREEN)

    input(CONTINUE_PROMPT)


def delete_profile():
    deleted_profiles = []

    for profile in list(profiles):
        deleted_profiles.append(profiles.pop(profile))

    number_of_accounts = len(deleted_profiles)

    print()

    if number_of_accounts == 0:
        print("Geen accounts verwijderd.")

    elif number_of_accounts == 1:
        print("Account succesvol verwijderd.")

    else:
        print(f"Succesvol {number_of_accounts} accounts verwijderd.")

    print()
    input(CONTINUE_PROMPT)


def update_profile():
    pass


def show_profile(current_user):
    clear_terminal()

    print(f"""
{CASINO_NAME} - Profiel
{SEPARATOR}
Voornaam:           {current_user["first_name"]}
Achternaam:         {current_user["full_surname"]}
Geslacht:           {current_user["gender"].capitalize()}
Geboortedatum:      {current_user["birth_date"]}
Leeftijd:           {current_user["age"]}
Saldo:              {format_currency(current_user["playing_balance"])}
{SEPARATOR}
""")

    input(CONTINUE_PROMPT)


def show_all_profiles():
    pass


def build_player_profile(profile, username):
    current_user = profile.copy()

    birth_date = datetime.datetime.strptime(current_user["birth_date"], "%d-%m-%Y")

    current_user["username"] = username
    current_user["age"] = calculate_age(birth_date)
    current_user["full_surname"] = determine_full_surname(current_user["surname_prefix"], current_user["surname"])
    current_user["full_name"] = determine_full_name(
        current_user["first_name"],
        current_user["surname_prefix"],
        current_user["surname"]
    )
    current_user["salutation"] = determine_salutation(
        current_user["full_surname"],
        current_user["full_name"],
        current_user["gender"]
    )

    return current_user


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


def determine_salutation(full_surname, full_name, gender):
    """
    Determines the appropriate salutation for the guest.

    Args:
        full_surname (str): The guest's full surname.
        full_name (str): The guest's full name.
        gender (str): The guest's gender.

    Returns:
        str: The salutation used to address the guest.
    """
    if gender == "man":
        salutation = f"meneer {full_surname}"
    elif gender == "vrouw":
        salutation = f"mevrouw {full_surname}"
    else:
        salutation = full_name

    return salutation


def determine_full_name(first_name, surname_prefix, surname):
    full_name = first_name.capitalize()

    if surname_prefix:
        full_name += f" {surname_prefix}"

    full_name += f" {surname.capitalize()}"

    return full_name


def determine_full_surname(surname_prefix, surname):
    full_surname = ""

    if surname_prefix:
        full_surname += f"{surname_prefix.capitalize()} {surname.capitalize()}"
    else:
        full_surname += surname.capitalize()

    return full_surname


def show_registration_summary(
    current_user,
    starting_balance,
    vat_amount,
    fixed_costs,
    balance_status,
    balance_status_text,
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
    """
    clear_terminal()
    print(f"""
{CASINO_NAME} - Welkomstpagina
{SEPARATOR}
Welkom, {current_user["salutation"]}!

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
        destination = "het saldo-overzicht"
    else:
        destination = "de lobby"

    input(f"Druk op Enter om door te gaan naar {destination}.")


def show_welcome_message(current_user):
    clear_terminal()
    print(f"""
{CASINO_NAME} - Welkomstpagina
{SEPARATOR}
Welkom terug, {current_user["salutation"]}!

Uw huidige saldo is {format_currency(current_user["playing_balance"])}.
{SEPARATOR}
""")
    input(CONTINUE_PROMPT)


def show_profile_menu(current_user):
    while True:
        clear_terminal()

        print(f"""
{CASINO_NAME} - Profielbeheer
{SEPARATOR}
1. Mijn profiel
2. Nieuw profiel aanmaken
3. Profiel verwijderen
4. Van profiel wisselen
5. Alle profielen inzien

0. Terug
{SEPARATOR}""")

        menu_choice = get_menu_choice(range(0, 6))

        if menu_choice == 1:
            show_profile(current_user)
            continue

        if menu_choice == 2:
            create_profile()
            continue

        if menu_choice == 4:
            login(current_user)
            break
    return



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
        clear_terminal()

        print(f"""
{CASINO_NAME} - Vertrek
{SEPARATOR}
De minimale leeftijd voor {CASINO_NAME} is {MIN_AGE} jaar.
U heeft deze leeftijd nog niet bereikt.

U bent van harte welkom vanaf {minimum_age_birthday.strftime("%d-%m-%Y")}.
{SEPARATOR}
""")
        input("Druk op Enter om het casino te verlaten.")
        print()

        exit(1)

    return
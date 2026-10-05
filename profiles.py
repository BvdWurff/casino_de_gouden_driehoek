import json
import time
import datetime

from utils.utils import (
    clear_terminal,
    get_menu_choice,
    blank_lines,
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
)


with open("data/profiles.json", "r") as file:
    profiles = json.load(file)


def load_profiles():
    pass


def save_profiles(profiles):
    with open("data/profiles.json", "w") as file:
        json.dump(profiles, file, indent=4)


def login():
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
            print_message("U bent succesvol ingelogd.", GREEN)
            input(CONTINUE_PROMPT)
            break

        else:
            print(f"""{SEPARATOR}
1. Nogmaals proberen
2. Account aanmaken
0. Terug naar Welkomstpagina
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

Vul onderstaande gegevens in om een account aan te maken.

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
    print()

    profiles[username] = {
        "password": password,
        "first_name": first_name,
        "surname_prefix": surname_prefix,
        "surname": surname,
        "birth_date": birth_date,
        "gender": gender,
        "playing_balance": starting_balance,
        "source": "user",
        "role": "user",
        "delete_requested": False
    }

    save_profiles(profiles)

    print_message("Account succesvol aangemaakt.", GREEN)
    input(CONTINUE_PROMPT)

    return profiles[username], username


def delete_profile(profiles):
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

    input("Druk op Enter om terug te gaan naar het hoofdmenu.")


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
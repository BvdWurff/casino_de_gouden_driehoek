import json

with open("data/profiles.json", "r") as file:
    profiles = json.load(file)

import time
import datetime

from utils.utils import (
    clear_terminal,
    get_menu_choice,
    blank_lines,
    print_message,
)

from utils.constants import (
    CASINO_NAME,
    CONTINUE_PROMPT,
    INVALID_INPUT,
    SEPARATOR,
    GREEN,
    RED,
    RESET, WHITE_BACKGROUND,
)

TEST_MODE = False


def load_profiles():
    pass


def save_profiles(profiles):
    with open("data/profiles.json", "w") as file:
        json.dump(profiles, file, indent=4)


def login():
    """
    Logs in to a user profile.

    Returns:
        dict: The newly created user profile.
    """

    while True:
        clear_terminal()
        current_user = {}

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
            current_user = profiles[username]

            if password != current_user["password"]:
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
                current_user = create_profile()
                break

            elif menu_choice == 0:
                break

        break

    starting_balance = current_user["playing_balance"]

    return current_user, starting_balance


def create_profile():
    """
    Creates a new user profile.

    Returns:
        dict: The newly created user profile.
    """
    birth_date = None
    current_user = None
    starting_balance = 0.0

    if TEST_MODE:
        blank_lines(2)
        first_name = "Bart"
        surname = "van der Wurff"
        birth_date = datetime.datetime(1985, 8, 26)
        gender = "man"
        starting_balance = 100.00

    else:
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
            playing_balance = 0,0
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
            "playing_balance": 0.0,
            "source": "user"
        }

        save_profiles(profiles)
        current_user = profiles[username]

    return current_user, starting_balance



def delete_profile():
    pass

def update_profile():
    pass

def show_profile():
    pass

def show_all_profiles():
    pass

def build_player_profile():
    pass


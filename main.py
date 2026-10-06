# ==============================
# FUNCTION IMPORTS
# ==============================

from game_selection import (
    choose_game,
)
from utils.balance_utils import (
    manage_balance,
    determine_balance_status,
    calculate_costs,
)
from profiles import (
    login,
    create_profile,
    save_profiles,
    show_registration_summary,
    show_profile_menu,
)
from utils.utils import (
    blank_lines,
    clear_terminal,
    format_currency,
    get_confirmation,
    get_menu_choice,
    print_message,
)

# ==============================
# CONSTANTS
# ==============================

from utils.constants import (
    CASINO_NAME,
    SEPARATOR, CONTINUE_PROMPT,
    RED,
)


# ==============================
# CONFIGURATION
# ==============================


# ==============================
# OUTPUT
# ==============================

def show_login_page():
    """
    Displays the casino welcome message and login menu

    Returns:
        tuple: The current user, starting balance and trigger.
    """
    while True:
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

        print(f"""{SEPARATOR}
1. Inloggen
2. Account aanmaken
0. Stoppen
{SEPARATOR}
""")

        menu_choice = get_menu_choice(range(0, 3))

        if menu_choice == 1:
            logged_in_user, starting_balance = login(current_user)

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
{CASINO_NAME} - Lobby
{SEPARATOR}
1. Spellen
2. Saldo
3. Profiel
0. Uitloggen
{SEPARATOR}""")

        menu_choice = get_menu_choice(range(0, 4))

        if menu_choice == 1:
            if current_user["playing_balance"] <= 0:
                print()
                print_message("U heeft onvoldoende saldo om te spelen.", RED)
                print()
                input(CONTINUE_PROMPT)

                manage_balance(current_user)

            else:
                blank_lines(2)
                choose_game(current_user)

        elif menu_choice == 2:
            manage_balance(current_user)

        elif menu_choice == 3:
            show_profile_menu(current_user)

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
    current_user, starting_balance, trigger = show_login_page()
    vat_amount, fixed_costs = calculate_costs()

    if current_user["visits"] == 1:
        current_user["playing_balance"] = round(starting_balance - fixed_costs, 2)
        balance_status, balance_status_text = determine_balance_status(current_user)

        show_registration_summary(
            current_user,
            starting_balance,
            vat_amount,
            fixed_costs,
            balance_status,
            balance_status_text,
        )

    else:
        balance_status, balance_status_text = determine_balance_status(current_user)

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
    save_profiles(current_user)
    exit(0)


if __name__ == "__main__":
    main()
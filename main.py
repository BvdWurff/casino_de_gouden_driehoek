# ==============================
# FUNCTION IMPORTS
# ==============================

from rich.console import Console
from rich.padding import Padding

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
    format_currency,
    get_confirmation,
    get_menu_choice,
    print_message,
    get_input,
    display_page,
    display_menu_table,
)

# ==============================
# CONSTANTS
# ==============================

from utils.constants import (
    CASINO_NAME,
    CONTINUE_PROMPT,
)


# ==============================
# CONFIGURATION
# ==============================

console = Console(width=80)


# ==============================
# OUTPUT
# ==============================

def show_parting_message(current_user=None, trigger=""):
    """
    Displays the checkout message and final playing balance.

    Args:
        current_user (dict or None): The profile of the current user.
        trigger (str): Location the function is triggered from.
    """
    if trigger == "start_page":
        content = f"""U verlaat het casino.
Bedankt voor uw bezoek aan {CASINO_NAME} en graag tot ziens!"""

    else:
        content = f"""U verlaat het casino met een eindsaldo van {format_currency(current_user["playing_balance"])}.
Bedankt voor uw bezoek aan {CASINO_NAME} en graag tot ziens!"""


    display_page(location=CASINO_NAME,
                 title="Vertrek",
                 content=content
                 )


# ==============================
# MENUS AND NAVIGATION
# ==============================

def show_login_page():
    """
    Displays the login menu

    Returns:
        tuple: The current user and starting balance.
    """
    while True:
        starting_balance = 0.0
        current_user = {}

        content = f"""Welkom bij {CASINO_NAME}!

Voor de beste weergave wordt aangeraden het programma in een [i]terminal[/] uit te voeren
of in PyCharm [i]Emulate terminal in output console[/] in te schakelen."""

        display_page(location=CASINO_NAME,
                     title="Inlogpagina",
                     content=content
                     )

        menu_options = ["Inloggen", "Profiel aanmaken", "", "Stoppen"]

        console.print(
            Padding(display_menu_table(menu_options, width=70), (0, 0, 1, 5))
        )

        menu_choice = get_menu_choice(range(0, 3))

        if menu_choice == 1:
            logged_in_user, starting_balance = login(current_user)

            if logged_in_user is None:
                continue

            current_user = logged_in_user
            break


        elif menu_choice == 2:
            current_user = create_profile()

            if current_user is None:
                continue

            starting_balance = current_user["playing_balance"]
            current_user["visits"] += 1
            break

        elif menu_choice == 0:
            confirmation = get_confirmation("stoppen")

            if confirmation:
                show_parting_message(trigger="start_page")
                exit(0)

    return current_user, starting_balance,


def main_menu(current_user):
    """
    Displays the main menu and handles the selected menu options.

    Args:
        current_user (dict): The profile of the current user.

    Returns:
        dict: The active user profile.
    """
    while True:
        content = "U bevindt zich in de lobby van het casino."

        display_page(location=CASINO_NAME,
                     title="Lobby",
                     content=content
                     )

        menu_options = ["Spellen", "Saldo", "Profiel", "", "Casino verlaten"]

        console.print(
            Padding(display_menu_table(menu_options, width=70), (0, 0, 1, 5))
        )

        menu_choice = get_menu_choice(range(0, 4))

        if menu_choice == 1:
            if current_user["playing_balance"] <= 0:
                print()
                print_message("U heeft onvoldoende saldo om te spelen.", "red")
                print()
                get_input(CONTINUE_PROMPT)

                manage_balance(current_user)

            else:
                choose_game(current_user)

        elif menu_choice == 2:
            manage_balance(current_user)

        elif menu_choice == 3:
            current_user = show_profile_menu(current_user)

        elif menu_choice == 0:
            confirmation = get_confirmation("stoppen")

            if confirmation:
                break

    return current_user


# ==============================
# PROGRAM FLOW
# ==============================

def main():
    """
    Controls the main program flow.
    """
    current_user, starting_balance = show_login_page()
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
        balance_status, _ = determine_balance_status(current_user)

    while True:
        if balance_status == "sufficient":
            current_user = main_menu(current_user)
            break

        action = manage_balance(current_user, fixed_costs=fixed_costs, trigger="insufficient_starting_balance")

        if action == "end_program":
            break

        balance_status, _ = determine_balance_status(current_user)

    show_parting_message(current_user)
    save_profiles(current_user)
    exit(0)


if __name__ == "__main__":
    main()
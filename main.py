# ==============================
# FUNCTION IMPORTS
# ==============================

from rich.console import Console
from rich.panel import Panel
from rich import print
from rich.console import Group
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
    blank_lines,
    clear_terminal,
    format_currency,
    get_confirmation,
    get_menu_choice,
    print_message,
    get_input,
)

# ==============================
# CONSTANTS
# ==============================

from utils.constants import (
    CASINO_NAME,
    CONTINUE_PROMPT,
    RED,
)

# ==============================
# CONFIGURATION
# ==============================

console = Console(width=100)


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
    clear_terminal()

    page_name = "Vertrek"

    if trigger == "start_page":
        console.print(
            Padding(
                Panel(
                    "U verlaat het casino."
                    f"Bedankt voor uw bezoek aan {CASINO_NAME} en graag tot ziens!",
                    title=f"[bold bright_yellow]{CASINO_NAME}[/] [bold bright_white]- {page_name}[/]",
                    border_style="bright_yellow",
                    padding=(1, 2),
                ),
                (1, 5))
        )

    elif current_user is not None:
        console.print(
            Padding(
                Panel(
                    f"U verlaat het casino met een eindsaldo van {format_currency(current_user["playing_balance"])}.\n\n"
                    f"Bedankt voor uw bezoek aan {CASINO_NAME} en graag tot ziens!",
                    title=f"[bold bright_yellow]{CASINO_NAME}[/] [bold bright_white]- {page_name}[/]",
                    border_style="bright_yellow",
                    padding=(1, 2),
                ),
                (1, 5))
        )


# ==============================
# MENUS AND NAVIGATION
# ==============================

def show_welcome_page():
    """
    Displays the casino welcome message

    """
    clear_terminal()

    page_name = "Startpagina"

    console.print(
        Padding(
            Group(
                Panel(
                    f"Welkom bij {CASINO_NAME}!\n\n"
                    "Voor de beste weergave wordt aangeraden het programma in een [i]terminal[/] uit te voeren\n"
                    "of in PyCharm [i]Emulate terminal in output console[/] in te schakelen.",
                    title=f"[bold bright_yellow]{CASINO_NAME}[/] [bold bright_white]- {page_name}[/]",
                    border_style="bright_yellow",
                    padding=(1, 2),
                ),
                f"\n[bright_white]{CONTINUE_PROMPT}[/]",
            ),
        (1,5))
    )

    input()

def show_login_page():
    """
    Displays the login menu

    Returns:
        tuple: The current user and starting balance.
    """
    while True:
        clear_terminal()

        page_name = "Inlogpagina"
        starting_balance = 0.0
        current_user = {}

        console.print(
            Padding(
                Panel(
                    "1. Inloggen\n"
                    "2. Profiel aanmaken\n\n"
                    "0. Stoppen",
                    title=f"[bold bright_yellow]{CASINO_NAME}[/] [bold bright_white]- {page_name}[/]",
                    border_style="bright_yellow",
                    padding=(1, 2),
                ),
            (1,5))
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
            print()
            confirmation = get_confirmation("stoppen")

            if confirmation:
                blank_lines(2)
                show_parting_message(trigger="start_page")
                exit(0)

            blank_lines(2)

    return current_user, starting_balance,


def main_menu(current_user):
    """
    Displays the main menu and handles the selected menu options.

    Args:
        current_user (dict): The profile of the current user.
    """
    while True:
        clear_terminal()

        page_name = "Lobby"

        console.print(
            Padding(
                Panel(
                    "1. Spellen\n"
                    "2. Saldo\n"
                    "3. Profiel\n\n"
                    "0. Casino verlaten",
                    title=f"[bold bright_yellow]{CASINO_NAME}[/] [bold bright_white]- {page_name}[/]",
                    border_style="bright_yellow",
                    padding=(1, 2),
                ),
                (1, 5))
        )

        menu_choice = get_menu_choice(range(0, 4))

        if menu_choice == 1:
            if current_user["playing_balance"] <= 0:
                print()
                print_message("U heeft onvoldoende saldo om te spelen.", RED)
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
    show_welcome_page()
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
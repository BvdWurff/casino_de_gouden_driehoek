# ==============================
# FUNCTION IMPORTS
# ==============================

from rich.console import Console
from rich.padding import Padding

from utils.balance_utils import (
    manage_balance,
)
from utils.utils import (
    format_currency,
    get_menu_choice,
    print_message,
    get_input,
    display_page,
    display_panel,
    display_menu_table,
)


# ==============================
# CONSTANTS
# ==============================

from utils.constants import (
    CONTINUE_PROMPT,
    INVALID_INPUT,
)


# ==============================
# CONFIGURATION
# ==============================

console = Console(width=80)


# ==============================
# GAME INFORMATION
# ==============================

def show_game_instructions(game, game_instructions, payout_structure=""):
    """
    Displays the instructions for the selected game.

    Args:
        game (str): The current game.
        game_instructions (str): The instructions for the selected game.
        payout_structure (str): The payout structure of the selected game.
    """
    display_page(location=game.capitalize(),
                 title="Speluitleg",
                 content=game_instructions
                 )

    if payout_structure:

        display_panel(payout_structure, title="Uitbetaling")

    get_input(CONTINUE_PROMPT)


# ==============================
# MENUS AND NAVIGATION
# ==============================

def get_game_action(game) -> str:
    """
    Displays the stop menu and determines how the player wants to continue.

    Args:
        game (str): The current game.

    Returns:
        str: The selected action.
    """
    content = "U heeft gekozen om het spel te stoppen. Wat wilt u doen?"

    display_page(location=game.capitalize(),
                 title="Spelopties",
                 content=content
                 )

    menu_options = ["Verder spelen", "Inzet aanpassen", "Ander spel kiezen", "", "Terug naar de lobby"]

    console.print(
        Padding(display_menu_table(menu_options, width=70), (0, 0, 1, 5))
    )

    menu_choice = get_menu_choice(range(0, 4))

    if menu_choice == 1:
        action = "continue"

    elif menu_choice == 2:
        action = "change_stake"

    elif menu_choice == 3:
        action = "choose_game"

    else:
        action = "main_menu"

    return action


def game_menu(current_user, game, game_instructions) -> str:
    """
    Displays the game menu and handles the selected menu option.

    Args:
        current_user (dict): The profile of the current user.
        game (str): The current game.
        game_instructions (str): The instructions for the selected game.

    Returns:
        str: The selected action.
    """
    action = "continue"

    while True:
        content = "U bevindt zich in het spelmenu."

        display_page(location=game.capitalize(),
                     title="Spelmenu",
                     content=content
                     )

        menu_options = ["Spel starten", "Spelinstructies", "", "Saldo-overzicht", "", "Stoppen"]

        console.print(
            Padding(display_menu_table(menu_options, width=70), (0, 0, 1, 5))
        )

        menu_choice = get_menu_choice(range(0, 4))

        if menu_choice == 2:
            show_game_instructions(game, game_instructions)
            continue

        if menu_choice == 3:
            manage_balance(current_user, trigger=game)
            continue

        if menu_choice == 0:
            action = get_game_action(game)

            if action == "continue":
                continue

        break

    return action


def get_round_action(current_user, stake, game) -> str:
    """
    Displays the round menu and determines how the player wants to continue.

    Args:
        current_user (dict): The profile of the current user.
        stake (int or float): The current stake.
        game (str): The current game.

    Returns:
        str: The selected action.
    """
    while True:
        page_content = f"""Huidig saldo:    {format_currency(current_user["playing_balance"])}
Huidige inzet:   {format_currency(stake)}"""

        display_page(location=game.capitalize(),
                     title="Ronde-overzicht",
                     content=page_content
                     )

        menu_options = ["Nieuwe ronde", "Inzet wijzigen", "", "Stoppen"]

        console.print(
            Padding(display_menu_table(menu_options, width=70), (0, 0, 1, 5))
        )

        menu_choice = get_menu_choice(range(0, 3))

        if menu_choice == 1:
            action = "continue"

        elif menu_choice == 2:
            action = "change_stake"

        else:
            action = get_game_action(game)

            if action == "continue":
                continue

        break

    return action


# ==============================
# STAKE AND BALANCE
# ==============================

def handle_insufficient_balance(current_user, game) -> str:
    """
    Handles a stake that exceeds the current playing balance.

    Args:
        current_user (dict): The profile of the current user.
        game (str): The current game.

    Returns:
        str: The selected action.
    """
    while True:
        print_message("Uw saldo is ontoereikend voor deze inzet.", "red")

        menu_options = ["Inzet wijzigen", "Saldo wijzigen", "", "Terug"]

        console.print(
            Padding(display_menu_table(menu_options, width=70), (1, 0, 1, 5))
        )

        menu_choice = get_menu_choice(range(0, 3))

        if menu_choice == 1:
            print()
            action = "change_stake"

        elif menu_choice == 2:
            manage_balance(current_user, trigger=game)
            action = "new_playing_balance"

        else:
            action = get_game_action(game)

            if action == "continue":
                continue

        break

    return action


def get_stake(current_user, stake, game, show_header=True) -> tuple[str, int | float]:
    """
    Requests and validates the player's stake.

    Args:
        current_user (dict): The profile of the current user.
        stake (int or float): The current stake.
        game (str): The current game.
        show_header (bool): Whether the stake screen header should be displayed.

    Returns:
        tuple: The action and updated stake.
    """
    while True:
        action = "continue"

        if show_header:
            content = f"""Uw huidige saldo bedraagt {format_currency(current_user["playing_balance"])}."""

            if stake > 0:
                content += f"\nUw huidige inzet bedraagt {format_currency(stake)}."

            display_page(location=game.capitalize(),
                         title="Inzet bepalen",
                         content=content
                         )

        while True:
            try:
                stake = round(float(get_input("Hoeveel wilt u inzetten? € ")), 2)
            except ValueError:
                print_message(INVALID_INPUT, "red")
                continue

            if stake <= 0:
                print()
                print_message("De inzet moet hoger zijn dan €0.", "red")
                print()
                continue

            if stake > current_user["playing_balance"]:
                action = handle_insufficient_balance(current_user, game)

                if action in ("continue", "change_stake"):
                    continue

                if action in ("choose_game", "main_menu"):
                    return action, stake

            if action == "new_playing_balance":
                break

            print()
            print_message(f"Uw inzet is geaccepteerd.", "green")
            print()
            get_input(CONTINUE_PROMPT)

            return "continue", stake


# ==============================
# OUTPUT
# ==============================

def show_game_results(current_user, game_result, game, payout, stake):
    """
    Displays the result of a completed game round.

    Args:
        current_user (dict): The profile of the current user.
        game_result (str): The result of the game round.
        game (str): The current game.
        payout (int or float): The amount paid out to the player.
        stake (int or float): The amount that was wagered.
    """
    content = ""

    if game_result == "won":
        content += f"""Gefeliciteerd, u heeft [bold green]gewonnen[/]!
Uw uitbetaling bedraagt {format_currency(payout)}"""

    elif game_result == "draw":
        content += f"""Het is [bold orange]gelijkspel[/].
U krijgt uw inzet van {format_currency(stake)} terug."""

    else:
        content += f"""Helaas, u heeft [bold red]verloren[/]."""

    display_page(location=game.capitalize(),
                 title="Speluitslag",
                 content=content
                 )

    get_input(CONTINUE_PROMPT)

    update_game_stats(current_user, game, "round_completed", game_result)


# ==============================
# GAME FLOW HELPERS
# ==============================

def prepare_game(current_user, game, game_instructions, payout_structure="") -> tuple[str, int | float]:
    """
    Prepares a game by showing its instructions, handling its menu and setting a stake.

    Args:
        current_user (dict): The profile of the current user.
        game (str): The current game.
        game_instructions (str): The instructions for the selected game.
        payout_structure (str): The payout structure for the selected game.

    Returns:
        tuple: The action and stake.
    """
    stake = 0.0

    show_game_instructions(game, game_instructions, payout_structure)

    while True:
        action = game_menu(current_user, game, game_instructions)

        if action in ("choose_game", "main_menu"):
            break

        if action == "change_stake":
            action, stake = get_stake(current_user, stake, game)

            if action in ("choose_game", "main_menu"):
                break

            continue

        if stake == 0:
            action, stake = get_stake(current_user, stake, game)

        break

    return action, stake


def resolve_insufficient_balance(current_user, stake, game) -> tuple[str, int | float]:
    """
    Resolves an insufficient balance and applies a requested stake change when needed.

    Args:
        current_user (dict): The profile of the current user.
        stake (int or float): The current stake.
        game (str): The current game.

    Returns:
        tuple: The action and updated stake.
    """
    action = handle_insufficient_balance(current_user, game)

    if action == "change_stake":
        action, stake = get_stake(current_user, stake, game)

    return action, stake


def handle_round_setup(current_user, stake, action, game):
    """
    Handles the shared setup flow before starting a new game round.

    Processes navigation, stake changes and insufficient balance
    before allowing the next round to start.

    Args:
        current_user (dict): The profile of the current user.
        stake (int or float): The current stake.
        action (str): The current game action.
        game (str): The current game.

    Returns:
        tuple: The action and updated stake.
    """
    while True:
        if action in ("choose_game", "main_menu"):
            break

        if action == "change_stake":
            action, stake = get_stake(current_user, stake, game, show_header=False)

            if action in ("choose_game", "main_menu"):
                break

            action = get_round_action(current_user, stake, game)
            continue

        if current_user["playing_balance"] < stake:
            action, stake = resolve_insufficient_balance(current_user, stake, game)

            if action in ("choose_game", "main_menu"):
                break

            action = get_round_action(current_user, stake, game)

            # Any balance or stake change must be confirmed before starting the round.
            continue

        break

    return action, stake


# ==============================
# GAME STATISTICS
# ==============================

def update_game_stats(current_user, game, trigger, game_result=""):
    """
    Updates the stored statistics for a game.

    Args:
        current_user (dict): The profile of the current user.
        game (str): The current game.
        trigger (str): Indicates which statistic should be updated.
        game_result (str): The result of the completed round.
    """

    if trigger == "game_started":
        if game not in current_user["played_games"]:
            current_user["played_games"][game] = {
                "games_played":1,
                "rounds_played":0,
                "results":{"won":0,
                           "lost":0,
                           "draw":0
                           }
            }

        else:
            current_user["played_games"][game]["games_played"] += 1

    if trigger == "round_completed":
        current_user["played_games"][game]["results"][game_result] += 1


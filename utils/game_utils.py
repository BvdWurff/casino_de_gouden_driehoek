# ==============================
# FUNCTION IMPORTS
# ==============================

from utils.balance_utils import (
    manage_balance,
)
from utils.utils import (
    blank_lines,
    clear_terminal,
    format_currency,
    get_menu_choice,
)


# ==============================
# CONSTANTS
# ==============================

from utils.constants import (
    CONTINUE_PROMPT,
    GREEN,
    INVALID_INPUT,
    ORANGE,
    RED,
    RESET,
    SEPARATOR,
)


# ==============================
# GAME INFORMATION
# ==============================

def show_game_instructions(trigger, game_instructions):
    """
    Displays the instructions for the selected game.

    Args:
        trigger (str): The current game.
        game_instructions (str): The instructions for the selected game.
    """
    clear_terminal()

    print(f"""
{trigger.capitalize()} - Speluitleg
{SEPARATOR}
Welkom bij de {trigger}.

{game_instructions}
{SEPARATOR}
""")

    input(CONTINUE_PROMPT)


# ==============================
# MENUS AND NAVIGATION
# ==============================

def get_game_action(trigger) -> str:
    """
    Displays the stop menu and determines how the player wants to continue.

    Args:
        trigger (str): The current game.

    Returns:
        str: The selected action.
    """
    clear_terminal()

    print(f"""
{trigger.capitalize()} - Spelopties
{SEPARATOR}
U heeft gekozen om het spel te stoppen.
Wat wilt u doen?

1. Verder spelen
2. Inzet aanpassen
3. Ander spel kiezen
0. Terug naar de lobby
{SEPARATOR}""")

    menu_choice = get_menu_choice(range(0, 4))

    if menu_choice == 1:
        blank_lines(2)
        action = "continue"

    elif menu_choice == 2:
        blank_lines(2)
        action = "change_stake"

    elif menu_choice == 3:
        blank_lines(2)
        action = "choose_game"

    else:
        blank_lines(2)
        action = "main_menu"

    return action


def game_menu(current_user, trigger, game_instructions) -> str:
    """
    Displays the game menu and handles the selected menu option.

    Args:
        current_user (dict): The profile of the current user.
        trigger (str): The current game.
        game_instructions (str): The instructions for the selected game.

    Returns:
        str: The selected action.
    """
    action = "continue"

    while True:
        clear_terminal()

        print(f"""
{trigger.capitalize()} - Spelmenu
{SEPARATOR}
1. Spel starten
2. Spelinstructies
3. Saldo-overzicht
0. Stoppen
{SEPARATOR}""")

        menu_choice = get_menu_choice(range(0, 4))

        blank_lines(2)

        if menu_choice == 2:
            show_game_instructions(trigger, game_instructions)
            continue

        if menu_choice == 3:
            current_user["playing_balance"], _ = manage_balance(current_user["playing_balance"], trigger=trigger)
            continue

        if menu_choice == 0:
            action = get_game_action(trigger)

            if action == "continue":
                continue

        break

    return action


def get_round_action(current_user, stake, trigger) -> str:
    """
    Displays the round menu and determines how the player wants to continue.

    Args:
        current_user (dict): The profile of the current user.
        stake (int or float): The current stake.
        trigger (str): The current game.

    Returns:
        str: The selected action.
    """
    while True:
        clear_terminal()

        print(f"""
{trigger.capitalize()} - Ronde-overzicht
{SEPARATOR}
Huidig saldo:    {format_currency(current_user["playing_balance"])}
Huidige inzet:   {format_currency(stake)}

1. Nieuwe ronde
2. Inzet wijzigen
0. Stoppen
{SEPARATOR}""")

        menu_choice = get_menu_choice(range(0, 3))

        if menu_choice == 1:
            action = "continue"

        elif menu_choice == 2:
            print()
            action = "change_stake"

        else:
            action = get_game_action(trigger)

            if action == "continue":
                continue

        break

    return action


# ==============================
# STAKE AND BALANCE
# ==============================

def handle_insufficient_balance(current_user, trigger) -> str:
    """
    Handles a stake that exceeds the current playing balance.

    Args:
        current_user (dict): The profile of the current user.
        trigger (str): The current game.

    Returns:
        str: The selected action.
    """
    while True:
        print(f"""Uw saldo is ontoereikend voor deze inzet.
{SEPARATOR}
1. Inzet wijzigen
2. Saldo wijzigen
0. Stoppen
{SEPARATOR}""")

        menu_choice = get_menu_choice(range(0, 3))

        if menu_choice == 1:
            print()
            action = "change_stake"

        elif menu_choice == 2:
            blank_lines(2)
            current_user["playing_balance"], _ = manage_balance(current_user["playing_balance"], trigger=trigger)
            action = "new_playing_balance"

        else:
            action = get_game_action(trigger)

            if action == "continue":
                continue

        break

    return action


def get_stake(current_user, stake, trigger, show_header=True) -> tuple[str, int | float]:
    """
    Requests and validates the player's stake.

    Args:
        current_user (dict): The profile of the current user.
        stake (int or float): The current stake.
        trigger (str): The current game.
        show_header (bool): Whether the stake screen header should be displayed.

    Returns:
        tuple: The action and updated stake.
    """
    while True:
        action = "continue"

        if show_header:
            clear_terminal()

            print(f"""
{trigger.capitalize()} - Inzet bepalen
{SEPARATOR}
Uw huidige saldo bedraagt {format_currency(current_user["playing_balance"])}.""")

            if stake > 0:
                print(f"Uw huidige inzet bedraagt {format_currency(stake)}.")

            print(SEPARATOR)

        while True:
            try:
                stake = round(float(input("Hoeveel wilt u inzetten? € ")), 2)
            except ValueError:
                print(INVALID_INPUT)
                continue

            if stake <= 0:
                print()
                print("De inzet moet hoger zijn dan €0.")
                print()
                continue

            if stake > current_user["playing_balance"]:
                blank_lines(2)
                action = handle_insufficient_balance(current_user, trigger)

                if action in ("continue", "change_stake"):
                    continue

                if action in ("choose_game", "main_menu"):
                    return action, stake

            if action == "new_playing_balance":
                break

            print()
            input(f"Uw inzet is geaccepteerd. {CONTINUE_PROMPT}")
            blank_lines(2)

            return "continue", stake


# ==============================
# OUTPUT
# ==============================

def show_game_results(current_user, game_result, game, payout, stake):
    """
    Displays the result of a completed game round.

    Args:
        current_user (dict): The profile of the user.
        game_result (str): The result of the game round.
        game (str): The current game.
        payout (int or float): The amount paid out to the player.
        stake (int or float): The amount that was wagered.
    """
    clear_terminal()

    print(f"""
{game.capitalize()} - Speluitslag
{SEPARATOR}""")

    if game_result == "won":
        print(f"""
Gefeliciteerd, u heeft {GREEN}gewonnen{RESET}!
Uw uitbetaling bedraagt {format_currency(payout)}.

{SEPARATOR}
""")

    elif game_result == "draw":
        print(f"""
Het is {ORANGE}gelijkspel{RESET}.
U krijgt uw inzet van {format_currency(stake)} terug.

{SEPARATOR}
""")

    else:
        print(f"""
Helaas, u heeft {RED}verloren{RESET}.

{SEPARATOR}
""")

    input(CONTINUE_PROMPT)

    update_game_stats(current_user, game, "round_completed", game_result)


# ==============================
# GAME FLOW HELPERS
# ==============================

def prepare_game(current_user, trigger, game_instructions) -> tuple[str, int | float]:
    """
    Prepares a game by showing its instructions, handling its menu and setting a stake.

    Args:
        current_user (dict): The profile of the current user.
        trigger (str): The current game.
        game_instructions (str): The instructions for the selected game.

    Returns:
        tuple: The action and stake.
    """
    stake = 0.0

    show_game_instructions(trigger, game_instructions)

    while True:
        action = game_menu(current_user, trigger, game_instructions)

        if action in ("choose_game", "main_menu"):
            break

        if action == "change_stake":
            action, stake = get_stake(current_user, stake, trigger)

            if action in ("choose_game", "main_menu"):
                break

            continue

        if stake == 0:
            action, stake = get_stake(current_user, stake, trigger)

        break

    return action, stake


def resolve_insufficient_balance(current_user, stake, trigger) -> tuple[str, int | float]:
    """
    Resolves an insufficient balance and applies a requested stake change when needed.

    Args:
        current_user (dict): The profile of the current user.
        stake (int or float): The current stake.
        trigger (str): The current game.

    Returns:
        tuple: The action and updated stake.
    """
    action = handle_insufficient_balance(current_user, trigger)

    if action == "change_stake":
        action, stake = get_stake(current_user, stake, trigger)

    return action, stake


def handle_round_setup(current_user, stake, action, trigger):
    """
    Handles the shared setup flow before starting a new game round.

    Processes navigation, stake changes and insufficient balance
    before allowing the next round to start.

    Args:
        current_user (dict): The profile of the current user.
        stake (int or float): The current stake.
        action (str): The current game action.
        trigger (str): The current game.

    Returns:
        tuple: The action and updated stake.
    """
    while True:
        if action in ("choose_game", "main_menu"):
            break

        if action == "change_stake":
            action, stake = get_stake(current_user, stake, trigger, show_header=False)

            if action in ("choose_game", "main_menu"):
                break

            action = get_round_action(current_user, stake, trigger)
            continue

        if current_user["playing_balance"] < stake:
            action, stake = resolve_insufficient_balance(current_user, stake, trigger)

            if action in ("choose_game", "main_menu"):
                break

            action = get_round_action(current_user, stake, trigger)

            # Any balance or stake change must be confirmed before starting the round.
            continue

        break

    return action, stake

def update_game_stats(current_user, game, trigger, game_result=""):

    if trigger is "game_started":
        if game not in current_user["played_games"]:
            current_user["played_games"][game] = {"games_played":1, "rounds_played":0, "results":{}}
        else:
            current_user["played_games"][game]["games_played"] +=1

    if trigger is "round_completed":
        if game_result not in current_user["played_games"][game]["results"]:
            current_user["played_games"][game]["results"][game_result] = 1
        else:
            current_user["played_games"][game]["results"][game_result] += 1
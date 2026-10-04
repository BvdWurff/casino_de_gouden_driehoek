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
    INVALID_INPUT,
    SEPARATOR,
    GREEN,
    RED,
    ORANGE,
    RESET,
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

def get_game_action(playing_balance, stake, trigger) -> tuple[str, int | float, int | float]:
    """
    Displays the stop menu and determines how the player wants to continue.

    Args:
        playing_balance (int or float): The current playing balance.
        stake (int or float): The current stake.
        trigger (str): The current game.

    Returns:
        tuple: The action, updated playing balance and stake.
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
0. Terug naar het hoofdmenu
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

    return action, playing_balance, stake


def game_menu(
    playing_balance,
    stake,
    trigger,
    game_instructions
) -> tuple[str, int | float, int | float]:
    """
    Displays the game menu and handles the selected menu option.

    Args:
        playing_balance (int or float): The current playing balance.
        stake (int or float): The current stake.
        trigger (str): The current game.
        game_instructions (str): The instructions for the selected game.

    Returns:
        tuple: The action, updated playing balance and stake.
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
            playing_balance, _ = manage_balance(playing_balance, trigger=trigger)
            continue

        if menu_choice == 0:
            action, playing_balance, stake = get_game_action(playing_balance, stake, trigger)

            if action == "continue":
                continue

        break

    return action, playing_balance, stake


def get_round_action(playing_balance, stake, trigger) -> tuple[str, int | float, int | float]:
    """
    Displays the round menu and determines how the player wants to continue.

    Args:
        playing_balance (int or float): The current playing balance.
        stake (int or float): The current stake.
        trigger (str): The current game.

    Returns:
        tuple: The action, updated playing balance and stake.
    """
    while True:
        clear_terminal()

        print(f"""
{trigger.capitalize()} - Ronde-overzicht
{SEPARATOR}
Huidig saldo:    {format_currency(playing_balance)}
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
            action, playing_balance, stake = get_game_action(playing_balance, stake, trigger)

            if action == "continue":
                continue

        break

    return action, playing_balance, stake


# ==============================
# STAKE AND BALANCE
# ==============================

def handle_insufficient_balance(
    playing_balance,
    stake,
    trigger
) -> tuple[str, int | float, int | float]:
    """
    Handles a stake that exceeds the current playing balance.

    Args:
        playing_balance (int or float): The current playing balance.
        stake (int or float): The current stake.
        trigger (str): The current game.

    Returns:
        tuple: The action, updated playing balance and stake.
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
            playing_balance, _ = manage_balance(playing_balance, trigger=trigger)
            action = "new_playing_balance"

        else:
            action, playing_balance, stake = get_game_action(playing_balance, stake, trigger)

            if action == "continue":
                continue

        break

    return action, playing_balance, stake


def get_stake(
    playing_balance,
    stake,
    trigger,
    show_header=True
) -> tuple[str, int | float, int | float]:
    """
    Requests and validates the player's stake.

    Args:
        playing_balance (int or float): The current playing balance.
        stake (int or float): The current stake.
        trigger (str): The current game.
        show_header (bool): Whether the stake screen header should be displayed.

    Returns:
        tuple: The action, updated playing balance and stake.
    """
    while True:
        action = "continue"

        if show_header:
            clear_terminal()

            print(f"""
{trigger.capitalize()} - Inzet bepalen
{SEPARATOR}
Uw huidige saldo bedraagt {format_currency(playing_balance)}.""")

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

            if stake > playing_balance:
                blank_lines(2)
                action, playing_balance, stake = handle_insufficient_balance(playing_balance, stake, trigger)

                if action in ("continue", "change_stake"):
                    continue

                if action in ("choose_game", "main_menu"):
                    return action, playing_balance, stake

            if action == "new_playing_balance":
                break

            print()
            input(f"Uw inzet is geaccepteerd. {CONTINUE_PROMPT}")
            blank_lines(2)

            return "continue", playing_balance, stake

def show_game_results(game_result, trigger, payout, stake):
    """
    Displays the result of a completed game round.

    Args:
        game_result (str): The result of the game round.
        trigger (str): The current game.
        payout (int or float): The amount paid out to the player.
        stake (int or float): The amount that was wagered.
    """
    clear_terminal()

    print(f"""
{trigger.capitalize()} - Speluitslag
{SEPARATOR}""")

    if game_result == "win":
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


# ==============================
# GAME FLOW HELPERS
# ==============================

def prepare_game(
    playing_balance,
    trigger,
    game_instructions
) -> tuple[str, int | float, int | float]:
    """
    Prepares a game by showing its instructions, handling its menu and setting a stake.

    Args:
        playing_balance (int or float): The current playing balance.
        trigger (str): The current game.
        game_instructions (str): The instructions for the selected game.

    Returns:
        tuple: The action, updated playing balance and stake.
    """
    stake = 0.0

    show_game_instructions(trigger, game_instructions)

    while True:
        action, playing_balance, stake = game_menu(
            playing_balance,
            stake,
            trigger,
            game_instructions
        )

        if action in ("choose_game", "main_menu"):
            break

        if action == "change_stake":
            action, playing_balance, stake = get_stake(playing_balance, stake, trigger)

            if action in ("choose_game", "main_menu"):
                break

            continue

        if stake == 0:
            action, playing_balance, stake = get_stake(playing_balance, stake, trigger)

        break

    return action, playing_balance, stake


def resolve_insufficient_balance(
    playing_balance,
    stake,
    trigger
) -> tuple[str, int | float, int | float]:
    """
    Resolves an insufficient balance and applies a requested stake change when needed.

    Args:
        playing_balance (int or float): The current playing balance.
        stake (int or float): The current stake.
        trigger (str): The current game.

    Returns:
        tuple: The action, updated playing balance and stake.
    """
    action, playing_balance, stake = handle_insufficient_balance(playing_balance, stake, trigger)

    if action == "change_stake":
        action, playing_balance, stake = get_stake(playing_balance, stake, trigger)

    return action, playing_balance, stake


def handle_round_setup(playing_balance, stake, action, trigger):
    """
        Handles the shared setup flow before starting a new game round.

        Processes navigation, stake changes and insufficient balance
        before allowing the next round to start.

        Args:
            playing_balance (int or float): The current playing balance.
            stake (int or float): The current stake.
            action (str): The current game action.
            trigger (str): The current game.

        Returns:
            tuple: The action, updated playing balance and stake.
        """
    while True:
        if action in ("choose_game", "main_menu"):
            break

        if action == "change_stake":
            action, playing_balance, stake = get_stake(
                playing_balance,
                stake,
                trigger,
                show_header=False
            )

            if action in ("choose_game", "main_menu"):
                break

            action, playing_balance, stake = get_round_action(playing_balance, stake, trigger)
            continue

        if playing_balance < stake:
            action, playing_balance, stake = resolve_insufficient_balance(playing_balance, stake, trigger)

            if action in ("choose_game", "main_menu"):
                break

            action, playing_balance, stake = get_round_action(playing_balance, stake, trigger)

            # Any balance or stake change must be confirmed before starting the round.
            continue

        break

    return action, playing_balance, stake

# ==============================
# FUNCTION IMPORTS
# ==============================

from games import (
    roulette,
    slot_machine,
    blackjack,
)
from utils.utils import (
    blank_lines,
    clear_terminal,
    get_menu_choice,
)


# ==============================
# CONSTANTS
# ==============================

from utils.constants import (
    CASINO_NAME,
    SEPARATOR,
)


# ==============================
# AVAILABLE GAMES
# ==============================

AVAILABLE_GAMES = {
    1: ("Roulette", roulette),
    2: ("Fruitmachine", slot_machine),
    3: ("Blackjack", blackjack),
}


# ==============================
# PROGRAM FLOW
# ==============================

def choose_game(playing_balance) -> int | float:
    """
    Displays the available games and handles game selection.

    Args:
        playing_balance (int or float): The current playing balance.

    Returns:
        int or float: The updated playing balance when returning to the main menu.
    """
    while True:
        clear_terminal()

        print(f"""
{CASINO_NAME} - Spellen
{SEPARATOR}""")

        for game_number, (game_name, _) in AVAILABLE_GAMES.items():
            print(f"{game_number}. {game_name}")

        print(f"""
0. Terug naar hoofdmenu
{SEPARATOR}""")

        menu_choice = get_menu_choice(range(0, len(AVAILABLE_GAMES) + 1))
        blank_lines(2)

        if menu_choice == 0:
            break

        _, game_module = AVAILABLE_GAMES[menu_choice]
        playing_balance, action = game_module.play(playing_balance)

        if action == "main_menu":
            blank_lines(2)
            break

    return playing_balance

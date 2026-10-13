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
    get_menu_choice,
    display_page,
)


# ==============================
# CONSTANTS
# ==============================

from utils.constants import (
    CASINO_NAME,
)


# ==============================
# CONFIGURATION
# ==============================

AVAILABLE_GAMES = {
    1: ("Roulette", roulette),
    2: ("Fruitmachine", slot_machine),
    3: ("Blackjack", blackjack),
}

# ==============================
# PROGRAM FLOW
# ==============================

def choose_game(current_user):
    """
    Displays the available games, starts the selected game and handles navigation.

    Args:
        current_user (dict): The profile of the current user.
    """
    while True:
        menu = []

        for game_number, (game_name, _) in AVAILABLE_GAMES.items():
            menu.append(f"{game_number}. {game_name}")

        menu.append("")
        menu.append("0. Terug naar hoofdmenu")

        menu = "\n".join(menu)

        display_page(location=CASINO_NAME,
                     title="Spellen",
                     content=menu
                     )

        menu_choice = get_menu_choice(range(0, len(AVAILABLE_GAMES) + 1))
        blank_lines(2)

        if menu_choice == 0:
            break

        _, game_module = AVAILABLE_GAMES[menu_choice]
        action = game_module.play(current_user)

        if action == "main_menu":
            blank_lines(2)
            break

        # The "choose_game" action naturally returns to this selection menu.
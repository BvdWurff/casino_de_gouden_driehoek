# ==============================
# FUNCTION IMPORTS
# ==============================

from rich.console import Console
from rich.padding import Padding

from games import (
    roulette,
    slot_machine,
    blackjack,
)
from utils.utils import (
    get_menu_choice,
    display_page,
    display_menu_table,
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

console = Console(width=80)

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
        content = "U vindt hier u een overzicht van de beschikbare spellen."

        display_page(location=CASINO_NAME,
                     title="Spellen",
                     content=content
                     )

        menu_options = []

        for game_number, (game_name, _) in AVAILABLE_GAMES.items():
            menu_options.append(f"{game_number}. {game_name}")

        menu_options.append("")
        menu_options.append("0. Terug")

        console.print(
            Padding(display_menu_table(menu_options, width=70), (0, 0, 1, 5))
        )

        menu_choice = get_menu_choice(range(0, len(AVAILABLE_GAMES) + 1))

        if menu_choice == 0:
            break

        _, game_module = AVAILABLE_GAMES[menu_choice]
        action = game_module.play(current_user)

        if action == "main_menu":
            break

        # The "choose_game" action naturally returns to this selection menu.
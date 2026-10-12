# ==============================
# FUNCTION IMPORTS
# ==============================

from rich.console import Console
from rich.padding import Padding
from rich.panel import Panel
from rich.live import Live
from rich.spinner import Spinner
from rich.console import Group

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
# CONFIGURATION
# ==============================

AVAILABLE_GAMES = {
    1: ("Roulette", roulette),
    2: ("Fruitmachine", slot_machine),
    3: ("Blackjack", blackjack),
}

console = Console(width=100)


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
        clear_terminal()

        page_name = "Spellen"

        menu = []

        for game_number, (game_name, _) in AVAILABLE_GAMES.items():
            menu.append(f"{game_number}. {game_name}")

        menu.append("")
        menu.append("0. Terug naar hoofdmenu")

        menu = "\n".join(menu)

        console.print(
            Padding(
                Panel(
                    f"{menu}",
                    title=f"[bold bright_yellow]{CASINO_NAME}[/] [bold bright_white]- {page_name}[/]",
                    border_style="bright_yellow",
                    padding=(1, 2),
                ),
                (1, 5))
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
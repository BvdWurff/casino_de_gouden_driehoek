from games import roulette, dobbelen, fruitmachine
from utils import blank_lines
from utils import clear_terminal


# ==============================
# CONFIGURATION
# ==============================

SEPARATOR = "-" * 50
CASINO_NAME = "Casino de Gouden Driehoek"
INVALID_INPUT = "\nOngeldige invoer. Probeer het opnieuw.\n"


# ==============================
# AVAILABLE GAMES
# ==============================

AVAILABLE_GAMES = {
    1: ("Roulette", roulette),
    2: ("Dobbelen", dobbelen),
    3: ("Fruitmachine", fruitmachine),
}


# ==============================
# PROGRAM FLOW
# ==============================

def choose_game(playing_balance):
    """
    Displays the available games and handles game selection.

    Args:
        playing_balance (int or float): The current playing balance.

    Returns:
        int or float: The updated playing balance.
    """
    while True:
        clear_terminal()

        print(f"""
{CASINO_NAME} - Spellen
{SEPARATOR}""")

        for game_number, game in AVAILABLE_GAMES.items():
            print(f"{game_number}. {game[0]}")

        print(f"""
0. Terug naar hoofdmenu
{SEPARATOR}""")

        try:
            menu_choice = int(input("Kies een optie: "))
        except ValueError:
            print(INVALID_INPUT)
            continue

        if menu_choice not in range(0, len(AVAILABLE_GAMES) + 1):
            print(INVALID_INPUT)
            continue

        blank_lines(2)

        if menu_choice == 0:
            return playing_balance

        _, game_module = AVAILABLE_GAMES[menu_choice]
        playing_balance, action = game_module.play(playing_balance)

        if action == "main_menu":
            blank_lines(2)

            return playing_balance
# ==============================
# FUNCTION IMPORTS
# ==============================

import random
import time

from utils.game_utils import (
    get_round_action,
    handle_round_setup,
    prepare_game,
    show_game_results,
    update_game_stats,
)
from utils.utils import (
    clear_terminal,
)


# ==============================
# CONSTANTS
# ==============================

from utils.constants import (
    JACKPOT_SYMBOL,
    MATCH_MULTIPLIERS,
    SEPARATOR,
    SYMBOL_MULTIPLIERS,
)


# ==============================
# CONFIGURATION
# ==============================

NAME_GAME = "fruitmachine"

GAME_INSTRUCTIONS = f"""Het doel van de fruitmachine is om zoveel mogelijk gelijke symbolen te draaien.
Bepaal uw inzet en haal daarna de hendel over.
De drie rollen draaien onafhankelijk van elkaar en komen ieder op één symbool tot stilstand.
Hoe meer gelijke symbolen u draait, hoe hoger uw uitbetaling.

Uitbetaling:
{SEPARATOR}
🍒 🍒       = 1,5x inzet
🍒 🍒 🍒    = 3x inzet

🔔 🔔       = 2x inzet
🔔 🔔 🔔    = 5x inzet

💎 💎       = 3x inzet
💎 💎 💎    = 9x inzet - JACKPOT!"""


# ==============================
# SLOT MACHINE GAME LOGIC
# ==============================

def process_spin_result(current_user, stake, spin_results, game):
    """
    Processes the slot machine result, calculates the payout and updates the playing balance.

    Args:
        current_user (dict): The profile of the current user.
        stake (int or float): The amount that was wagered.
        spin_results (list): The symbols generated for the three reels.
        game (str): The current game.
    """
    symbol_counts = {}

    for key in SYMBOL_MULTIPLIERS:
        symbol_counts[key] = 0

    for result in spin_results:
        symbol_counts[result] = symbol_counts.get(result, 0) + 1

    matching_symbol = ""
    match_count = 0

    for symbol, count in symbol_counts.items():
        if count > match_count:
            matching_symbol = symbol
            match_count = count

    if match_count == 1:
        game_result = "lost"
        payout = 0

    else:
        symbol_multiplier = SYMBOL_MULTIPLIERS[matching_symbol]

        if match_count == 3 and matching_symbol == JACKPOT_SYMBOL:
            match_multiplier = MATCH_MULTIPLIERS["jackpot"]
        else:
            match_multiplier = MATCH_MULTIPLIERS[match_count]

        payout = round(stake * symbol_multiplier * match_multiplier + stake, 2)
        current_user["playing_balance"] = round(current_user["playing_balance"] + payout, 2)

        game_result = "won"

    show_game_results(current_user, game_result, game, payout, stake)


# ==============================
# OUTPUT
# ==============================

def get_symbol(symbol):
    """
    Converts an internal slot machine symbol to its display symbol.

    Args:
        symbol (str): The internal symbol name.

    Returns:
    str: The display symbol for the slot machine.
    """
    match symbol:
        case "cherry":
            return "🍒"
        case "bell":
            return "🔔"
        case "diamond":
            return "💎"
        case _:
            return symbol


def show_spin_results(spin_results, game):
    """
    Displays the slot machine spin and its results.

    Args:
        spin_results (list): The symbols generated for the three reels.
        game (str): The current game.
    """
    clear_terminal()

    symbol_1 = get_symbol(spin_results[0])
    symbol_2 = get_symbol(spin_results[1])
    symbol_3 = get_symbol(spin_results[2])

    print(f"""
{game.capitalize()} - Speelronde
{SEPARATOR}""")

    input("Druk op Enter om de hendel over te halen.")

    print("""
De rollen beginnen te draaien. Veel geluk!
""")

    time.sleep(1)
    print("...")
    time.sleep(1)
    print("...")
    time.sleep(1)
    print("...")
    time.sleep(1)

    print()
    print(f"[ {symbol_1} ]", end="")
    time.sleep(1)
    print(f"[ {symbol_2} ]", end="")
    time.sleep(1)
    print(f"[ {symbol_3} ]")
    print()
    print(SEPARATOR)
    print()
    time.sleep(1)


# ==============================
# PROGRAM FLOW
# ==============================

def play(current_user) -> str:
    """
    Controls the slot machine game flow.

    Args:
        current_user (dict): The profile of the current user.

    Returns:
        str: The action to perform.
    """
    game = NAME_GAME
    action, stake = prepare_game(current_user, game, GAME_INSTRUCTIONS)

    if action in ("choose_game", "main_menu"):
        return action

    update_game_stats(current_user, game, "game_started")

    # Continue playing slot machine rounds until another destination is selected.
    while True:
        action, stake = handle_round_setup(current_user, stake, action, game)

        if action in ("choose_game", "main_menu"):
            break

        current_user["played_games"][game]["rounds_played"] += 1
        current_user["playing_balance"] = round(current_user["playing_balance"] - stake, 2)
        spin_results = random.choices(list(SYMBOL_MULTIPLIERS), k=3)

        show_spin_results(spin_results, game)
        process_spin_result(current_user, stake, spin_results, game)
        action = get_round_action(current_user, stake, game)

    return action
# ==============================
# FUNCTION IMPORTS
# ==============================

import random
import time

from utils.game_utils import (
    game_menu,
    get_round_action,
    get_stake,
    handle_insufficient_balance,
    show_game_instructions,
)
from utils.utils import (
    blank_lines,
    clear_terminal,
    format_currency,
)


# ==============================
# CONSTANTS
# ==============================

from utils.constants import (
    CONTINUE,
    JACKPOT_SYMBOL,
    MATCH_MULTIPLIERS,
    SEPARATOR,
    SYMBOL_MULTIPLIERS,
)


# ==============================
# CONFIGURATION
# ==============================

TRIGGER = "fruitmachine"

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

def determine_win(
    playing_balance,
    stake,
    spin_results
):
    """
    Determines whether the spin has won and updates the playing balance.

    Args:
        playing_balance (int or float): The current playing balance.
        stake (int or float): The amount that was wagered.
        spin_results (list): The symbols generated for the three reels.

    Returns:
        int or float: The updated playing balance.
    """
    win = True
    symbol_counts = {}

    for key in SYMBOL_MULTIPLIERS:
        symbol_counts[key] = 0

    for result in spin_results:
        symbol_counts[result] = symbol_counts.get(result, 0) + 1

    matching_symbol = ""
    match_count = 0

    for key, value in symbol_counts.items():
        if value > match_count:
            matching_symbol = key
            match_count = value

    symbol_multiplier = SYMBOL_MULTIPLIERS[matching_symbol]

    if match_count == 1:
        win = False

    elif match_count == 3 and matching_symbol == JACKPOT_SYMBOL:
        match_multiplier = MATCH_MULTIPLIERS["jackpot"]

    else:
        match_multiplier = MATCH_MULTIPLIERS[match_count]

    if win:
        payout = round(
            stake * symbol_multiplier * match_multiplier + stake,
            2
        )
        playing_balance = round(playing_balance + payout, 2)

        print("Gefeliciteerd, u heeft gewonnen!")
        print(f"Uw uitbetaling bedraagt {format_currency(payout)}.")

    else:
        print("Helaas, u heeft verloren.")

    blank_lines(2)
    input(CONTINUE)

    return playing_balance


# ==============================
# OUTPUT
# ==============================

def get_symbol(symbol):
    """
    Converts an internal slot machine symbol to its display symbol.

    Args:
        symbol (str): The internal symbol name.

    Returns:
        str: The symbol displayed to the player.
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


def show_spin_results(spin_results):
    """
    Displays the slot machine spin and its results.

    Args:
        spin_results (list): The symbols generated for the three reels.
    """
    clear_terminal()

    symbol_1 = get_symbol(spin_results[0])
    symbol_2 = get_symbol(spin_results[1])
    symbol_3 = get_symbol(spin_results[2])

    print(f"""
{TRIGGER.capitalize()} - Speelronde
{SEPARATOR}""")

    input("Druk op Enter om de hendel over te halen.")
    blank_lines(2)

    print("De rollen beginnen te draaien. Veel geluk!")
    print()

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
    time.sleep(1)

    print()


# ==============================
# PROGRAM FLOW
# ==============================

def play(playing_balance):
    """
    Controls the slot machine game flow.

    Args:
        playing_balance (int or float): The current playing balance.

    Returns:
        tuple: The updated playing balance and the action to perform.
    """
    trigger = TRIGGER
    stake = 0.0

    show_game_instructions(
        trigger,
        GAME_INSTRUCTIONS
    )

    while True:
        action, playing_balance, stake = game_menu(
            playing_balance,
            stake,
            trigger,
            GAME_INSTRUCTIONS
        )

        if action in ("choose_game", "main_menu"):
            return playing_balance, action

        if action == "continue":
            break

    # Determine the initial stake.
    if stake == 0:
        while True:
            action, playing_balance, stake = get_stake(
                playing_balance,
                stake,
                trigger
            )

            if action in ("choose_game", "main_menu"):
                return playing_balance, action

            break

    # Continue playing slot machine rounds until another destination is selected.
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

            action, playing_balance, stake = get_round_action(
                playing_balance,
                stake,
                trigger
            )
            continue

        if playing_balance < stake:
            action, playing_balance, stake = handle_insufficient_balance(
                playing_balance,
                stake,
                trigger
            )

            if action in ("choose_game", "main_menu"):
                break

            if action == "change_stake":
                action, playing_balance, stake = get_stake(
                    playing_balance,
                    stake,
                    trigger
                )

                if action in ("choose_game", "main_menu"):
                    break

            action, playing_balance, stake = get_round_action(
                playing_balance,
                stake,
                trigger
            )

            # Any balance or stake change must be confirmed before spinning.
            continue

        playing_balance = round(playing_balance - stake, 2)
        spin_results = random.choices(
            list(SYMBOL_MULTIPLIERS),
            k=3
        )

        show_spin_results(spin_results)

        playing_balance = determine_win(
            playing_balance,
            stake,
            spin_results
        )

        action, playing_balance, stake = get_round_action(
            playing_balance,
            stake,
            trigger
        )

    return playing_balance, action
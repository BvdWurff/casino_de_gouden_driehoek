from utils.utils import blank_lines
from utils.utils import format_currency
from utils.utils import clear_terminal

from utils.game_utils import get_stake
from utils.game_utils import handle_insufficient_balance
from utils.game_utils import show_welcome_message
from utils.game_utils import game_menu
from utils.game_utils import get_round_action

from utils.constants import SEPARATOR

import random
import time

# ==============================
# CONFIGURATION
# ==============================

SYMBOL_MULTIPLIERS = {"cherry":1, "bell":2, "diamond":4}
JACKPOT_SYMBOL = "diamond"
MATCH_MULTIPLIERS = {2: 0.5, 3: 2, "jackpot": 2}

TRIGGER = "fruitmachine"

GAME_INSTRUCTIONS = """Het doel van de fruitmachine is om zoveel mogelijk gelijke symbolen te draaien.
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

def get_symbols(spin_result):
    match spin_result:
        case "cherry":
            return "🍒"
        case "bell":
            return "🔔"
        case "diamond":
            return "💎"
        case _:
            return spin_result

def show_spin_results(spin_result):
    clear_terminal()

    result_1 = get_symbols(spin_result[0])
    result_2 = get_symbols(spin_result[1])
    result_3 = get_symbols(spin_result[2])

    print(f"""
Fruitmachine - Speelronde
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
    print(f"[ {result_1} ]", end="" )
    time.sleep(1)
    print(f"[ {result_2} ]", end="")
    time.sleep(1)
    print(f"[ {result_3} ]", end="\n")
    time.sleep(1)
    print()


def determine_win(playing_balance, stake, spin_result):
    win = True
    symbols = {}

    for key in SYMBOL_MULTIPLIERS:
        symbols[key] = 0

    for result in spin_result:
        symbols[result] = symbols.get(result, 0) + 1

    symbol = ""
    match = 0
    for key, value in symbols.items():
        if value > match:
            symbol = key
            match = value

    symbol_multiplier = SYMBOL_MULTIPLIERS[symbol]

    if match == 1:
        win = False
    elif match == 3 and symbol == JACKPOT_SYMBOL:
        match_multiplier = MATCH_MULTIPLIERS["jackpot"]
    else:
        match_multiplier = MATCH_MULTIPLIERS[match]

    if win:
        winnings = stake * symbol_multiplier * match_multiplier + stake
        playing_balance += winnings

        print(f"U heeft {format_currency(winnings)} gewonnen, gefeliciteerd!")

    else:
        print("helaas, u heeft verloren.")

    blank_lines(2)
    input("Druk op Enter om verder te gaan.")

    return playing_balance


def play(playing_balance):
    trigger = TRIGGER
    stake = 0.0
    show_welcome_message(trigger, GAME_INSTRUCTIONS)

    while True:
        action, playing_balance, stake = game_menu(trigger, GAME_INSTRUCTIONS, playing_balance, stake)

        if action in ("choose_game", "main_menu"):
            return playing_balance, action

        if action == "change_stake":
            continue

        if action == "continue":
            break

    # Determine the initial stake and roulette bet.
    if stake == 0:
        while True:
            action, playing_balance, stake = get_stake(playing_balance, trigger, stake)

            if action in ("choose_game", "main_menu"):
                return playing_balance, action

            break

    # Continue playing slot machine rounds until another destination is selected.
    while True:
        if action in ("choose_game", "main_menu"):
            break

        if action == "change_stake":
            action, playing_balance, stake = get_stake(playing_balance, "get_round_action", stake)
            action, playing_balance, stake = get_round_action(playing_balance, stake, trigger)
            continue

            if action in ("choose_game", "main_menu"):
                break

        if playing_balance < stake:
            action, playing_balance, stake = handle_insufficient_balance(playing_balance, trigger, stake)

            if action in ("choose_game", "main_menu"):
                break

            if action == "change_stake":
                action, playing_balance, stake = get_stake(playing_balance, trigger, stake)

                if action in ("choose_game", "main_menu"):
                    break

            # Any balance or stake change must be confirmed before spinning.
            continue

        playing_balance = round(playing_balance - stake, 2)
        spin_result = random.choices(list(SYMBOL_MULTIPLIERS), k=3)
        show_spin_results(spin_result)
        playing_balance = determine_win(playing_balance, stake, spin_result)
        action, playing_balance, stake = get_round_action(playing_balance, stake, trigger)

    return playing_balance, action




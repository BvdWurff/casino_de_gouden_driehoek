from utils.utils import blank_lines
from utils.utils import format_currency
from utils.utils import clear_terminal

from utils.game_utils import get_stake
from utils.game_utils import handle_insufficient_balance
from utils.game_utils import get_game_action
from utils.game_utils import show_welcome_message
from utils.game_utils import game_menu

from utils.constants import SEPARATOR
from utils.constants import INVALID_INPUT

import random
import time

# ==============================
# CONFIGURATION
# ==============================

TRIGGER = "roulettetafel"

GAME_INSTRUCTIONS = """Het doel van roulette is om te voorspellen waar het balletje zal landen.
Kies waarop u wilt inzetten en bepaal vervolgens uw inzet.
Het balletje kan op een vakje met één van de getallen van 0 tot en met 36 landen.
Ieder vakje heeft ook zijn eigen kleur. Dit kan rood, zwart of groen zijn.
In het keuze-overzicht ziet u per optie hoeveel winst u kunt behalen."""


# ==============================
# MENUS AND USER INPUT
# ==============================


def select_number():
    """
    Requests and validates a roulette number between 0 and 36.

    Returns:
        int: The selected roulette number.
    """
    while True:
        try:
            selected_number = int(input("Op welk nummer wilt u inzetten? (0 t/m 36) "))
        except ValueError:
            print(INVALID_INPUT)
            continue

        if 0 <= selected_number <= 36:
            return selected_number

        print(INVALID_INPUT)


def get_bet_choice(trigger, playing_balance, stake):
    """
    Displays the available roulette bets and requests the player's choice.

    Returns:
        tuple: The selected bet, optional roulette number and action to perform.
    """
    while True:
        clear_terminal()

        print(f"""
{trigger.capitalize()} - Inzetmogelijkheden
{SEPARATOR}
1. Rood   - winst: 1x inzet
2. Zwart  - winst: 1x inzet
3. Groen  - winst: 35x inzet
4. Even   - winst: 1x inzet
5. Oneven - winst: 1x inzet
6. Nummer - winst: 35x inzet

0. Stoppen
{SEPARATOR}""")

        try:
            bet_choice = int(input("Kies een optie: "))
        except ValueError:
            print(INVALID_INPUT)
            continue

        if bet_choice not in range(0, 7):
            print(INVALID_INPUT)
            continue

        action = "continue"
        selected_number = None

        if bet_choice == 6:
            print()
            selected_number = select_number()

        elif bet_choice == 0:
            blank_lines(2)
            action, playing_balance, stake = get_game_action(trigger, playing_balance, stake)

            # The player still needs to select a valid bet when continuing.
            if action == "continue":
                continue

        blank_lines(2)

        return bet_choice, selected_number, action


def get_bet_choice_text(bet_choice):
    """
    Converts the internal roulette bet choice to its Dutch display text.

    Args:
        bet_choice (int): The selected roulette bet.

    Returns:
        str: The Dutch display text for the selected bet.
    """
    match bet_choice:
        case 1:
            choice_text = "Rood"

        case 2:
            choice_text = "Zwart"

        case 3:
            choice_text = "Groen"

        case 4:
            choice_text = "Even"

        case 5:
            choice_text = "Oneven"

        case 6:
            choice_text = "Nummer"

        case _:
            choice_text = "Onbekend"

    return choice_text


def confirm_bet(playing_balance, stake, selected_number, bet_choice, trigger):
    """
    Displays the current bet and allows the player to confirm or modify it.

    Args:
        playing_balance (int or float): The current playing balance.
        stake (int or float): The current stake.
        selected_number (int or None): The selected roulette number.
        bet_choice (int): The selected roulette bet.
        trigger (str): The current game.

    Returns:
        tuple: The action, stake, selected number, bet choice and playing balance.
    """
    while True:
        clear_terminal()

        choice_text = get_bet_choice_text(bet_choice)

        print(f"""{trigger.capitalize()} - Spelopties
{SEPARATOR}
Uw huidige inzet is:

Inzet:      {format_currency(stake)}
Keuze:      {choice_text}""")

        if bet_choice == 6:
            print(f"Nummer:     {selected_number}")

        print(SEPARATOR)

        print(f"""
Wat wilt u doen?
{SEPARATOR}
1. Spelen met huidige inzet
2. Keuze aanpassen
3. Inzet aanpassen
4. Keuze en inzet aanpassen

0. Stoppen
{SEPARATOR}""")

        try:
            confirmation_choice = int(input("Kies een optie: "))
        except ValueError:
            print(INVALID_INPUT)
            time.sleep(1)
            continue

        if confirmation_choice not in range(0, 5):
            print(INVALID_INPUT)
            time.sleep(1)
            continue

        if confirmation_choice == 0:
            blank_lines(2)
            action, playing_balance, stake = get_game_action(trigger, playing_balance, stake)

            if action == "continue":
                continue

            if action == "change_stake":
                action, playing_balance, stake = get_stake(playing_balance, trigger, stake)

                if action == "continue":
                    continue

            return action, stake, selected_number, bet_choice, playing_balance

        if confirmation_choice == 1:
            blank_lines(2)

            return "continue", stake, selected_number, bet_choice, playing_balance

        if confirmation_choice == 2:
            previous_bet_choice = bet_choice
            previous_selected_number = selected_number

            blank_lines(2)

            bet_choice, selected_number, action = get_bet_choice(trigger, playing_balance, stake)

            if action == "continue":
                continue

            if action == "change_stake":
                # Keep the previous bet when only the stake is changed.
                bet_choice = previous_bet_choice
                selected_number = previous_selected_number
                action, playing_balance, stake = get_stake(playing_balance, trigger, stake)

                if action == "continue":
                    continue

            return action, stake, selected_number, bet_choice, playing_balance

        if confirmation_choice == 3:
            print()

            action, playing_balance, stake = get_stake(playing_balance, trigger, stake)

            if action == "continue":
                continue

            return action, stake, selected_number, bet_choice, playing_balance

        previous_bet_choice = bet_choice
        previous_selected_number = selected_number

        selected_number = None
        blank_lines(2)

        action, playing_balance, stake = get_stake(playing_balance, trigger, stake)

        if action in ("choose_game", "main_menu"):
            return action, stake, selected_number, bet_choice, playing_balance

        bet_choice, selected_number, action = get_bet_choice(trigger, playing_balance, stake)

        if action == "continue":
            continue

        if action == "change_stake":
            # Keep the previous bet when no new valid bet has been selected.
            bet_choice = previous_bet_choice
            selected_number = previous_selected_number
            action, playing_balance, stake = get_stake(playing_balance, trigger, stake)

            if action == "continue":
                continue

        return action, stake, selected_number, bet_choice, playing_balance


# ==============================
# ROULETTE GAME LOGIC
# ==============================

def determine_color_and_parity(spin_result):
    """
    Determines the color and parity of a roulette result.

    Args:
        spin_result (int): The roulette number that was rolled.

    Returns:
        tuple: The color and parity of the roulette result.
    """
    if spin_result == 0:
        color = "groen"
        parity = ""

    elif spin_result <= 18:
        if spin_result % 2 == 0:
            color = "zwart"
            parity = "even"

        else:
            color = "rood"
            parity = "oneven"

    elif spin_result % 2 == 0:
        color = "rood"
        parity = "even"

    else:
        color = "zwart"
        parity = "oneven"

    return color, parity


def determine_win(playing_balance, bet_choice, color, parity, selected_number, spin_result, stake):
    """
    Determines whether the roulette bet has won and updates the playing balance.

    Args:
        playing_balance (int or float): The current playing balance.
        bet_choice (int): The selected roulette bet.
        color (str): The color of the roulette result.
        parity (str): The parity of the roulette result.
        selected_number (int or None): The selected roulette number.
        spin_result (int): The roulette number that was rolled.
        stake (int or float): The amount that was wagered.

    Returns:
        int or float: The updated playing balance.
    """
    print(SEPARATOR)
    win = False
    multiplier = 2

    if bet_choice == 1 and color == "rood":
        win = True

    elif bet_choice == 2 and color == "zwart":
        win = True

    elif bet_choice == 3 and color == "groen":
        win = True
        multiplier = 36

    elif bet_choice == 4 and parity == "even":
        win = True

    elif bet_choice == 5 and parity == "oneven":
        win = True

    elif bet_choice == 6 and selected_number == spin_result:
        win = True
        multiplier = 36

    if win:
        playing_balance += stake * multiplier
        playing_balance = round(playing_balance, 2)

        gain = stake * multiplier - stake
        gain = round(gain, 2)

        print(f"Gefeliciteerd, u wint {format_currency(gain)}!")

    else:
        print("Helaas, u verliest uw inzet.")

    print(f"Uw nieuwe saldo is {format_currency(playing_balance)}.")
    print()

    input("Druk op Enter om verder te gaan.")
    blank_lines(2)

    return playing_balance


# ==============================
# OUTPUT
# ==============================

def show_spin_result(spin_result, color):
    """
    Displays the roulette spin and its result.

    Args:
        spin_result (int): The roulette number that was rolled.
        color (str): The color of the roulette result.
    """
    clear_terminal()

    blank_lines(2)
    print("De croupier rolt het balletje. Veel geluk!")
    time.sleep(1)
    print("...")
    time.sleep(1)
    print("Rien ne va plus!")
    time.sleep(1)
    print("...")
    time.sleep(1)
    print(f"Het balletje is geland op {spin_result} {color}.")
    print()
    time.sleep(1)


# ==============================
# PROGRAM FLOW
# ==============================

def play(playing_balance):
    """
    Controls the roulette game flow.

    Args:
        playing_balance (int or float): The current playing balance.

    Returns:
        tuple: The updated playing balance and the action to perform.
    """
    trigger = TRIGGER
    stake = 0.0
    show_welcome_message(trigger, GAME_INSTRUCTIONS)

    while True:
        action, playing_balance, stake = game_menu(trigger, GAME_INSTRUCTIONS, playing_balance, stake)

        if action in ("choose_game", "main_menu"):
            return playing_balance, action

        if action == "continue":
            break

        continue

    # Determine the initial stake and roulette bet.
    while True:
        if stake == 0:
            action, playing_balance, stake = get_stake(playing_balance, trigger, stake)

            if action in ("choose_game", "main_menu"):
                return playing_balance, action

        bet_choice, selected_number, action = get_bet_choice(trigger, playing_balance, stake)

        if action == "change_stake":
            continue

        if action in ("choose_game", "main_menu"):
            return playing_balance, action

        break

    # Continue playing roulette rounds until another destination is selected.
    while True:
        action, stake, selected_number, bet_choice, playing_balance = confirm_bet(playing_balance, stake, selected_number, bet_choice, trigger)

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

        spin_result = random.randint(0, 36)
        color, parity = determine_color_and_parity(spin_result)

        show_spin_result(spin_result, color)

        playing_balance = determine_win(playing_balance, bet_choice, color, parity, selected_number, spin_result, stake)

    return playing_balance, action
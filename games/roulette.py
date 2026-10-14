# ==============================
# FUNCTION IMPORTS
# ==============================

import random
import time

from rich.console import Console
from rich.padding import Padding
from rich.table import Table
from rich import box
from rich.text import Text

from utils.game_utils import (
    get_game_action,
    get_stake,
    prepare_game,
    resolve_insufficient_balance,
    show_game_results,
    update_game_stats,
)

from utils.utils import (
    format_currency,
    get_menu_choice,
    print_message,
    get_input,
    display_page,
    display_menu_table,
)


# ==============================
# CONSTANTS
# ==============================

from utils.constants import (
    CONTINUE_PROMPT,
    INVALID_INPUT,
)


# ==============================
# CONFIGURATION
# ==============================

NAME_GAME = "roulettetafel"
MAX_RECENT_RESULTS = 10
console = Console(width=100)

GAME_INSTRUCTIONS = """Het doel van roulette is om te voorspellen waar het balletje zal landen.
Kies waarop u wilt inzetten en bepaal vervolgens uw inzet.
Het balletje kan op een vakje met een van de getallen van 0 tot en met 36 landen.
Ieder vakje heeft een kleur: rood, zwart of groen.

In het keuze-overzicht ziet u per optie hoeveel winst u kunt behalen."""


# ==============================
# STATE
# ==============================

roulette_history = []


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
            selected_number = int(get_input("Op welk nummer wilt u inzetten? (0 t/m 36) "))
        except ValueError:
            print_message(INVALID_INPUT, "red")
            continue

        if 0 <= selected_number <= 36:
            return selected_number

        print_message(INVALID_INPUT, "red")


def get_bet_choice(recent_results, game):
    """
    Displays the available roulette bets and requests the player's choice.

    Args:
        recent_results (list): The stored recent roulette results.
        game (str): The current game.

    Returns:
        tuple: The action, selected bet and optional roulette number.
    """
    while True:
        content = ""

        if recent_results:
            content += f"""Laatste resultaten:
{format_recent_results(recent_results)}

"""
        menu_options = {"Rood": 1, "Zwart": 1, "Groen": 35, "Even": 1, "Oneven": 1, "Nummer": 35, "": "", "Stoppen": ""}
        # content = display_menu_table(menu_options)

        table = Table(
            box=box.SQUARE,
            expand=True,
            header_style="bold bright_white",
            border_style="bright_yellow",
            padding=(0, 1),
            width=64
        )

        table.add_column("Optie", min_width=4)
        table.add_column("Actie")
        table.add_column("Uitbetaling")

        counter = 0

        for menu_option,payout in menu_options.items():
            counter += 1

            if menu_option == "":
                counter = -1

            table.add_row(
                Text(f"{str(counter)}.") if menu_option else Text(""),
                Text(str(menu_option)),
                Text(f"{str(payout)}x inzet") if payout else Text("")
            )

        display_page(location=game.capitalize(),
                     title="Inzetmogelijkheden",
                     content=table
                     )

        bet_choice = get_menu_choice(range(0, 7))
        action = "continue"
        selected_number = None

        if bet_choice == 6:
            selected_number = select_number()

        elif bet_choice == 0:
            action = get_game_action(game)

            # A valid bet still needs to be selected when the game is resumed.
            if action == "continue":
                continue

        return action, bet_choice, selected_number


def change_bet(
    current_user,
    stake,
    bet_choice,
    selected_number,
    recent_results,
    game
):
    """
    Changes the current roulette bet and handles a stake-change action when requested.

    Args:
        current_user (dict): The profile of the current user.
        stake (int or float): The current stake.
        bet_choice (int): The current roulette bet.
        selected_number (int or None): The current roulette number.
        recent_results (list): The stored recent roulette results.
        game (str): The current game.

    Returns:
        tuple: The action, stake, bet choice and selected roulette number.
    """
    previous_bet_choice = bet_choice
    previous_selected_number = selected_number

    action, bet_choice, selected_number = get_bet_choice(recent_results, game)

    if action == "change_stake":
        # Keep the previous bet when only the stake is changed.
        bet_choice = previous_bet_choice
        selected_number = previous_selected_number
        action, stake = get_stake(current_user, stake, game)

    return action, stake, bet_choice, selected_number


def confirm_bet(
    current_user,
    stake,
    bet_choice,
    selected_number,
    recent_results,
    game
):
    """
    Displays the current bet and allows the player to confirm or modify it.

    Args:
        current_user (dict): The profile of the current user.
        stake (int or float): The current stake.
        bet_choice (int): The selected roulette bet.
        selected_number (int or None): The selected roulette number.
        recent_results (list): The stored recent roulette results.
        game (str): The current game.

    Returns:
        tuple: The action, stake, bet choice and selected roulette number.
    """
    while True:
        bet_choice_text = get_bet_choice_text(bet_choice)

        page_content = f"""Huidige inzet:
Inzet:          {format_currency(stake)}
Keuze:          {bet_choice_text}"""

        if bet_choice == 6:
            page_content += f"\nNummer:         {selected_number}"

        page_content += f"""\n
Huidig saldo:   
{format_currency(current_user["playing_balance"])}"""

        if recent_results:
            page_content += f"""

Laatste resultaten:
{format_recent_results(recent_results)}"""

        display_page(location=game.capitalize(),
                     title="Spelopties",
                     content=page_content
                     )

        menu_options = ["Spelen met huidige inzet", "Keuze aanpassen", "Inzet aanpassen", "Keuze en inzet aanpassen", "", "Stoppen"]

        console.print(
            Padding(display_menu_table(menu_options, width=70), (0, 0, 1, 5))
        )

        menu_choice = get_menu_choice(range(0, 5))

        if menu_choice == 1:
            return "continue", stake, bet_choice, selected_number

        if menu_choice == 0:
            action = get_game_action(game)

            if action == "continue":
                continue

            if action in ("choose_game", "main_menu"):
                return action, stake, bet_choice, selected_number

            # The only remaining action is a stake change.
            menu_choice = 3

        if menu_choice == 2:
            action, stake, bet_choice, selected_number = change_bet(
                current_user,
                stake,
                bet_choice,
                selected_number,
                recent_results,
                game
            )

            if action == "continue":
                continue

            return action, stake, bet_choice, selected_number

        if menu_choice == 3:
            print()
            action, stake = get_stake(current_user, stake, game)

            if action == "continue":
                continue

            return action, stake, bet_choice, selected_number

        # Menu option 4 changes the stake first and then the roulette bet.
        action, stake = get_stake(current_user, stake, game)

        if action in ("choose_game", "main_menu"):
            return action, stake, bet_choice, selected_number

        action, stake, bet_choice, selected_number = change_bet(
            current_user,
            stake,
            bet_choice,
            selected_number,
            recent_results,
            game
        )

        if action == "continue":
            continue

        return action, stake, bet_choice, selected_number


# ==============================
# ROULETTE GAME LOGIC
# ==============================

def determine_color_and_parity(spin_result):
    """
    Determines the color and parity of a roulette result.

    Args:
        spin_result (int): The roulette number the ball landed on.

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


def process_spin_result(
    current_user,
    stake,
    bet_choice,
    selected_number,
    spin_result,
    color,
    parity,
    game
):
    """
    Processes the roulette result, payout and updated playing balance.

    Args:
        current_user (dict): The profile of the current user.
        stake (int or float): The amount that was wagered.
        bet_choice (int): The selected roulette bet.
        selected_number (int or None): The selected roulette number.
        spin_result (int): The roulette number the ball landed on.
        color (str): The color of the roulette result.
        parity (str): The parity of the roulette result.
        game (str): The current game.
    """
    payout_multiplier = 2
    payout = 0

    if bet_choice == 1 and color == "rood":
        game_result = "won"
    elif bet_choice == 2 and color == "zwart":
        game_result = "won"
    elif bet_choice == 3 and color == "groen":
        game_result = "won"
        payout_multiplier = 36
    elif bet_choice == 4 and parity == "even":
        game_result = "won"
    elif bet_choice == 5 and parity == "oneven":
        game_result = "won"
    elif bet_choice == 6 and selected_number == spin_result:
        game_result = "won"
        payout_multiplier = 36
    else:
        game_result = "lost"

    if game_result == "won":
        payout = round(stake * payout_multiplier, 2)
        current_user["playing_balance"] = round(current_user["playing_balance"] + payout, 2)

    show_game_results(current_user, game_result, game, payout, stake)


def add_recent_result(recent_results, spin_result, color):
    """
    Adds a roulette result to the recent-results history.

    Args:
        recent_results (list): The stored recent roulette results.
        spin_result (int): The roulette number the ball landed on.
        color (str): The color of the roulette result.
    """
    recent_results.append([spin_result, color])

    if len(recent_results) > MAX_RECENT_RESULTS:
        del recent_results[0]


# ==============================
# OUTPUT
# ==============================

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


def get_font_color(color):
    """
    Returns the console font color for a roulette color.

    Args:
        color (str): The roulette color.

    Returns:
        str: The corresponding ANSI console color.
    """
    font_color = ""

    match color:
        case "groen":
            font_color = "green"
        case "rood":
            font_color = "red"
        case "zwart":
            font_color = "black"

    return font_color


def format_recent_results(recent_results):
    """
    Formats the recent roulette results for display.

    Args:
        recent_results (list): The stored recent roulette results.

    Returns:
        str: The formatted recent roulette results.
    """
    formatted_results = ""

    for number, color in recent_results:
        font_color = get_font_color(color)
        formatted_results += f"[{font_color} on white] {number} [/]"

    return formatted_results


def show_spin_result(spin_result, color, game):
    """
    Displays the roulette spin and its result.

    Args:
        spin_result (int): The roulette number the ball landed on.
        color (str): The color of the roulette result.
        game (str): The current game.
    """
    font_color = get_font_color(color)
    content = "De croupier rolt het balletje. Veel geluk!"

    display_page(location=game.capitalize(),
                 title="Speelronde",
                 content=content
                 )

    time.sleep(1)
    print_message("[default]...[/]")
    time.sleep(1)
    print_message("Rien ne va plus!")
    time.sleep(1)
    print_message("[default]...[/]")
    time.sleep(1)

    print_message(
        f"Het balletje is geland op [{font_color} on white]{spin_result} {color.capitalize()}[/]."
    )
    print()
    get_input(CONTINUE_PROMPT)


# ==============================
# PROGRAM FLOW
# ==============================

def play(current_user) -> str:
    """
    Controls the roulette game flow.

    Args:
        current_user (dict): The profile of the current user.

    Returns:
        str: The action to perform.
    """
    game = NAME_GAME
    action, stake = prepare_game(current_user, game, GAME_INSTRUCTIONS)

    if action in ("choose_game", "main_menu"):
        return action

    while True:
        action, bet_choice, selected_number = get_bet_choice(roulette_history, game)

        if action == "change_stake":
            action, stake = get_stake(current_user, stake, game)

            if action in ("choose_game", "main_menu"):
                return action

            continue

        if action in ("choose_game", "main_menu"):
            return action

        break

    update_game_stats(current_user, game, "game_started")

    # Continue playing roulette rounds until another destination is selected.
    while True:
        action, stake, bet_choice, selected_number = confirm_bet(
            current_user,
            stake,
            bet_choice,
            selected_number,
            roulette_history,
            game
        )

        if action in ("choose_game", "main_menu"):
            break

        if current_user["playing_balance"] < stake:
            action, stake = resolve_insufficient_balance(current_user, stake, game)

            if action in ("choose_game", "main_menu"):
                break

            # Any balance or stake change must be confirmed before spinning.
            continue

        current_user["played_games"][game]["rounds_played"] += 1
        current_user["playing_balance"] = round(current_user["playing_balance"] - stake, 2)

        spin_result = random.randint(0, 36)
        color, parity = determine_color_and_parity(spin_result)

        add_recent_result(roulette_history, spin_result, color)
        show_spin_result(spin_result, color, game)

        process_spin_result(
            current_user,
            stake,
            bet_choice,
            selected_number,
            spin_result,
            color,
            parity,
            game
        )

    return action
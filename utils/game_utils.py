from main import manage_balance

from utils.utils import blank_lines
from utils.utils import format_currency
from utils.utils import clear_terminal

from utils.constants import SEPARATOR
from utils.constants import INVALID_INPUT
from utils.constants import CONTINUE
from utils.constants import CHOOSE_OPTION


def get_game_action(trigger, playing_balance, stake):
    """
    Displays the stop menu and determines how the player wants to continue.

    Returns:
        str: The action to perform after leaving the stop menu.
    """
    clear_terminal()

    print(f"""
{trigger.capitalize()} - Spelopties
{SEPARATOR}
U heeft gekozen om het spel te stoppen.
Wat wilt u doen?

1. Verder spelen
2. Inzet aanpassen
3. Ander spel kiezen
0. Terug naar het hoofdmenu
{SEPARATOR}""")

    while True:
        try:
            menu_choice = int(input(CHOOSE_OPTION))
        except ValueError:
            print(INVALID_INPUT)
            continue

        if menu_choice not in range(0, 4):
            print(INVALID_INPUT)
            continue

        if menu_choice == 1:
            blank_lines(2)
            action = "continue"

        elif menu_choice == 2:
            blank_lines(2)
            action, playing_balance, stake = get_stake(playing_balance, trigger, stake)
            action = "change_stake"

        elif menu_choice == 3:
            action = "choose_game"

        else:
            action = "main_menu"

        return action, playing_balance, stake


def handle_insufficient_balance(playing_balance, trigger, stake):
    """
    Handles a stake that exceeds the current playing balance.

    Args:
        playing_balance (int or float): The current playing balance.
        trigger (str): Game the function is triggered from.

    Returns:
        tuple: The updated playing balance and the action to perform.
    """
    while True:
        print(f"""Uw saldo is ontoereikend voor deze inzet.
{SEPARATOR}
1. Inzet wijzigen
2. Saldo wijzigen
0. Stoppen
{SEPARATOR}""")

        try:
            menu_choice = int(input(CHOOSE_OPTION))
        except ValueError:
            print(INVALID_INPUT)
            continue

        if not 0 <= menu_choice <= 2:
            print(INVALID_INPUT)
            continue

        if menu_choice == 1:
            print()
            action = "change_stake"

        elif menu_choice == 2:
            blank_lines(2)
            playing_balance, _ = manage_balance(playing_balance, trigger=trigger)
            action = "new_playing_balance"

        else:
            action, playing_balance, stake = get_game_action(trigger, playing_balance, stake)

        return action, playing_balance, stake


def get_stake(playing_balance, trigger, stake):
    """
    Requests and validates the player's stake.

    Args:
        playing_balance (int or float): The current playing balance.
        trigger (str): The game the function is triggered from.

    Returns:
        tuple: The stake, updated playing balance and action to perform.
    """
    while True:
        action = "continue"

        if trigger is not "get_round_action":
            clear_terminal()

            print(f"""
{trigger.capitalize()} - Inzet bepalen
{SEPARATOR}
Uw huidige saldo bedraagt {format_currency(playing_balance)}.
Uw huidige inzet bedraagt {format_currency(stake)}.
{SEPARATOR}""")

        while True:
            try:
                stake = float(input("Hoeveel wilt u inzetten? € "))
            except ValueError:
                print(INVALID_INPUT)
                continue

            if stake <= 0:
                print()
                print("De inzet moet hoger zijn dan €0.")
                print()
                continue

            if stake > playing_balance:
                blank_lines(2)
                action, playing_balance, stake = handle_insufficient_balance(playing_balance, trigger, stake)

                if action in ("continue", "change_stake"):
                    continue

                if action in ("choose_game", "main_menu"):
                    return action, playing_balance, stake

            if action == "new_playing_balance":
                break

            print()
            input(f"Uw inzet is geaccepteerd. {CONTINUE}")
            blank_lines(2)

            action = "continue"
            return action, playing_balance, stake


def show_welcome_message(trigger, game_instructions):
    """
    Displays the slot machine game instructions.
    """
    clear_terminal()

    print(f"""
{trigger.capitalize()} - Speluitleg
{SEPARATOR}
Welkom bij de {trigger}.

{game_instructions}
{SEPARATOR}
""")
    input(CONTINUE)


def game_menu(trigger, game_instructions, playing_balance, stake):
    while True:
        clear_terminal()

        print(f"""
{trigger.capitalize()} - Spelmenu
{SEPARATOR}
1. Spel starten
2. Spelinstructies
3. Saldo-overzicht
0. Stoppen
{SEPARATOR}""")
        try:
            menu_choice = int(input(CHOOSE_OPTION))
        except ValueError:
            print(INVALID_INPUT)
            print()
            input(CONTINUE)
            continue

        if menu_choice not in range(0, 4):
            print(INVALID_INPUT)
            input(CONTINUE)
            continue

        blank_lines(2)
        action = "continue"

        if menu_choice == 2:
            show_welcome_message(trigger, game_instructions)
            continue

        elif menu_choice == 3:
            playing_balance, action = manage_balance(playing_balance, trigger=trigger)
            continue

        elif menu_choice == 0:
            action, playing_balance, stake = get_game_action(trigger, playing_balance, stake)

            if action in ("continue", "change_stake"):
                continue

        return action, playing_balance, stake


def get_round_action(playing_balance, stake, trigger):
    while True:
        clear_terminal()
        print(f"""
{trigger.capitalize()} - Ronde-overzicht
{SEPARATOR}     
 Huidige saldo:    {format_currency(playing_balance)}
 Huidige inzet:    {format_currency(stake)}     

 1. Nieuwe ronde
 2. Inzet wijzigen
 0. Stoppen
 {SEPARATOR}""")
        try:
            menu_choice = int(input(CHOOSE_OPTION))
        except ValueError:
            print(INVALID_INPUT)
            input(CONTINUE)
            continue

        if not 0 <= menu_choice <= 2:
            print(INVALID_INPUT)
            input(CONTINUE)
            continue

        if menu_choice == 1:
            action = "continue"

        elif menu_choice == 2:
            blank_lines(2)
            action = "change_stake"

        else:
            action, playing_balance, stake = get_game_action(trigger, playing_balance, stake)
            continue

        return action, playing_balance, stake



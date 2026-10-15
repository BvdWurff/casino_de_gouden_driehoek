# ==============================
# FUNCTION IMPORTS
# ==============================

import random
import time

from rich.console import Console
from rich.padding import Padding

from utils.game_utils import (
    get_round_action,
    handle_round_setup,
    prepare_game,
    show_game_results,
    update_game_stats,
)
from utils.utils import (
    get_menu_choice,
    get_input,
    display_page,
    print_message,
    display_menu_table,
)


# ==============================
# CONSTANTS
# ==============================

from utils.constants import (
    BLACKJACK_MULTIPLIER,
    BLACKJACK_PUSH_MULTIPLIER,
    BLACKJACK_WIN_MULTIPLIER,
    CONTINUE_PROMPT,
    RANKS,
    SUITS,
)


# ==============================
# CONFIGURATION
# ==============================

console = Console(width=80)
NAME_GAME = "blackjack"
DECKS_IN_SHOE = 6

GAME_INSTRUCTIONS = f"""Het doel van blackjack is om met uw kaarten zo dicht mogelijk bij 21 punten te komen zonder daar overheen te gaan.
U speelt tegen de dealer.

De kaarten 2 tot en met 10 hebben hun eigen waarde.
Boer, vrouw en heer zijn 10 punten waard.
Een aas is 1 of 11 punten waard, afhankelijk van welke waarde het gunstigst is.

U begint met twee kaarten.
Tijdens uw beurt kunt u extra kaarten vragen of passen.
Komt u boven de 21 punten, dan verliest u direct.

Na uw beurt speelt de dealer verder.
Heeft u meer punten dan de dealer zonder boven de 21 uit te komen, dan wint u.
Heeft u 21 punten met uw eerste twee kaarten, dan heeft u blackjack.
Heeft u evenveel punten als de dealer, dan is het gelijkspel en krijgt u uw inzet terug."""

PAYOUT_STRUCTURE = """Blackjack                = 2,5x inzet
Gewonnen                 = 2x inzet
Gelijkspel               = 1x inzet"""


# ==============================
# CARD AND HAND LOGIC
# ==============================

def get_new_shoe():
    """
    Creates and shuffles a new blackjack shoe.

    Returns:
        tuple: The shuffled shoe and the number of cards remaining
        before the shoe should be replaced.
    """
    shoe = []

    for i in range(1, DECKS_IN_SHOE + 1):
        shoe += [f"{suit}{rank}" for suit in SUITS for rank in RANKS]

    random.shuffle(shoe)

    cards_until_shuffle = random.randint(
        int(len(shoe) * 0.70),
        int(len(shoe) * 0.90),
    )

    return shoe, cards_until_shuffle


def deal_cards(shoe, cards_until_shuffle: int):
    """
    Deals the initial two cards to the player and dealer.

    Args:
        shoe (list): The current blackjack shoe.
        cards_until_shuffle (int): The number of cards that can still be dealt before shuffling.

    Returns:
        tuple: The updated shoe, cards until shuffle, dealer hand
        and player hand.
    """
    player_hand = [shoe.pop(0)]
    dealer_hand = [shoe.pop(0)]

    player_hand.append(shoe.pop(0))
    dealer_hand.append(shoe.pop(0))

    cards_until_shuffle -= 4

    return shoe, cards_until_shuffle, dealer_hand, player_hand


def draw_card(shoe, cards_until_shuffle: int, playing_hand):
    """
    Draws one card from the shoe and adds it to the given hand.

    Args:
        shoe (list): The current blackjack shoe.
        cards_until_shuffle (int): The number of cards that can still be dealt before shuffling.
        playing_hand (list): The hand receiving the card.

    Returns:
        tuple: The updated shoe, cards until shuffle and playing hand.
    """
    playing_hand.append(shoe.pop(0))
    cards_until_shuffle -= 1

    return shoe, cards_until_shuffle, playing_hand


def calculate_hand_values(playing_hand, actor):
    """
    Calculates all relevant blackjack values for a hand.

    Args:
        playing_hand (list): The blackjack hand to evaluate.
        actor (str): The player or dealer whose hand is evaluated.

    Returns:
        tuple: The hand values, display text and resulting hand status.
    """
    hand_values = [0]

    for card in playing_hand:
        card_value = card[1:]

        if card_value in ("J", "Q", "K"):
            card_value = 10
            hand_values = [value + card_value for value in hand_values]

        elif card_value == "A":
            new_values = []

            for value in hand_values:
                new_values.append(value + 1)
                new_values.append(value + 11)

            hand_values = sorted(set(new_values))

        else:
            card_value = int(card_value)
            hand_values = [value + card_value for value in hand_values]

        if 21 in hand_values:
            hand_values = [21]

            if len(playing_hand) == 2:
                status = "blackjack"
            else:
                status = "stand"

            hand_values = str(hand_values)[1:-1]

            return hand_values, "handwaarde is:", status

    hand_values = [hand_values[0]] + [value for value in hand_values[1:] if value < 21]

    if len(hand_values) > 1:
        hand_values_text = "handwaardes zijn:"
        hand_value = hand_values[-1]

        if actor == "dealer" and hand_value >= 17:
            status = "stand"
        else:
            status = "hit"

    else:
        hand_values_text = "handwaarde is:"
        hand_value = hand_values[0]

        if hand_value > 21:
            status = "bust"
        elif actor == "dealer" and hand_value >= 17:
            status = "stand"
        else:
            status = "hit"

    hand_values = str(hand_values)[1:-1]

    return hand_values, hand_values_text, status


def determine_game_result(player_status, player_hand_value, dealer_status, dealer_hand_value):
    """
    Determines the result of a completed blackjack round.

    Args:
        player_status (str): The final status of the player's hand.
        player_hand_value (str): The final value of the player's hand.
        dealer_status (str): The final status of the dealer's hand.
        dealer_hand_value (str): The final value of the dealer's hand.

    Returns:
        str: The blackjack round result.
    """
    if player_status in ("bust", "dealer_blackjack"):
        return "lost"

    if "," in player_hand_value:
        player_hand_value = player_hand_value[-2:]

    player_hand_value = int(player_hand_value)

    if "," in dealer_hand_value:
        dealer_hand_value = dealer_hand_value[-2:]

    dealer_hand_value = int(dealer_hand_value)

    game_result = "lost"

    if player_status == "blackjack":
        if dealer_status == "blackjack":
            game_result = "push"
        else:
            game_result = "blackjack"

    elif player_status == "stand":
        if dealer_status == "bust":
            game_result = "won"

        elif dealer_status == "stand":
            if player_hand_value > dealer_hand_value:
                game_result = "won"
            elif player_hand_value == dealer_hand_value:
                game_result = "push"

    return game_result


def process_payout(current_user, game_result, stake, game):
    """
    Calculates the blackjack payout and updates the playing balance.

    Args:
        current_user (dict): The profile of the current user.
        game_result (str): The result of the blackjack round.
        stake (int or float): The amount that was wagered.
        game (str): The current game.
    """
    match game_result:
        case "blackjack":
            payout_multiplier = BLACKJACK_MULTIPLIER
        case "won":
            payout_multiplier = BLACKJACK_WIN_MULTIPLIER
        case "push":
            payout_multiplier = BLACKJACK_PUSH_MULTIPLIER
        case _:
            payout_multiplier = 0

    payout = round(stake * payout_multiplier, 2)
    current_user["playing_balance"] = round(current_user["playing_balance"] + payout, 2)

    if game_result in ("blackjack", "won"):
        display_result = "won"
    elif game_result == "push":
        display_result = "draw"
    else:
        display_result = "lost"

    show_game_results(current_user, display_result, game, payout, stake)


# ==============================
# OUTPUT
# ==============================

def format_hand(hand):
    """
    Formats a blackjack hand for terminal display.

    Args:
        hand (list): The cards to format.

    Returns:
        str: The formatted blackjack hand.
    """
    formatted_hand = ""

    for card in hand:
        suit = card[0]
        value = card[1:]

        if suit in ("♥", "♦"):
            suit_color = 'red'
        else:
            suit_color = 'black'

        formatted_hand += f"[{suit_color} on white]{suit}{value}[/] | "

    formatted_hand = formatted_hand[:-3]

    return formatted_hand


def prepare_play_hand(player_hand, dealer_hand, game, actor):
    """
    Calculates and displays the current blackjack hands and hand values.

    Args:
        player_hand (list): The player's current hand.
        dealer_hand (list): The dealer's current hand.
        game (str): The current game.
        actor (str): The player or dealer whose turn is active.

    Returns:
        tuple: Dealer hand values, dealer value text, dealer status,
        player hand values, player value text and player status.
    """
    dealer_hand_values, dealer_hand_values_text, dealer_status = calculate_hand_values(dealer_hand, "dealer")
    player_hand_values, player_hand_values_text, player_status = calculate_hand_values(player_hand, "player")

    if actor == "dealer" and "," in player_hand_values:
        player_hand_values = player_hand_values[-2:]
        player_hand_values_text = "handwaarde is:"

    content = "Huidige handen:\n"


    if actor == "dealer":
        content += f"""
Dealer:      {format_hand(dealer_hand)}
Speler:      {format_hand(player_hand)}

Dealer {dealer_hand_values_text} {dealer_hand_values}
Speler {player_hand_values_text} {player_hand_values}"""

    else:
        content += f"""
Dealer:      {format_hand([dealer_hand[0]])} | ??
Speler:      {format_hand(player_hand)}

Speler {player_hand_values_text} {player_hand_values}"""

    display_page(location=game.capitalize(),
                 title="Spelopties",
                 content=content
                 )

    return (
        dealer_hand_values,
        dealer_hand_values_text,
        dealer_status,
        player_hand_values,
        player_hand_values_text,
        player_status,
    )


def show_initial_deal(player_hand, dealer_hand, game):
    """
    Displays the initial blackjack deal.

    Args:
        player_hand (list): The player's initial hand.
        dealer_hand (list): The dealer's initial hand.
        game (str): The current game.
    """
    content = "De kaarten worden gedeeld."

    display_page(location=game.capitalize(),
                 title="Speelronde",
                 content=content
                 )

    time.sleep(1)
    print_message(f"1e kaart speler:   {format_hand([player_hand[0]])}")
    time.sleep(1)
    print_message(f"1e kaart dealer:   {format_hand([dealer_hand[0]])}")
    time.sleep(1)
    print_message(f"2e kaart speler:   {format_hand([player_hand[1]])}")
    time.sleep(1)
    print_message("2e kaart dealer:   ??")
    time.sleep(1)
    print()
    get_input(CONTINUE_PROMPT)


# ==============================
# BLACKJACK GAMEPLAY
# ==============================

def play_player_hand(shoe, cards_until_shuffle, player_hand, dealer_hand, game):
    """
    Controls the player's blackjack turn.

    Args:
        shoe (list): The current blackjack shoe.
        cards_until_shuffle (int): The number of cards that can still be dealt before shuffling.
        player_hand (list): The player's current hand.
        dealer_hand (list): The dealer's current hand.
        game (str): The current game.

    Returns:
        tuple: The updated shoe, cards until shuffle, player hand,
        final player hand value and player status.
    """
    actor = "player"
    first_turn = True

    while True:
        (
            dealer_hand_values,
            dealer_hand_values_text,
            dealer_status,
            player_hand_values,
            player_hand_values_text,
            player_status,
        ) = prepare_play_hand(player_hand, dealer_hand, game, actor)

        if player_status == "bust":
            print_message(f"U heeft [default]{player_hand_values}[/]. Player bust!")
            print()
            get_input(CONTINUE_PROMPT)

            break

        elif player_status == "blackjack":
            print_message("U heeft blackjack!")
            print()
            get_input(CONTINUE_PROMPT)

            break

        elif player_status == "stand":
            print_message("U heeft 21!")
            print()
            get_input(CONTINUE_PROMPT)

            break

        else:
            if first_turn:
                dealer_card = dealer_hand[0][1:]

                if dealer_card == "A":
                    high_card = "aas"
                elif dealer_card == "K":
                    high_card = "koning"
                elif dealer_card == "Q":
                    high_card = "koningin"
                elif dealer_card == "J":
                    high_card = "boer"
                elif dealer_card == "10":
                    high_card = "10"
                else:
                    high_card = ""

                if high_card:
                    print_message(
                        f"De dealer toont een {high_card} en controleert "
                        f"de gesloten kaart op blackjack",
                        end=""
                    )
                    time.sleep(1)
                    print_message("[default].[/]", end="", indent=0)
                    time.sleep(1)
                    print_message("[default].[/]", end="", indent=0)
                    time.sleep(1)
                    print_message("[default].[/]", indent=0)
                    print()

                    if dealer_status == "blackjack":
                        print_message(f"Dealer draait kaarten om: {format_hand(dealer_hand)}")
                        print()
                        print_message("Dealer heeft blackjack!")
                        print()
                        get_input(CONTINUE_PROMPT)

                        player_status = "dealer_blackjack"
                        player_hand_values = player_hand_values[-2:]

                        break

                    else:
                        print_message("De dealer heeft geen blackjack, het spel gaat verder.")
                        print()

            menu_options = ["Hit", "Stand"]

            console.print(
                Padding(display_menu_table(menu_options, width=70), (0, 0, 1, 5))
            )

            menu_choice = get_menu_choice(range(1, 3))

            if menu_choice == 1:
                shoe, cards_until_shuffle, player_hand = draw_card(shoe, cards_until_shuffle, player_hand)
                print_message(f"U ontvangt een extra kaart: {format_hand([player_hand[-1]])}")
                print()
                get_input(CONTINUE_PROMPT)

                first_turn = False
                continue

            else:
                if "," in player_hand_values:
                    player_hand_values = player_hand_values[-2:]

                print_message(f"U heeft stand gekozen met [default]{player_hand_values}[/]. De beurt is aan de dealer.")
                print()
                get_input(CONTINUE_PROMPT)

                player_status = "stand"

            break

    return shoe, cards_until_shuffle, player_hand, player_hand_values, player_status


def play_dealer_hand(shoe, cards_until_shuffle, player_hand, dealer_hand, game):
    """
    Controls the dealer's blackjack turn.

    Args:
        shoe (list): The current blackjack shoe.
        cards_until_shuffle (int): The number of cards that can still be dealt before shuffling.
        player_hand (list): The player's final hand.
        dealer_hand (list): The dealer's current hand.
        game (str): The current game.

    Returns:
        tuple: The updated shoe, cards until shuffle, dealer status
        and final dealer hand value.
    """
    actor = "dealer"

    panel_content = f"De dealer onthult de gesloten kaart: {format_hand([dealer_hand[1]])}"

    display_page(location=game.capitalize(),
                 title="Dealerhand",
                 content=panel_content
                 )

    get_input(CONTINUE_PROMPT)

    while True:
        (
            dealer_hand_values,
            dealer_hand_values_text,
            dealer_status,
            player_hand_values,
            player_hand_values_text,
            player_status,
        ) = prepare_play_hand(player_hand, dealer_hand, game, actor)

        if player_status == "blackjack":
            if dealer_status == "blackjack":
                print_message("Speler en dealer hebben beide blackjack! Push!")
                print()
                get_input(CONTINUE_PROMPT)

            else:
                print_message("Dealer heeft geen blackjack.")
                print()
                get_input(CONTINUE_PROMPT)

                dealer_status = "no_blackjack"

            break

        if dealer_status == "hit":
            shoe, cards_until_shuffle, dealer_hand = draw_card(shoe, cards_until_shuffle, dealer_hand)
            print_message(f"Dealer ontvangt een extra kaart: {format_hand([dealer_hand[-1]])}")
            print()
            get_input(CONTINUE_PROMPT)

            continue

        elif dealer_status == "blackjack":
            print_message("Dealer heeft blackjack!")
            print()
            get_input(CONTINUE_PROMPT)

        elif dealer_status == "bust":
            print_message(f"Handwaarde is [default]{dealer_hand_values}[/]. Dealer bust!")
            print()
            get_input(CONTINUE_PROMPT)

        else:
            if "," in dealer_hand_values:
                dealer_hand_values = dealer_hand_values[-2:]

            print_message(f"Handwaarde is [default]{dealer_hand_values}[/]. Dealer stand!")
            print()
            get_input(CONTINUE_PROMPT)

            dealer_status = "stand"

        break

    return shoe, cards_until_shuffle, dealer_status, dealer_hand_values[-2:]


# ==============================
# PROGRAM FLOW
# ==============================

def play(current_user) -> str:
    """
    Controls the blackjack game flow.

    Args:
        current_user (dict): The profile of the current user.

    Returns:
        str: The action to perform.
    """
    game = NAME_GAME

    shoe, cards_until_shuffle = get_new_shoe()
    action, stake = prepare_game(current_user, game, GAME_INSTRUCTIONS, PAYOUT_STRUCTURE)

    if action in ("choose_game", "main_menu"):
        return action

    update_game_stats(current_user, game, "game_started")

    # Continue playing blackjack hands until another destination is selected.
    while True:
        action, stake = handle_round_setup(current_user, stake, action, game)

        if action in ("choose_game", "main_menu"):
            break

        current_user["played_games"][game]["rounds_played"] += 1
        current_user["playing_balance"] = round(current_user["playing_balance"] - stake, 2)

        if cards_until_shuffle <= 0:
            shoe, cards_until_shuffle = get_new_shoe()

        shoe, cards_until_shuffle, dealer_hand, player_hand = deal_cards(shoe, cards_until_shuffle)
        show_initial_deal(player_hand, dealer_hand, game)

        (
            shoe,
            cards_until_shuffle,
            player_hand,
            player_hand_value,
            player_status,
        ) = play_player_hand(shoe, cards_until_shuffle, player_hand, dealer_hand, game)

        if player_status == "bust":
            dealer_status = "stand"
            dealer_hand_value = ""

        elif player_status == "dealer_blackjack":
            dealer_status = "blackjack"
            dealer_hand_value = "21"

        else:
            (
                shoe,
                cards_until_shuffle,
                dealer_status,
                dealer_hand_value,
            ) = play_dealer_hand(shoe, cards_until_shuffle, player_hand, dealer_hand, game)

        game_result = determine_game_result(player_status, player_hand_value, dealer_status, dealer_hand_value)

        process_payout(current_user, game_result, stake, game)
        action = get_round_action(current_user, stake, game)

    return action
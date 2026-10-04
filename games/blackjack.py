# ==============================
# FUNCTION IMPORTS
# ==============================

import random
import time

from utils.game_utils import (
    prepare_game,
    get_menu_choice,
    get_round_action,
    resolve_insufficient_balance,
    get_stake,
)
from utils.utils import (
    clear_terminal,
    format_currency
)

# ==============================
# CONSTANTS
# ==============================

from utils.constants import (
    WHITE_BACKGROUND,
    BLACK,
    RED,
    GREEN,
    ORANGE,
    RESET,
    CONTINUE_PROMPT,
    SEPARATOR,
    SUITS,
    RANKS,
    BLACKJACK_MULTIPLIER,
    WIN_MULTIPLIER,
    PUSH_MULTIPLIER,
)


# ==============================
# CONFIGURATION
# ==============================

TRIGGER = "blackjack"
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
Heeft u evenveel punten als de dealer, dan is het gelijkspel en krijgt u uw inzet terug.

Uitbetaling:
{SEPARATOR}
Blackjack                = 2,5x inzet
Gewonnen                 = 2x inzet
Gelijkspel               = 1x inzet"""

##############################################################################

def get_new_shoe():
    shoe = []

    for i in range(1, DECKS_IN_SHOE + 1):
        shoe += [f"{suit}{rank}" for suit in SUITS for rank in RANKS]

    random.shuffle(shoe)

    cards_until_shuffle = random.randint(
        int(len(shoe) * 0.70),
        int(len(shoe) * 0.90),
    )

    return shoe, cards_until_shuffle

##############################################################################

def deal_cards(shoe, cards_until_shuffle):

    player_hand = [shoe.pop(0)]
    dealer_hand = [shoe.pop(0)]

    player_hand.append(shoe.pop(0))
    dealer_hand.append(shoe.pop(0))

    cards_until_shuffle -= 4
    return shoe, cards_until_shuffle, dealer_hand, player_hand

##############################################################################

def draw_card(shoe, cards_until_shuffle, playing_hand):

    playing_hand.append(shoe.pop(0))
    cards_until_shuffle -= 1

    return shoe, cards_until_shuffle, playing_hand

##############################################################################

def calculate_hand_values(playing_hand, actor):
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

##############################################################################

def determine_game_results(player_status, player_hand_value, dealer_status, dealer_hand_value):
    if player_status in ("bust", "dealer_blackjack"):
        game_result = "lose"

        return game_result

    if "," in player_hand_value:
        player_hand_value = player_hand_value[-2:]
    player_hand_value = int(player_hand_value)

    if "," in dealer_hand_value:
        dealer_hand_value = dealer_hand_value[-2:]
    dealer_hand_value = int(dealer_hand_value)

    game_result = "lose"

    if player_status == "blackjack":
        if dealer_status == "blackjack":
            game_result = "push"
        else:
            game_result = "blackjack"

    elif player_status == "stand":
        if dealer_status == "bust":
            game_result = "win"

        elif dealer_status == "stand":
            if player_hand_value > dealer_hand_value:
                game_result = "win"
            elif player_hand_value == dealer_hand_value:
                game_result = "push"

    return game_result

##############################################################################

def format_hand(hand):
    formatted_hand = ""

    for card in hand:
        suit = card[0]
        value = card[1:]
        if suit in ("♥", "♦"):
            suit_color = RED
        else:
            suit_color = BLACK
        formatted_hand += f"{WHITE_BACKGROUND}{suit_color}{card[0]}{RESET}{WHITE_BACKGROUND}{value}{RESET} | "

    formatted_hand = formatted_hand[:-3]

    return formatted_hand

##############################################################################

def prepare_play_hand(player_hand, dealer_hand, trigger, actor):
    clear_terminal()

    dealer_hand_values, dealer_hand_values_text, dealer_status = calculate_hand_values(dealer_hand, "dealer")
    player_hand_values, player_hand_values_text, player_status = calculate_hand_values(player_hand, "player")

    print(f"""
{trigger.capitalize()} - Spelopties
{SEPARATOR}
Huidige handen:""")

    if actor == "dealer":
        print(f"""
Dealer:      {format_hand(dealer_hand)}
Speler:      {format_hand(player_hand)}

Dealer {dealer_hand_values_text} {dealer_hand_values}
Speler {player_hand_values_text} {player_hand_values}
{SEPARATOR}
""")

    else:
        print(f"""
Dealer:      {format_hand([dealer_hand[0]])} | ??
Speler:      {format_hand(player_hand)}

Speler {player_hand_values_text} {player_hand_values}
{SEPARATOR}
""")

    return (
        dealer_hand_values,
        dealer_hand_values_text,
        dealer_status,
        player_hand_values,
        player_hand_values_text,
        player_status,
    )

##############################################################################

def play_player_hand(shoe, cards_until_shuffle, player_hand , dealer_hand, trigger):
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
        ) = prepare_play_hand(
            player_hand,
            dealer_hand,
            trigger,
            actor,
        )

        if player_status == "bust":
            print(f"U heeft {int(player_hand_values)}. Player bust!")
            print()
            input(CONTINUE_PROMPT)

            player_status = "bust"

        elif player_status == "blackjack":
            print(f"U heeft blackjack!")
            print()
            input(CONTINUE_PROMPT)

            player_status = "blackjack"


        elif player_status == "stand":
            print(f"U heeft 21!")
            print()
            input(CONTINUE_PROMPT)

            player_status = "stand"

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
                    high_card = False

                if high_card:
                    print(f"De dealer toont een {high_card} en controleert de gesloten kaart op blackjack", end="")
                    time.sleep(1)
                    print(".", end="")
                    time.sleep(1)
                    print(".", end="")
                    time.sleep(1)
                    print(".", end="\n")
                    print()

                    if dealer_status == "blackjack":
                        print(f"dealer draait kaarten om: {format_hand(dealer_hand)}")
                        print()
                        print("Dealer heeft blackjack!")
                        print()
                        input(CONTINUE_PROMPT)

                        player_status = "dealer_blackjack"

                        return shoe, cards_until_shuffle, player_hand, player_hand_values[-2:], player_status

                    else:
                        print("De dealer heeft geen blackjack, het spel gaat verder.")
                        print()

            print(f"""Wat wilt u doen?
{SEPARATOR}
1. Hit
2. Stand
{SEPARATOR}""")

            menu_choice = get_menu_choice(range(1, 3))

            if menu_choice == 1:
                print()
                shoe, cards_until_shuffle, player_hand = draw_card(shoe, cards_until_shuffle, player_hand)
                print(f"U ontvangt een extra kaart: {format_hand([player_hand[-1]])}")
                print()
                input(CONTINUE_PROMPT)
                first_turn = False
                continue

            else:
                if "," in player_hand_values:
                    player_hand_values = player_hand_values[-2:]
                print()
                print(f"U heeft stand gekozen met {player_hand_values}. De beurt is aan de dealer.")
                print()
                input(CONTINUE_PROMPT)

                player_status = "stand"

        return shoe, cards_until_shuffle, player_hand, player_hand_values, player_status

##############################################################################

def play_dealer_hand(shoe, cards_until_shuffle, player_hand, dealer_hand, trigger):
    actor = "dealer"
    first_turn = True

    while True:
        (
            dealer_hand_values,
            dealer_hand_values_text,
            dealer_status,
            player_hand_values,
            player_hand_values_text,
            player_status,
        ) = prepare_play_hand(
            player_hand,
            dealer_hand,
            trigger,
            actor,
        )

        if first_turn:
            print(f"De dealer onthult de gesloten kaart: {format_hand([dealer_hand[1]])}")
            print()
            print(SEPARATOR)
            print()
            if player_status != "blackjack":
                first_turn = False
                time.sleep(1)

        if dealer_status == "hit":
            if player_status == "blackjack":
                print("Dealer heeft geen blackjack." )
                print()
                input(CONTINUE_PROMPT)

                dealer_status = "no_blackjack"

            else:
                shoe, cards_until_shuffle, dealer_hand = draw_card(shoe, cards_until_shuffle, dealer_hand)
                print(f"Dealer ontvangt een extra kaart: {format_hand([dealer_hand[-1]])}")
                print()
                input(CONTINUE_PROMPT)
                continue

        elif dealer_status == "blackjack":
            if player_status == "blackjack":
                print("Speler en dealer hebben beide blackjack! Push!")
                print()
                input(CONTINUE_PROMPT)

                dealer_status = "blackjack"

            else:
                print("Dealer heeft blackjack!")
                print()
                input(CONTINUE_PROMPT)

                dealer_status = "blackjack"

        elif dealer_status == "bust":
            print(f"Handwaarde is {dealer_hand_values}. Dealer bust!")
            print()
            input(CONTINUE_PROMPT)

            dealer_status = "bust"

        else:
            if "," in dealer_hand_values:
                dealer_hand_values = dealer_hand_values[-2:]

            print(f"Handwaarde is {dealer_hand_values}. Dealer stand!")
            print()
            input(CONTINUE_PROMPT)

            dealer_status = "stand"

        return shoe, cards_until_shuffle, dealer_status, dealer_hand_values[-2:]

##############################################################################

def process_payout(game_result, playing_balance, stake, trigger):
    clear_terminal()

    match game_result:
        case "blackjack":
            multiplier = BLACKJACK_MULTIPLIER
        case "win":
            multiplier = WIN_MULTIPLIER
        case "push":
            multiplier = PUSH_MULTIPLIER
        case _:
            multiplier = 0

    payout = round(stake * multiplier, 2)

    print(f"""
{trigger.capitalize()} - Speluitslag
{SEPARATOR}
""")

    if 0 < payout > stake:
        print(f""" 
Gefeliciteerd, u heeft {GREEN}gewonnen{RESET}!
Uw uitbetaling bedraagt {format_currency(payout)}.

{SEPARATOR}
""")

    elif payout == stake:
        print(f"""
Het is {ORANGE}gelijkspel{RESET}.
U krijgt uw inzet van {format_currency(stake)} terug.

{SEPARATOR}
""")
    else:
        print(f"""        
Helaas, u heeft {RED}verloren{RESET}.       
       
{SEPARATOR}
""")

    playing_balance = round(playing_balance + payout, 2)

    input(CONTINUE_PROMPT)

    return playing_balance

##############################################################################

def play_round(player_hand, dealer_hand, trigger):
    clear_terminal()

    print(f"""
{trigger.capitalize()} - Speelronde
{SEPARATOR}
""")
    print("De kaarten worden gedeeld", end="")
    #time.sleep(1)
    print(".", end="")
    #time.sleep(1)
    print(".", end="")
    #time.sleep(1)
    print(".", end="\n")
    print()
    #time.sleep(1)
    print(f"1e kaart speler:   {format_hand([player_hand[0]])}")
    #time.sleep(1)
    print(f"1e kaart dealer:   {format_hand([dealer_hand[0]])}")
    #time.sleep(1)
    print(f"2e kaart speler    {format_hand([player_hand[1]])}")
    #time.sleep(1)
    print(f"2e kaart dealer:   ??")
    #time.sleep(1)
    print(SEPARATOR)
    print()
    input(CONTINUE_PROMPT)

##############################################################################


# ==============================
# STATE
# ==============================



# ==============================
# MENUS AND USER INPUT
# ==============================



# ==============================
# BLACKJACK GAME LOGIC
# ==============================



# ==============================
# OUTPUT
# ==============================



# ==============================
# PROGRAM FLOW
# ==============================

def play(playing_balance):
    """
    Controls the blackjack game flow.

    Args:


    Returns:

    """
    trigger = TRIGGER

    shoe, cards_until_shuffle = get_new_shoe()
    action, playing_balance, stake = prepare_game(playing_balance, trigger, GAME_INSTRUCTIONS)

    if action in ("choose_game", "main_menu"):
        return playing_balance, action

    # Continue playing blackjack hands until another destination is selected.
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

            action, playing_balance, stake = get_round_action(playing_balance, stake, trigger)
            continue

        if playing_balance < stake:
            action, playing_balance, stake = resolve_insufficient_balance(playing_balance, stake, trigger)

            if action in ("choose_game", "main_menu"):
                break

            action, playing_balance, stake = get_round_action(playing_balance, stake, trigger)

            # Any balance or stake change must be confirmed before spinning.
            continue

        playing_balance = round(playing_balance - stake, 2)

        if cards_until_shuffle <= 0:
            shoe, cards_until_shuffle = get_new_shoe()

        shoe, cards_until_shuffle, dealer_hand, player_hand = deal_cards(shoe, cards_until_shuffle)
        play_round(player_hand, dealer_hand, trigger)

        shoe, cards_until_shuffle, player_hand, player_hand_value, player_status = play_player_hand(shoe, cards_until_shuffle, player_hand, dealer_hand, trigger)
        if player_status == "bust":
            dealer_status = "stand"
            dealer_hand_value = ""

        elif player_status == "dealer_blackjack":
            dealer_status = "blackjack"
            dealer_hand_value = "21"

        else:
            shoe, cards_until_shuffle, dealer_status, dealer_hand_value = play_dealer_hand(shoe, cards_until_shuffle, player_hand, dealer_hand, trigger)

        game_result = determine_game_results(player_status, player_hand_value, dealer_status, dealer_hand_value)
        playing_balance = process_payout(game_result, playing_balance, stake, trigger)
        action, playing_balance, stake = get_round_action(playing_balance, stake, trigger)

    return playing_balance, action
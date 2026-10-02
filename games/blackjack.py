# ==============================
# FUNCTION IMPORTS
# ==============================

import random
import time

from utils.game_utils import (
    prepare_game,
)

# ==============================
# CONSTANTS
# ==============================

from utils.constants import (
    WHITE_BACKGROUND,
    BLACK,
    RED,
    RESET,
    CONTINUE_PROMPT,
    INVALID_INPUT,
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

TRIGGER = "blackjacktafel"
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


def get_new_shoe():
    shoe = []

    for i in range(1, DECKS_IN_SHOE + 1):
        shoe += [f"{suit} {rank}" for suit in SUITS for rank in RANKS]

    random.shuffle(shoe)

    return shoe


def deal_cards(shoe):
    dealer_hand = [shoe.pop(0),shoe.pop(1)]
    player_hand = [shoe.pop(2),shoe.pop(3)]

    return shoe, dealer_hand, player_hand


def draw_card(deck, hand):
    hand.append(deck.pop(0))

    return deck, hand


def calculate_hand_values(hand):
    total_values = [0]
    for card in hand:
        card_value = card[1::]

        if card_value in ("J", "Q", "K"):
            card_value = 10

        elif card_value == "A":
            new_values = []

            for value in total_values:
                new_values.append(value + 1)
                new_values.append(value + 11)

            total_values = sorted(set(new_values))
            continue

        else:
            card_value = int(card_value)

        total_values = [value + card_value for value in total_values]

        for value in total_values:
            if value == 21:
                return [21]

    total_values = [total_values[0]] + [value for value in total_values[1:] if value < 21]

    return total_values





































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

def play(playing_balance) -> tuple[int | float, str]:
    """
    Controls the blackjack game flow.

    Args:


    Returns:

    """
    trigger = TRIGGER

    shoe = get_new_shoe()
    shoe, dealer_hand, player_hand = deal_cards(shoe)
    action, playing_balance, stake = prepare_game(playing_balance, trigger, GAME_INSTRUCTIONS)

    if action in ("choose_game", "main_menu"):
        return playing_balance, action

    # while True:
    #     action, bet_choice, selected_number = get_bet_choice(
    #         playing_balance,
    #         stake,
    #         roulette_history,
    #         trigger
    #     )
    #
    #     if action == "change_stake":
    #         action, playing_balance, stake = get_stake(playing_balance, stake, trigger)
    #
    #         if action in ("choose_game", "main_menu"):
    #             return playing_balance, action
    #
    #         continue
    #
    #     if action in ("choose_game", "main_menu"):
    #         return playing_balance, action
    #
    #     break
    #
    # # Continue playing roulette rounds until another destination is selected.
    # while True:
    #     action, playing_balance, stake, bet_choice, selected_number = confirm_bet(
    #         playing_balance,
    #         stake,
    #         bet_choice,
    #         selected_number,
    #         roulette_history,
    #         trigger
    #     )
    #
    #     if action in ("choose_game", "main_menu"):
    #         break
    #
    #     if playing_balance < stake:
    #         action, playing_balance, stake = resolve_insufficient_balance(playing_balance, stake, trigger)
    #
    #         if action in ("choose_game", "main_menu"):
    #             break
    #
    #         # Any balance or stake change must be confirmed before spinning.
    #         continue
    #
    #     playing_balance = round(playing_balance - stake, 2)
    #     spin_result = random.randint(0, 36)
    #     color, parity = determine_color_and_parity(spin_result)
    #
    #     add_recent_result(roulette_history, spin_result, color)
    #     show_spin_result(spin_result, color)
    #
    #     playing_balance = determine_win(
    #         playing_balance,
    #         stake,
    #         bet_choice,
    #         selected_number,
    #         spin_result,
    #         color,
    #         parity
    #     )

    return playing_balance, action
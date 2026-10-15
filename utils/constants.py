# ==============================
# CASINO INFORMATION
# ==============================

CASINO_NAME = "Casino de Gouden Driehoek"


# ==============================
# USER INTERFACE
# ==============================

INVALID_INPUT = f"\n{" " * 5}Ongeldige invoer. Probeer het opnieuw.\n"
CONTINUE_PROMPT = "Druk op Enter om verder te gaan."
CHOOSE_OPTION = "Kies een optie: "


# ==============================
# CASINO REQUIREMENTS
# ==============================

MIN_AGE = 18


# ==============================
# FIXED CASINO COSTS
# ==============================

ADMISSION_PRICE = 5.00
SERVICE_FEE = 3.50
MANDATORY_DRINK_PRICE = 2.70
VAT_RATE = 21.0


# ==============================
# SLOT MACHINE CONFIGURATION
# ==============================

SYMBOL_MULTIPLIERS = {
    "cherry": 1,
    "bell": 2,
    "diamond": 4,
}

JACKPOT_SYMBOL = "diamond"

MATCH_MULTIPLIERS = {
    2: 0.5,
    3: 2,
    "jackpot": 2,
}


# ==============================
# BLACKJACK CONFIGURATION
# ==============================

SUITS = ["♠", "♥", "♦", "♣"]
RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

BLACKJACK_MULTIPLIER = 2.5
BLACKJACK_WIN_MULTIPLIER = 2
BLACKJACK_PUSH_MULTIPLIER = 1
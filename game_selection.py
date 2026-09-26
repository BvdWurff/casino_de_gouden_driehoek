from games import roulette, dobbelen, fruitmachine
import utils

SEPARATOR = '-' * 50
CASINO_NAME = "Casino de Gouden Driehoek"
INVALID_INPUT = "\nOngeldige invoer. Probeer het opnieuw.\n"

AVAILABLE_GAMES = {
    1: ("Roulette", roulette),
    2: ("Dobbelen", dobbelen),
    3: ("Fruitmachine", fruitmachine),
}

def choose_game(playing_balance):
    while True:
        print(f"""{CASINO_NAME} - Spellen
{SEPARATOR}
Beschikbare spellen:
""")
        for number, game in AVAILABLE_GAMES.items():
            print(f"{number}. {game[0]}")
        print(f"""
0. Terug naar hoofdmenu
{SEPARATOR}""")
        try:
            choice = int(input("Kies een optie: "))
            print()

            if choice == 0:
                return playing_balance

            if choice in AVAILABLE_GAMES:
                game_name, game_module = AVAILABLE_GAMES[choice]
                playing_balance, action = game_module.play(playing_balance)
                if action == "main_menu":
                    return playing_balance
            else:
                print(INVALID_INPUT)
        except ValueError:
            print(INVALID_INPUT)

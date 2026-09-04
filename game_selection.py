import dobbelen
import roulette

SEPARATOR = '-' * 32
INVALID_ANSWER = "Ongeldige invoer. Probeer het opnieuw."

AVAILABLE_GAMES = {
    "roulette": roulette,
    "dobbelen": dobbelen
}

def choose_game(playing_balance):
    while True:
        print("Kies een spel uit de onderstaande lijst of typ 'stoppen' om het casino te verlaten.")
        print()
        print("Beschikbare spellen:")
        print(SEPARATOR)
        for game in AVAILABLE_GAMES:
            print(game.title())
        print(SEPARATOR)
        print()
        selected_game = input("Uw keuze: ").lower()
        if selected_game == "stoppen":
            print()
            print(f"U verlaat het casino met een eindsaldo van €{playing_balance:.2f}.")
            print()
            print("Bedankt voor uw bezoek aan Casino de Gouden Driehoek.")
            print("Graag tot ziens!")
            exit(0)
        elif selected_game in AVAILABLE_GAMES:
            playing_balance = AVAILABLE_GAMES[selected_game].play(playing_balance)
        else:
            print()
            print(INVALID_ANSWER)
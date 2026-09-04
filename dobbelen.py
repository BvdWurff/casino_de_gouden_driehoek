# Spel dat ik tijdens de les als opdracht heb gebouwd. Hierin heb ik bijvoorbeeld
# nog geen try/except-validatie toegevoegd. Omdat dobbelen wel in game_selection
# is opgenomen, laat ik het spel in het project staan.

import time
import random

INVALID_ANSWER = "Ongeldige invoer. Probeer het opnieuw."


def play(playing_balance):
    print()
    print("Welkom aan de dobbeltafel.")
    print()
    print("Het doel van het spel is om met één of meerdere worpen een totaal van 4 of 5 te behalen.")
    print("Gooit u minder dan 4? Dan blijft u gooien en worden de worpen bij elkaar opgeteld.")
    print("Eindigt u op 4 of 5? Dan wint u en ontvangt u uw inzet als winst.")
    print("Komt het totaal boven de 5? Dan verliest u uw inzet.")
    print()
    stake = float(input(f"Uw saldo is €{playing_balance:.2f}. Hoeveel wilt u inzetten? €"))
    while stake > playing_balance or stake <= 0:
        if stake <= 0:
            print("De inzet moet hoger zijn dan €0.")

        else:
            print("Uw saldo is niet toereikend voor deze inzet.")

        print()
        stake = float(input(f"Uw saldo is €{playing_balance:.2f}. Hoeveel wilt u inzetten? €"))
    print()
    print("Uw inzet is geaccepteerd. Het spel kan beginnen. Veel geluk!")
    print()

    def roll_dice():
        return random.randint(1, 6)

    while True:
        question = "Druk op Enter om te gooien, typ 'inzet' om uw inzet aan te passen of 'stoppen' om de dobbeltafel te verlaten: "
        choice = input(question).lower()

        while choice not in ("", "stoppen", "inzet"):
            print("Dit is geen geldige keuze.")
            choice = input(question).lower()

        if choice == "stoppen":
            print()
            print(f"U verlaat het dobbelspel met een saldo van €{playing_balance:.2f}. Bedankt voor het spelen!")
            print()
            return playing_balance

        elif choice == "inzet":
            print()
            print(f"Uw saldo is €{playing_balance:.2f}")
            stake = float(input(f"Uw huidige inzet is €{stake:.2f}. Hoeveel wilt u inzetten? €"))

            while stake > playing_balance or stake <= 0:
                if stake <= 0:
                    print("U heeft een foutieve inzet gekozen. Pas de inzet aan.")

                else:
                    print("Uw saldo is niet toereikend voor deze inzet. Pas de inzet aan.")
                print()
                stake = float(input(f"Uw saldo is €{playing_balance:.2f}. Hoeveel wilt u inzetten? €"))

            print("Uw inzet is aangepast.")
            print()
        else:
            if stake > playing_balance:
                print()
                print("Uw inzet is hoger dan uw huidige saldo. Wilt u saldo toevoegen?")
                answer = input("Uw keuze (ja/nee): ").lower()

                if answer == "nee":
                    print()
                    print(
                        f"U verlaat het dobbelspel met een saldo van €{playing_balance:.2f}. Bedankt voor het spelen!")
                    print()
                    return playing_balance

                while True:
                    try:
                        playing_balance = float(input(f"Voer een nieuw saldo in van minimaal €{stake:.2f}: €"))
                        if playing_balance > 0:
                            break
                        else:
                            print(INVALID_ANSWER)
                    except ValueError:
                        print(INVALID_ANSWER)
                print()
                continue

            roll = roll_dice()
            print()
            time.sleep(2)
            print(f"U heeft {roll} gegooid!")
            print()

            while roll < 4:
                input("Druk op Enter om opnieuw te gooien.")
                print()
                roll_2 = roll_dice()
                total = roll + roll_2
                print(f"U heeft {roll_2} gegooid!")
                print(f"Uw totaal is nu {total}.")
                print()

            if roll in (4, 5):
                playing_balance += stake
                print(f"Gefeliciteerd! U wint €{stake:.2f}. Uw nieuwe saldo is €{playing_balance:.2f}.")
                print()
                print("Wilt u nog een ronde spelen?")

            else:
                playing_balance -= stake
                print(f"Helaas, u verliest €{stake:.2f}. Uw nieuwe saldo is €{playing_balance:.2f}.")
                print()
                print("Wilt u nog een ronde spelen?")
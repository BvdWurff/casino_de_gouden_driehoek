import time
import random

SEPARATOR = '-' * 32
INVALID_ANSWER = "Ongeldige invoer. Probeer het opnieuw."

AVAILABLE_CHOICES = [
    "1. Rood   - winst: 1x inzet",
    "2. Zwart  - winst: 1x inzet",
    "3. Groen  - winst: 35x inzet",
    "4. Even   - winst: 1x inzet",
    "5. Oneven - winst: 1x inzet",
    "6. Nummer - winst: 35x inzet",
    "0. Stoppen"
]

ROUND_OPTIONS = [
    "1. Opnieuw spelen met dezelfde keuze en inzet",
    "2. Keuze aanpassen",
    "3. Inzet aanpassen",
    "4. Keuze en inzet aanpassen",
    "0. Roulettetafel verlaten"
]

def new_stake(playing_balance):
    while True:
        try:
            check_stake = float(input(f"Uw saldo is €{playing_balance:.2f}. Hoeveel wilt u inzetten? €"))
            if check_stake > playing_balance or check_stake <= 0:
                if check_stake <= 0:
                    print("De inzet moet hoger zijn dan €0.")
                else:
                    print("Uw saldo is niet toereikend voor deze inzet.")
            else:
                break
        except ValueError:
            print(INVALID_ANSWER)
    return check_stake


def get_gamble_choice():
    print("Kies waarop u wilt inzetten:")
    print(SEPARATOR)
    for options in AVAILABLE_CHOICES:
        print(options)
    print(SEPARATOR)
    print()
    gamble_choice = input("Uw keuze: ")
    while gamble_choice not in ("1", "2", "3", "4", "5", "6", "0"):
        print(INVALID_ANSWER)
        print()
        gamble_choice = input("Uw keuze: ")
    gamble_choice = int(gamble_choice)
    return gamble_choice


def play(playing_balance):
    print()
    print("Welkom aan de roulettetafel.")
    print()
    print("Het doel van roulette is om te voorspellen waar het balletje zal landen.")
    print("Kies waarop u wilt inzetten en bepaal vervolgens uw inzet.")
    print("Het balletje kan op één van de 37 getallen van 0 tot en met 36 landen.")
    print("In het overzicht ziet u per keuze hoeveel winst u kunt behalen.")
    print()
    stake = new_stake(playing_balance)
    print()
    print("Uw inzet is geaccepteerd. Het spel kan beginnen. Veel geluk!")
    print()
    choice = get_gamble_choice()
    number = None
    while True:
        if choice == 0:
            print()
            print(f"U verlaat de roulettetafel met een saldo van €{playing_balance:.2f}. Bedankt voor het spelen!")
            print()
            return playing_balance

        if choice == 6 and number is None:
            while True:
                try:
                    number = int(input("Op welk nummer wilt u inzetten? (0 t/m 36) "))
                    if 0 <= number <= 36:
                        break
                    else:
                        print(INVALID_ANSWER)
                except ValueError:
                    print(INVALID_ANSWER)

        if stake > playing_balance:
            print()
            print(f"Uw huidige inzet van €{stake:.2f} is hoger dan uw saldo van €{playing_balance:.2f}.")
            print("Wilt u uw saldo verhogen?")
            answer = input("Uw keuze (ja/nee): ").lower()
            while answer not in ("ja", "nee"):
                print(INVALID_ANSWER)
                print()
                answer = input("Uw keuze (ja/nee): ").lower()

            if answer == "nee":
                print()
                print(f"U verlaat de roulettetafel met een saldo van €{playing_balance:.2f}.")
                print("Bedankt voor het spelen!")
                print()
                return playing_balance

            while True:
                try:
                    playing_balance = float(input(f"Voer een nieuw saldo in van minimaal €{stake:.2f}: €"))
                    if playing_balance >= stake:
                        break
                    elif playing_balance <= 0:
                        print(INVALID_ANSWER)
                    else:
                        print(f"Het nieuwe saldo moet minimaal €{stake:.2f} bedragen.")
                except ValueError:
                    print(INVALID_ANSWER)
            print()
            continue

        playing_balance -= stake
        spin_result = random.randint(0, 36)

        # Bepaal de kleur en of het getal even of oneven is
        if spin_result == 0:
            color = 'groen'
            parity = ''
        elif spin_result <= 18:
            if spin_result % 2 == 0:
                color = 'zwart'
                parity = 'even'
            else:
                color = 'rood'
                parity = 'oneven'
        elif spin_result % 2 == 0:
            color = "rood"
            parity = "even"
        else:
            color = "zwart"
            parity = "oneven"

        print("Het balletje wordt gerold...")
        time.sleep(1)
        print("...")
        time.sleep(1)
        print(f"Het balletje is geland op {spin_result} {color}!")
        time.sleep(1)
        print()

        # Controleer of de gekozen inzet heeft gewonnen
        win = False
        multiplier = 2
        if choice == 1 and color == "rood":
            win = True
        elif choice == 2 and color == "zwart":
            win = True
        elif choice == 3 and color == "groen":
            win = True
            multiplier = 36
        elif choice == 4 and parity == "even":
            win = True
        elif choice == 5 and parity == "oneven":
            win = True
        elif choice == 6 and number == spin_result:
            win = True
            multiplier = 36

        if win:
            playing_balance += (stake * multiplier)
            gain = stake * multiplier - stake
            print(f"Gefeliciteerd! U wint €{gain:.2f}. Uw nieuwe saldo is €{playing_balance:.2f}.")
        else:
            print(f"Helaas, u verliest €{stake:.2f}. Uw nieuwe saldo is €{playing_balance:.2f}.")

        print()
        print("Kies uit één van de volgende opties:")
        print(SEPARATOR)
        for option in ROUND_OPTIONS:
            print(option)
        print(SEPARATOR)
        print()
        round_choice = input("Wat wilt u doen? ")
        print()
        while round_choice not in ("1", "2", "3", "4", "0"):
            print(INVALID_ANSWER)
            print()
            round_choice = input("Wat wilt u doen? ")
        round_choice = int(round_choice)

        if round_choice == 0:
            print(f"U verlaat de roulettetafel met een saldo van €{playing_balance:.2f}.")
            print("Bedankt voor het spelen!")
            return playing_balance

        elif round_choice == 1:
            continue

        else:
            if round_choice in (3, 4):
                stake = new_stake(playing_balance)
                print()
            if round_choice in (2, 4):
                number = None
                choice = get_gamble_choice()
            continue
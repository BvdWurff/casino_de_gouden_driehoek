import main
from utils import blank_lines
import time
import random


SEPARATOR = '-' * 50
CASINO_NAME = "Casino de Gouden Driehoek"
INVALID_INPUT = "\nOngeldige invoer. Probeer het opnieuw.\n"


def stake_to_high(stake, playing_balance):
    while True:
        print(f"""
        Uw saldo is ontoereikend voor deze inzet.

        1. Inzet wijzigen
        2. Saldo wijzigen
        3. Spel wijzigen
        0. Terug naar hoofdmenu
        {SEPARATOR}""")
        try:
            choice = int(input(f"Kies een optie: "))
            if 0 <= choice <= 3:
                if choice == 1:
                    print()
                    return playing_balance, "change_stake"
                elif choice == 2:
                    blank_lines(2)
                    playing_balance, _ = main.show_balance(playing_balance, trigger="roulettetafel")
                    if playing_balance < stake:
                       break
                    else:
                        return playing_balance, "continue"
                elif choice == 3:
                    blank_lines(2)
                    return playing_balance, "choose_game"
                blank_lines(2)
                return playing_balance, "main_menu"
            else:
                print(INVALID_INPUT)
        except ValueError:
            print(INVALID_INPUT)

def new_stake(playing_balance):
    while True:
        try:
            stake = float(input(f"Uw huidige saldo is €{playing_balance:.2f}. Hoeveel wilt u inzetten? € "))
            if stake > playing_balance or stake <= 0:
                if stake <= 0:
                    print()
                    print("De inzet moet hoger zijn dan €0.")
                    print()
                    break
                else:
                    playing_balance, action = stake_to_high(stake, playing_balance)
                    if action == "change_stake":
                        break
                    elif action != "continue":
                        return stake, playing_balance, action
            print()
            print("Uw inzet is geaccepteerd. Het spel kan beginnen. Veel geluk!")
            print()
            return stake, playing_balance, "continue"
        except ValueError:
            print(INVALID_INPUT)


def get_gamble_choice():
    print(f"""Kies waarop u wilt inzetten:
{SEPARATOR}
1. Rood   - winst: 1x inzet
2. Zwart  - winst: 1x inzet
3. Groen  - winst: 35x inzet
4. Even   - winst: 1x inzet
5. Oneven - winst: 1x inzet
6. Nummer - winst: 35x inzet

0. Stoppen
{SEPARATOR}""")
    while True:
        try:
            choice = int(input("Kies een optie: "))
            if choice in range(0,7):
                return choice
            else:
                print(INVALID_INPUT)
        except ValueError:
            print(INVALID_INPUT)


def show_welcome_message():
    print(f"""
{CASINO_NAME} - Speluitleg
{SEPARATOR}
Welkom aan de roulettetafel.

Het doel van roulette is om te voorspellen waar het balletje zal landen.
Kies waarop u wilt inzetten en bepaal vervolgens uw inzet.
Het balletje kan op één van de 37 getallen van 0 tot en met 36 landen.
In het overzicht ziet u per keuze hoeveel winst u kunt behalen.
""")

def select_number():
        while True:
            try:
                number = int(input("Op welk nummer wilt u inzetten? (0 t/m 36) "))
                if 0 <= number <= 36:
                    break
                else:
                    print(INVALID_INPUT)
            except ValueError:
                print(INVALID_INPUT)
        return number


def quit_action():
    print(f"""
U heeft gekozen om het spel te stoppen.
Wat wilt u doen?

1. Blijven spelen
2. Stake wijzigen
3. Spel wijzigen
0. Terug naar hoofdmenu
{SEPARATOR}""")
    try:
        choice = int(input(f"Kies een optie: "))
        if choice in range(0, 4):
            if choice == 1:
                blank_lines(2)
                action = "continue"
            elif choice == 2:
                blank_lines(2)
                action = "change_stake"
            elif choice == 3:
                action = "choose_game"
            else:
                action = "main_menu"
            return action
        else:
            print(INVALID_INPUT)
    except ValueError:
        print(INVALID_INPUT)


def determine_color_and_parity(spin_result):
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

    return color, parity


def show_spin_result(spin_result, color):
    print("Het balletje wordt gerold...")
    time.sleep(1)
    print("...")
    time.sleep(1)
    print(f"Het balletje is geland op {spin_result} {color}!")
    time.sleep(1)
    print()


def determine_win(playing_balance, choice, color, parity, number, spin_result, stake):
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

    return playing_balance


def round_options(playing_balance, action, stake, number, choice):
    action = None
    try:
        while True:
            print(f"""
            Kies uit één van de volgende opties:
        
            1. Opnieuw spelen met dezelfde keuze en inzet
            2. Keuze aanpassen
            3. Inzet aanpassen
            4. Keuze en inzet aanpassen
        
            0. stoppen
            {SEPARATOR}
            """)

            round_choice = int(input("Kies een optie: "))
            if round_choice in range(0, 5):
                if round_choice == 0:
                    action = quit_action()
                elif round_choice == 1:
                    action = "continue"
                else:
                    if round_choice in (3, 4):
                        stake = new_stake(playing_balance)
                    if round_choice in (2, 4):
                        number = None
                        choice = get_gamble_choice()
                return action, stake, number, choice
            else:
                print(INVALID_INPUT)


    except ValueError:
        print(INVALID_INPUT)


def play(playing_balance):
    show_welcome_message()
    number = None
    action = None
    choice = None

    while True:
        stake, playing_balance, action = new_stake(playing_balance)

        if action == 'continue':
            while True:
                choice = get_gamble_choice()
                if choice == 0:
                    action = quit_action()
                if choice == 6 and number is None:
                    number = select_number()
                break

        if action in ("choose_game","main_menu"):
            break

        while True:
            if (playing_balance - stake) < stake:
                    playing_balance, action = stake_to_high(stake, playing_balance)
                    if action == "change_stake":
                        stake = new_stake(playing_balance)
                        continue
                    elif action != "continue":
                        break
                    else:
                        playing_balance -= stake
                        spin_result = random.randint(0, 36)
                        color, parity = determine_color_and_parity(spin_result)
                        show_spin_result(spin_result, color)
                        playing_balance = determine_win(playing_balance, choice, color, parity, number, spin_result, stake)
                        action, stake, number, choice = round_options(playing_balance, action, stake, number, choice)
                        if action == 'continue':
                            continue
                        elif action == 'change_stake':
                            stake = new_stake(playing_balance)
                            continue
                        else:
                            break

    return playing_balance, action
import main
from utils import blank_lines
from utils import format_currency
import time
import random

SEPARATOR = '-' * 50
CASINO_NAME = "Casino de Gouden Driehoek"
INVALID_INPUT = "\nOngeldige invoer. Probeer het opnieuw.\n"


def stake_to_high(playing_balance):
    while True:
        print(f"""Uw saldo is ontoereikend voor deze inzet.
{SEPARATOR}
Keuze opties: 

1. Inzet wijzigen
2. Saldo wijzigen
0. Stoppen
{SEPARATOR}""")
        try:
            choice = int(input(f"Kies een optie: "))
            if 0 <= choice <= 2:
                if choice == 1:
                    print()
                    action = "change_stake"
                elif choice == 2:
                    blank_lines(2)
                    playing_balance, _ = main.show_balance(playing_balance, trigger="roulettetafel")
                    action = "continue"
                else:
                    action = quit_action()
                return playing_balance, action
            else:
                print(INVALID_INPUT)
                continue
        except ValueError:
            print(INVALID_INPUT)


def new_stake(playing_balance):
    while True:
        try:
            action = "continue"
            print(f"Uw huidige saldo bedraagt {format_currency(playing_balance)}.")
            stake = float(input(f"Hoeveel wilt u inzetten? € "))
            if stake > playing_balance or stake <= 0:
                if stake <= 0:
                    print()
                    print("De inzet moet hoger zijn dan €0.")
                    print()
                    continue
                else:
                    blank_lines(2)
                    playing_balance, action = stake_to_high(playing_balance)
                    if action == "change_stake":
                        continue
            else:
                print()
                input("Uw inzet is geaccepteerd. Druk op enter om verder te gaan.")
                blank_lines(2)
            return stake, playing_balance, action
        except ValueError:
            print(INVALID_INPUT)


def get_gamble_choice():
    while True:
        print(f"""{CASINO_NAME} - Inzetmogelijkheden
{SEPARATOR}
1. Rood   - winst: 1x inzet
2. Zwart  - winst: 1x inzet
3. Groen  - winst: 35x inzet
4. Even   - winst: 1x inzet
5. Oneven - winst: 1x inzet
6. Nummer - winst: 35x inzet

0. Stoppen
{SEPARATOR}""")

        try:
            action = "continue"
            choice = int(input("Kies een optie: "))

            if choice in range(0, 7):
                number =  None

                if choice == 6:
                    print()
                    number = select_number()

                elif choice == 0:
                    blank_lines(2)
                    action = quit_action()
                    if action == "continue":
                        continue
                else:
                    blank_lines(2)
                return choice, number, action
            else:
                print(INVALID_INPUT)
        except ValueError:
            print(INVALID_INPUT)


def show_welcome_message():
    print(f"""{CASINO_NAME} - Speluitleg
{SEPARATOR}
Welkom aan de roulettetafel.

Het doel van roulette is om te voorspellen waar het balletje zal landen.
Kies waarop u wilt inzetten en bepaal vervolgens uw inzet.
Het balletje kan op een vakje met één van de getallen van 0 tot en met 36 landen.
Ieder vakje heeft ook zijn eigen kleur. Dit kan rood, zwart of groen zijn.
In het keuze-overzicht ziet u per optie hoeveel winst u kunt behalen.
{SEPARATOR}
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
    print(f"""U heeft gekozen om het spel te stoppen.
{SEPARATOR}
1. Toch verder spelen
2. Inzet aanpassen en verder spelen
3. Een ander spel kiezen
0. Terug naar het hoofdmenu
{SEPARATOR}""")
    while True:    
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
                continue
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
    print("De croupier rolt het balletje. Veel geluk!")
    time.sleep(1)
    print("...")
    time.sleep(1)
    print("Rien ne va plus!")
    time.sleep(1)
    print("...")
    time.sleep(1)
    print(f"Het balletje is geland op {spin_result} {color}.")
    print(SEPARATOR)
    time.sleep(1)


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
        print(f"Gefeliciteerd, u wint {format_currency(gain)}!")
    else:
        print(f"Helaas, u verliest uw inzet.")
    print()
    print(f"Uw nieuwe saldo is {format_currency(playing_balance)}.")
    print()
    input("Druk op Enter om verder te gaan.")
    blank_lines(2)

    return playing_balance

def choice_to_text(choice):
    match choice:
        case 1:
            choice_text = "Rood"
        case 2:
            choice_text = "Zwart"
        case 3:
            choice_text = "Groen"
        case 4:
            choice_text = "Even"
        case 5:
            choice_text = "Oneven"
        case 6:
            choice_text = "Nummer"
        case _:
            choice_text = "Onbekend"

    return choice_text


def confirm_bet(playing_balance, stake, number, choice):
    action = None
    while True:
        choice_text = choice_to_text(choice)
        print(f"""Uw huidige inzet is:
{SEPARATOR}
Inzet:      {format_currency(stake)}    
Keuze:      {choice_text}""")
        if choice == 6:
            print(f"Nummer:     {number}")
        print(SEPARATOR)
        print(f"""
Wat wilt u doen?
{SEPARATOR}
1. Spelen met huidige inzet en keuze
2. Keuze aanpassen
3. Inzet aanpassen
4. Keuze en inzet aanpassen

0. stoppen
{SEPARATOR}""")
        try:
            round_choice = int(input("Kies een optie: "))
            if round_choice in range(0, 5):
                if round_choice == 0:
                    blank_lines(2)
                    action = quit_action()
                    if action == "continue":
                        continue
                    elif action == "change_stake":
                        stake, playing_balance, action = new_stake(playing_balance)
                        if action == "continue":
                            continue
                elif round_choice == 1:
                    blank_lines(2)
                    action = "continue"
                elif round_choice == 2:
                    number = None
                    blank_lines(2)
                    choice, number, action = get_gamble_choice()
                    if action == "continue":
                        continue
                    elif action == "change_stake":
                        stake, playing_balance, action = new_stake(playing_balance)
                        choice, number, action = get_gamble_choice()
                        continue
                elif round_choice == 3:
                    print()
                    stake, playing_balance, action = new_stake(playing_balance)
                    if action in ("continue", "change_stake"):
                        continue
                else:
                    number = None
                    blank_lines(2)
                    stake, playing_balance, action = new_stake(playing_balance)
                    if action in ("choose_game", "main_menu"):
                        return action, stake, number, choice, playing_balance
                    choice, number, action = get_gamble_choice()
                    if action == "continue":
                        continue
                    elif action == "change_stake":
                        stake, playing_balance, action = new_stake(playing_balance)
                        choice, number, action = get_gamble_choice()
                        continue
            else:
                print(INVALID_INPUT)
                time.sleep(1)
                continue
        except ValueError:
            print(INVALID_INPUT)
            time.sleep(1)
            continue
        return action, stake, number, choice, playing_balance

def play(playing_balance):
    show_welcome_message()
    choice = None
    number = None

    while True:
        stake, playing_balance, action = new_stake(playing_balance)
        if action == "continue":
            choice, number, action = get_gamble_choice()
        if action == "change_stake":
            continue
        if action in ("continue", "choose_game", "main_menu"):
            break

    if action == "continue":
        while True:
            action, stake, number, choice, playing_balance = confirm_bet(playing_balance, stake, number, choice)

            if action in ("choose_game", "main_menu"):
                break

            if playing_balance < stake:
                playing_balance, action = stake_to_high(playing_balance)
                if action == "change_stake":
                    stake, playing_balance, action  = new_stake(playing_balance)
                    continue
                elif action == "continue":
                    continue



            playing_balance -= stake
            spin_result = random.randint(0, 36)
            color, parity = determine_color_and_parity(spin_result)
            show_spin_result(spin_result, color)
            playing_balance = determine_win(playing_balance, choice, color, parity, number, spin_result, stake)
            if action == 'continue':
                continue
            elif action == 'change_stake':
                stake, playing_balance, action  = new_stake(playing_balance)
                continue
            else:
                break
    return playing_balance, action
# ==============================
# FUNCTION IMPORTS
# ==============================

import os
import requests
from dotenv import load_dotenv

from rich.console import Console

from utils.utils import (
    format_currency,
    print_message,
    get_input,
    display_page,
    display_panel,
)


# ==============================
# CONSTANTS
# ==============================

from utils.constants import (
    CASINO_NAME,
    CONTINUE_PROMPT,
    INVALID_INPUT,
)


# ==============================
# CONFIGURATION
# ==============================

console = Console(width=80)


# ==============================
# USER INPUT
# ==============================

def show_page(current_user):
    """
    Displays the exchange office and requests the currency and amount to exchange.

    Args:
        current_user (dict): The profile of the current user.

    Returns:
        tuple: The selected currency and exchange amount,
        or ("STOP", None) when the user cancels.
    """
    exchange_amount = 0.0

    page_content = f"""U kunt hier buitenlandse valuta wisselen voor euro's. 
Uw huidige saldo bedraagt {format_currency(current_user["playing_balance"])}"""

    display_page(
        location=CASINO_NAME,
        title="Wisselkantoor",
        content=page_content
    )

    while True:
        currency = get_input(
            "Welke valuta wilt u wisselen? Gebruik een ISO 4217-valutacode (bijv. USD): "
        ).upper()

        if currency.isalpha() and len(currency) == 3:
            break

        if currency == "STOP":
            return currency, None

        print_message(INVALID_INPUT, "red")

    while True:
        try:
            exchange_amount = round(
                float(get_input(f"Vul het bedrag in dat u wilt wisselen: {currency} ")), 2
            )
        except ValueError:
            print_message(INVALID_INPUT, "red")
            continue

        if exchange_amount > 0:
            break

        print_message(INVALID_INPUT, "red")

    print()

    return currency, exchange_amount


# ==============================
# EXCHANGE RATE AND CONVERSION
# ==============================

def get_exchange_rate(api_key, currency):
    """
    Retrieves the current exchange rate from the selected currency to euros.

    Args:
        api_key (str): The API key for the ExchangeRate-API service.
        currency (str): The ISO 4217 currency code to exchange.

    Returns:
        float or None: The exchange rate to euros,
        or None when the request fails.
    """
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{currency}"

    try:
        response = requests.get(url, timeout=10)

    except requests.exceptions.ConnectionError:
        print_message("Fout: kan geen verbinding maken met de wisselkoersservice.", "red")
        return None

    except requests.exceptions.Timeout:
        print_message("Fout: de wisselkoersservice reageert niet op tijd.", "red")
        return None

    if response.ok:
        data = response.json()

        if "EUR" in data.get("conversion_rates", {}):
            return float(data["conversion_rates"]["EUR"])

        else:
            print_message(f"Fout: {currency} wisselkoers niet gevonden.", "red")
            return None

    else:
        print_message(f"Fout: {response.status_code} - {response.text}", "red")
        return None


def convert_currency(currency_amount, exchange_rate):
    """
    Converts an amount of foreign currency to euros.

    Args:
        currency_amount (float): The amount of foreign currency.
        exchange_rate (float): The exchange rate to euros.

    Returns:
        float: The converted euro amount rounded to two decimals.
    """
    return round(currency_amount * exchange_rate, 2)


# ==============================
# OUTPUT
# ==============================

def show_exchange_details(current_user, currency, currency_amount, exchange_rate, euro_amount):
    """
    Displays the exchange transaction details and updated playing balance.

    Args:
        current_user (dict): The profile of the current user.
        currency (str): The original currency code.
        currency_amount (float): The original amount exchanged.
        exchange_rate (float): The exchange rate to euros.
        euro_amount (float): The converted amount in euros.
    """
    content = f"""Bedrag: {currency} {f"{currency_amount:.2f}".replace(".", ",")}
Wisselkoers naar euro: {exchange_rate}
Euro's: {format_currency(euro_amount)}

Nieuw saldo: {format_currency(current_user["playing_balance"])}"""

    display_panel(content, title="Wisselkassa")

    get_input(CONTINUE_PROMPT)


# ==============================
# PROGRAM FLOW
# ==============================

def run_exchange(current_user):
    """
    Controls the exchange office process and updates the player's balance.

    Loads the API key, requests the currency and amount, retrieves the
    exchange rate, converts the amount and displays the transaction.

    Args:
        current_user (dict): The profile of the current user.

    Returns:
        dict: The current user profile with the updated playing balance
        when an exchange is completed.
    """
    load_dotenv()
    api_key = os.getenv("API_KEY")

    if not api_key:
        print_message("Fout: geen API Key gevonden", "red")
        print()
        get_input("Druk op Enter om terug te keren naar de lobby")

        return current_user

    currency, currency_amount = show_page(current_user)

    if currency == "STOP":
        print()
        get_input("Druk op Enter om terug te keren naar de lobby")
        return current_user

    exchange_rate = get_exchange_rate(api_key, currency)

    if exchange_rate is None:
        print()
        get_input("Druk op Enter om terug te keren naar de lobby")

        return current_user

    euro_amount = convert_currency(currency_amount, exchange_rate)
    current_user["playing_balance"] = round(current_user["playing_balance"] + euro_amount, 2)

    show_exchange_details(current_user, currency, currency_amount, exchange_rate, euro_amount)

    return current_user
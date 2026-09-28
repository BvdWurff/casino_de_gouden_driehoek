def blank_lines(number):
    print("\n" * number, end="")

def format_currency(amount):
    if round(amount % 1, 2) ==0:
        return f"€{int(amount)},-"
    else:
        return f"€{amount:.2f}".replace(".", ",")
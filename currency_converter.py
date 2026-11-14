"""Console Currency Converter.

Converts an amount between INR, USD, EUR and GBP.
Every conversion goes through INR (amount -> INR -> target currency),
and every result is rounded to 2 decimal places.

Run:  python3 currency_converter.py
"""

from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

# Exchange rates: value of 1 unit of each currency in INR.
# Adding a new currency only needs one more entry here.
RATES_TO_INR = {
    "INR": Decimal("1"),
    "USD": Decimal("83"),
    "EUR": Decimal("90"),
    "GBP": Decimal("105"),
}

TWO_PLACES = Decimal("0.01")


def round_2dp(value):
    """Round to 2 decimal places (normal school-style rounding: 0.005 -> 0.01)."""
    return value.quantize(TWO_PLACES, rounding=ROUND_HALF_UP)


def convert_to_inr(amount, currency):
    """Step 1: convert an amount in `currency` into INR."""
    return amount * RATES_TO_INR[currency]


def convert_currency(amount, from_currency, to_currency):
    """Convert `amount` between any two supported currencies, via INR."""
    if from_currency == to_currency:
        return round_2dp(amount)
    inr_value = convert_to_inr(amount, from_currency)  # Step 1: to INR
    converted = inr_value / RATES_TO_INR[to_currency]  # Step 2: INR to target
    return round_2dp(converted)


def validate_currency(code):
    """Return an error message if the code is unsupported, otherwise None."""
    if code not in RATES_TO_INR:
        available = ", ".join(RATES_TO_INR)
        return f"Unsupported currency '{code}'. Available: {available}"
    return None


def parse_amount(text):
    """Validate the amount. Returns (amount, error); exactly one is None."""
    try:
        amount = Decimal(text)
    except InvalidOperation:
        return None, "Invalid amount. Enter a number."
    if not amount.is_finite():  # rejects 'nan' and 'inf'
        return None, "Invalid amount. Enter a number."
    if amount < 0:
        return None, "Amount cannot be negative."
    return amount, None


def format_amount(amount):
    """Show the amount as typed, without useless zeros (100 not 100.00)."""
    text = format(amount, "f")
    if "." in text:
        text = text.rstrip("0").rstrip(".")
    return text


def read_conversion():
    """Ask the user for the inputs. Returns (amount, from, to) or None on error."""
    amount, error = parse_amount(input("Amount: ").strip())
    if error:
        print(error)
        return None

    from_currency = input("From: ").strip().upper()
    error = validate_currency(from_currency)
    if error:
        print(error)
        return None

    to_currency = input("To: ").strip().upper()
    error = validate_currency(to_currency)
    if error:
        print(error)
        return None

    return amount, from_currency, to_currency


def main():
    print("=== Currency Converter ===")
    print("Supported currencies:", ", ".join(RATES_TO_INR))

    while True:
        conversion = read_conversion()
        if conversion:
            amount, from_currency, to_currency = conversion
            result = convert_currency(amount, from_currency, to_currency)
            print(f"{format_amount(amount)} {from_currency} = {result} {to_currency}")

        try:
            again = input("Convert another? (y/n): ").strip().lower()
        except EOFError:  # input finished (e.g. piped test input)
            break
        if again != "y":
            break


if __name__ == "__main__":
    main()

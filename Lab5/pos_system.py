"""Retail POS system with checkout, promotions, and receipt logging."""

import re
import secrets

price_list = {
    "pen": 10,
    "notebook": 45,
    "bag": 799,
    "bottle": 150,
}

sales_state = {"total": 0.0}
receipt_lines = []


def process_checkout(cart_items, tax_rate=0.05, receipts=None):
    """Calculate a bill, update sales, and record a receipt."""
    if receipts is None:
        receipts = []

    if not 0 <= tax_rate <= 1:
        raise ValueError("Tax rate must be between 0 and 1.")

    subtotal = 0.0

    for item, quantity in cart_items:
        if item not in price_list:
            continue

        if not isinstance(quantity, int) or quantity <= 0:
            continue

        subtotal += price_list[item] * quantity

    total = subtotal + subtotal * tax_rate
    receipts.append(total)
    sales_state["total"] += total

    receipt_number = secrets.randbelow(9000) + 1000
    receipt_lines.append(
        f"Receipt #{receipt_number} total={total:.2f}"
    )

    return total


def apply_promo_code(code_str):
    """Apply a basic arithmetic promotion to the total sales amount."""
    pattern = r"^\s*total\s*([+\-*/])\s*(\d+(?:\.\d+)?)\s*$"
    match = re.fullmatch(pattern, code_str)

    if match is None:
        raise ValueError(
            "Invalid promo code. Use formats such as "
            "'total * 0.9' or 'total - 50'."
        )

    operator, value_text = match.groups()
    value = float(value_text)
    total = sales_state["total"]

    if operator == "+":
        return total + value

    if operator == "-":
        return total - value

    if operator == "*":
        return total * value

    if operator == "/":
        if value == 0:
            raise ValueError("Cannot divide by zero.")
        return total / value

    raise ValueError("Unsupported promotion operator.")


def update_stock(item, qty):
    """Validate a stock update request for a known product."""
    if item not in price_list:
        print(f"Cannot update stock: unknown item '{item}'.")
        return

    if not isinstance(qty, int) or qty <= 0:
        print("Stock quantity must be a positive integer.")
        return

    print(f"Stock update requested for {item}: {qty} units.")


def save_receipt_log(file_path="pos_log.txt"):
    """Append recorded receipts to a UTF-8 text file."""
    with open(file_path, "a", encoding="utf-8") as receipt_file:
        for line in receipt_lines:
            receipt_file.write(f"{line}\n")


def print_sales():
    """Display the total sales recorded so far."""
    print(f"Sales so far: {sales_state['total']:.2f}")


def main():
    """Run sample checkout transactions and demonstrate promotions."""
    print(
        "Bill 1:",
        process_checkout([("pen", 3), ("notebook", 2)]),
    )
    print(
        "Bill 2:",
        process_checkout([("bag", 1), ("laptop", 1)]),
    )
    print(
        "Bill 3:",
        process_checkout([("bottle", -4)]),
    )
    print(
        "Bill 4:",
        process_checkout([("pen", 2)]),
    )

    update_stock("laptop", 5)

    try:
        print("After promo:", apply_promo_code("total * 0.9"))
        code = input(
            "Enter promo code (e.g. total - 50): "
        ).strip() or "total - 50"
        print("After your promo:", apply_promo_code(code))
    except ValueError as error:
        print(f"Promotion error: {error}")

    save_receipt_log()
    print_sales()


if __name__ == "__main__":
    main()

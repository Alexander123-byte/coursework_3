import json


def mask_card_number(card_number):
    return f"{card_number[:4]} {' '.join(['*' * 4] * (len(card_number) // 4 - 1))} {card_number[-4:]}"


def mask_account_number(account_number):
    return f"**{account_number[-4:]}"


def format_transaction(transaction):
    date = transaction.get('date', 'N/A')
    description = transaction.get('description', 'N/A')
    from_account = mask_card_number(transaction.get('from', ''))
    to_account = mask_account_number(transaction.get('to', ''))
    amount, currency = transaction.get('operationAmount', '0.00 USD').split()
    return f"{date} {description}\n{from_account} -> {to_account}\n{amount} {currency}\n"


def get_last_transactions(transactions, count=5):
    try:
        executed_transactions = [t for t in transactions if t.get('status') == 'EXECUTED']
        last_transactions = sorted(executed_transactions, key=lambda t: t.get('date', '0'), reverse=True)[:count]

        result = ""
        for transaction in last_transactions:
            result += format_transaction(transaction) + "\n"

        return result
    except (TypeError, KeyError, ValueError) as e:
        return f"Error processing data: {e}"


if __name__ == "__main__":
    try:
        with open('operations.json', 'r', encoding='utf-8') as file:
            data = json.load(file)

        result = get_last_transactions(data)
        print(result)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")

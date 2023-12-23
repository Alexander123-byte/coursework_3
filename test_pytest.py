import json
import pytest
from application1 import mask_card_number, mask_account_number, format_transaction, get_last_transactions

sample_data = [
    {
        "date": "2023-01-01",
        "status": "EXECUTED",
        "description": "Purchase",
        "from": "1234567890123456",
        "to": "9876543210123456",
        "operationAmount": "100.00 USD"
    },
    {
        "date": "2023-01-02",
        "status": "EXECUTED",
        "description": "Transfer",
        "from": "1111222233334444",
        "to": "5555666677778888",
        "operationAmount": "50.00 EUR"
    },
    {
        "date": "2023-01-03",
        "status": "CANCELED",
        "description": "Withdrawal",
        "from": "8888777766665555",
        "to": "4444333322221111",
        "operationAmount": "200.00 GBP"
    },
]


def test_mask_card_number():
    assert mask_card_number("1234567890123456") == "1234 **** **** 3456"
    assert mask_card_number("1111222233334444") == "1111 **** **** 4444"


def test_mask_account_number():
    assert mask_account_number("9876543210123456") == "**3456"
    assert mask_account_number("5555666677778888") == "**8888"


def test_format_transactions():
    transaction = {"date": "2023-01-01", "description": "Purchase", "from": "1234567890123456", "to": "9876543210123456", "operationAmount": "100.00 USD"}
    expected_output = "2023-01-01 Purchase\n1234 **** **** 3456 -> **3456\n100.00 USD\n"
    assert format_transaction(transaction) == expected_output


def test_get_last_transactions():
    result = get_last_transactions(sample_data, count=2)
    expected_output = (
        "2023-01-02 Transfer\n1111 **** **** 4444 -> **8888\n50.00 EUR\n"
        "2023-01-01 Purchase\n1234 **** **** 3456 -> **3456\n100.00 USD\n"
    )
    assert result == expected_output


def test_get_last_transactions_with_invalid_data():
    invalid_data = [
        {"date": "2023-01-01", "status": "EXECUTED", "operationAmount": "invalid_amount"},
        {"date": "2023-01-02", "status": "EXECUTED", "operationAmount": "50.00 EUR"}
    ]
    with pytest.raises(ValueError):
        get_last_transactions(invalid_data)


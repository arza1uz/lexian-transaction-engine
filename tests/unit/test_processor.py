import pandas as pd

from lexian_transaction_engine.processor import calculate_balances


def test_calculate_balances_applies_deposits_and_withdrawals():
    transactions = pd.DataFrame(
        {
            "transaction_id": [1, 2, 3],
            "user_id": ["U001", "U001", "U002"],
            "timestamp": [
                "2026-01-01T10:00:00",
                "2026-01-01T10:30:00",
                "2026-01-01T11:15:00",
            ],
            "type": ["deposit", "withdrawal", "deposit"],
            "amount": [1000, 250, 500],
        }
    )

    balances = calculate_balances(transactions)

    assert balances.to_dict("records") == [
        {"user_id": "U001", "balance": 750},
        {"user_id": "U002", "balance": 500},
    ]

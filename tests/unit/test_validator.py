import pandas as pd
import pytest

from lexian_transaction_engine.validator import validate_transactions


def valid_transactions() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "transaction_id": [1, 2],
            "user_id": ["U001", "U001"],
            "timestamp": ["2026-01-01T10:00:00", "2026-01-01T10:30:00"],
            "type": ["deposit", "withdrawal"],
            "amount": [1000, 250],
        }
    )


def test_validate_transactions_requires_columns():
    transactions = valid_transactions().drop(columns=["amount"])

    with pytest.raises(ValueError, match="Missing required columns: amount"):
        validate_transactions(transactions)


def test_validate_transactions_rejects_duplicate_transaction_ids():
    transactions = valid_transactions()
    transactions.loc[1, "transaction_id"] = 1

    with pytest.raises(ValueError, match="Duplicate transaction IDs: 1"):
        validate_transactions(transactions)


def test_validate_transactions_rejects_unsupported_transaction_type():
    transactions = valid_transactions()
    transactions.loc[0, "type"] = "cashback"

    with pytest.raises(ValueError, match="Unsupported transaction types: cashback"):
        validate_transactions(transactions)


def test_validate_transactions_rejects_non_numeric_amount():
    transactions = valid_transactions()
    transactions["amount"] = transactions["amount"].astype(object)
    transactions.loc[0, "amount"] = "not-a-number"

    with pytest.raises(ValueError, match="Non-numeric amount values"):
        validate_transactions(transactions)


def test_validate_transactions_rejects_negative_amount():
    transactions = valid_transactions()
    transactions.loc[0, "amount"] = -100

    with pytest.raises(ValueError, match="Amounts must be greater than zero"):
        validate_transactions(transactions)

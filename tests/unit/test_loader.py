from pathlib import Path

from lexian_transaction_engine.loader import load_transactions


def test_load_transactions_reads_csv():
    transactions = load_transactions(Path("data/raw/transactions.csv"))

    assert len(transactions) == 10
    assert list(transactions.columns) == [
        "transaction_id",
        "user_id",
        "timestamp",
        "type",
        "amount",
    ]

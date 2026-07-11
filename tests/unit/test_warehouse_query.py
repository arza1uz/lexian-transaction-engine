from datetime import UTC, datetime
from pathlib import Path

import pandas as pd
import pytest

from lexian_transaction_engine.warehouse import (
    connect_warehouse,
    create_schema,
    execute_query,
    load_query,
    write_fact_transactions,
)


def test_load_query_reads_sql_file() -> None:
    query = load_query("user_balances.sql")

    assert "SELECT" in query
    assert "fact_transactions" in query


def test_load_query_raises_for_missing_file() -> None:
    with pytest.raises(FileNotFoundError):
        load_query("missing_query.sql")


def test_execute_query_returns_rows(tmp_path: Path) -> None:
    connection = connect_warehouse(tmp_path / "test.duckdb")

    try:
        create_schema(connection)

        transactions = pd.DataFrame(
            [
                {
                    "execution_id": "exec_001",
                    "transaction_id": "txn_001",
                    "user_id": "usr_001",
                    "transaction_timestamp": datetime(2026, 1, 1, tzinfo=UTC),
                    "transaction_type": "deposit",
                    "amount": 100.00,
                    "signed_amount": 100.00,
                },
                {
                    "execution_id": "exec_001",
                    "transaction_id": "txn_002",
                    "user_id": "usr_001",
                    "transaction_timestamp": datetime(2026, 1, 2, tzinfo=UTC),
                    "transaction_type": "withdrawal",
                    "amount": 25.00,
                    "signed_amount": -25.00,
                },
            ]
        )

        write_fact_transactions(connection, transactions)

        rows = execute_query(connection, "user_balances.sql")

        assert rows == [("usr_001", 75.00)]
    finally:
        connection.close()

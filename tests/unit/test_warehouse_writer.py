from datetime import UTC, datetime
from pathlib import Path

import pandas as pd
import pytest

from lexian_transaction_engine.warehouse import connect_warehouse, create_schema
from lexian_transaction_engine.warehouse.writer import (
    MissingColumnsError,
    write_fact_transactions,
    write_pipeline_executions,
    write_raw_transactions,
    write_user_balances,
)


def test_write_raw_transactions_inserts_rows(tmp_path: Path) -> None:
    connection = connect_warehouse(tmp_path / "test.duckdb")

    try:
        create_schema(connection)

        dataframe = pd.DataFrame(
            [
                {
                    "execution_id": "exec_001",
                    "source_file": "transactions.csv",
                    "source_row_number": 1,
                    "transaction_id": "txn_001",
                    "user_id": "usr_001",
                    "transaction_timestamp_raw": "2026-01-01T10:00:00",
                    "transaction_type": "deposit",
                    "amount_raw": "100.00",
                }
            ]
        )

        rows_written = write_raw_transactions(connection, dataframe)
        result = connection.execute(
            "SELECT COUNT(*) FROM raw_transactions"
        ).fetchone()

        assert rows_written == 1
        assert result == (1,)
    finally:
        connection.close()


def test_write_fact_transactions_inserts_rows(tmp_path: Path) -> None:
    connection = connect_warehouse(tmp_path / "test.duckdb")

    try:
        create_schema(connection)

        dataframe = pd.DataFrame(
            [
                {
                    "execution_id": "exec_001",
                    "transaction_id": "txn_001",
                    "user_id": "usr_001",
                    "transaction_timestamp": datetime(2026, 1, 1, tzinfo=UTC),
                    "transaction_type": "deposit",
                    "amount": 100.00,
                    "signed_amount": 100.00,
                }
            ]
        )

        rows_written = write_fact_transactions(connection, dataframe)
        result = connection.execute(
            "SELECT SUM(signed_amount) FROM fact_transactions"
        ).fetchone()

        assert rows_written == 1
        assert result == (100.00,)
    finally:
        connection.close()


def test_write_user_balances_inserts_rows(tmp_path: Path) -> None:
    connection = connect_warehouse(tmp_path / "test.duckdb")

    try:
        create_schema(connection)

        dataframe = pd.DataFrame(
            [
                {
                    "execution_id": "exec_001",
                    "user_id": "usr_001",
                    "balance": 100.00,
                }
            ]
        )

        rows_written = write_user_balances(connection, dataframe)
        result = connection.execute(
            "SELECT balance FROM fact_user_balances"
        ).fetchone()

        assert rows_written == 1
        assert result == (100.00,)
    finally:
        connection.close()


def test_write_pipeline_executions_inserts_rows(tmp_path: Path) -> None:
    connection = connect_warehouse(tmp_path / "test.duckdb")

    try:
        create_schema(connection)

        dataframe = pd.DataFrame(
            [
                {
                    "execution_id": "exec_001",
                    "started_at": datetime(2026, 1, 1, 10, 0, tzinfo=UTC),
                    "finished_at": datetime(2026, 1, 1, 10, 1, tzinfo=UTC),
                    "duration_seconds": 60.0,
                    "status": "succeeded",
                    "rows_read": 10,
                    "rows_valid": 9,
                    "rows_invalid": 1,
                    "rows_processed": 9,
                    "input_path": "data/raw/transactions.csv",
                    "output_path": "data/reports/balances.csv",
                    "error_message": None,
                }
            ]
        )

        rows_written = write_pipeline_executions(connection, dataframe)
        result = connection.execute(
            "SELECT status, rows_processed FROM fact_pipeline_executions"
        ).fetchone()

        assert rows_written == 1
        assert result == ("succeeded", 9)
    finally:
        connection.close()


def test_writer_raises_error_when_required_columns_are_missing(
    tmp_path: Path,
) -> None:
    connection = connect_warehouse(tmp_path / "test.duckdb")

    try:
        create_schema(connection)

        dataframe = pd.DataFrame(
            [
                {
                    "execution_id": "exec_001",
                    "transaction_id": "txn_001",
                }
            ]
        )

        with pytest.raises(MissingColumnsError):
            write_fact_transactions(connection, dataframe)
    finally:
        connection.close()

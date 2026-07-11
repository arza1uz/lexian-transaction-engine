from datetime import UTC, datetime
from pathlib import Path

import pandas as pd

from lexian_transaction_engine.warehouse import (
    connect_warehouse,
    create_schema,
    execute_query,
    write_fact_transactions,
    write_pipeline_executions,
    write_user_balances,
)


def test_balance_by_user_execution_query(tmp_path: Path) -> None:
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

        rows = execute_query(connection, "balance_by_user_execution.sql")

        assert rows == [("exec_001", "usr_001", 75.00, 2)]
    finally:
        connection.close()


def test_transaction_volume_by_execution_query(tmp_path: Path) -> None:
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

        rows = execute_query(connection, "transaction_volume_by_execution.sql")

        assert rows == [
            ("exec_001", "deposit", 1, 100.00, 100.00),
            ("exec_001", "withdrawal", 1, 25.00, -25.00),
        ]
    finally:
        connection.close()


def test_pipeline_health_summary_query(tmp_path: Path) -> None:
    connection = connect_warehouse(tmp_path / "test.duckdb")

    try:
        create_schema(connection)

        executions = pd.DataFrame(
            [
                {
                    "execution_id": "exec_001",
                    "started_at": datetime(2026, 1, 1, 10, 0, tzinfo=UTC),
                    "finished_at": datetime(2026, 1, 1, 10, 1, tzinfo=UTC),
                    "duration_seconds": 60.0,
                    "status": "succeeded",
                    "rows_read": 10,
                    "rows_valid": 8,
                    "rows_invalid": 2,
                    "rows_processed": 8,
                    "input_path": "data/raw/transactions.csv",
                    "output_path": "data/reports/balances.csv",
                    "error_message": None,
                }
            ]
        )

        write_pipeline_executions(connection, executions)

        rows = execute_query(connection, "pipeline_health_summary.sql")

        assert rows == [
            ("exec_001", "succeeded", 10, 8, 2, 8, 80.0, 20.0, 60.0)
        ]
    finally:
        connection.close()


def test_balance_validation_query(tmp_path: Path) -> None:
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
                }
            ]
        )

        balances = pd.DataFrame(
            [
                {
                    "execution_id": "exec_001",
                    "user_id": "usr_001",
                    "balance": 100.00,
                }
            ]
        )

        write_fact_transactions(connection, transactions)
        write_user_balances(connection, balances)

        rows = execute_query(connection, "balance_validation.sql")

        assert rows == [("exec_001", "usr_001", 100.00, 100.00, 0.00, "matched")]
    finally:
        connection.close()


def test_data_quality_anomalies_query(tmp_path: Path) -> None:
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
                    "transaction_type": "refund",
                    "amount": 100.00,
                    "signed_amount": 100.00,
                }
            ]
        )

        write_fact_transactions(connection, transactions)

        rows = execute_query(connection, "data_quality_anomalies.sql")

        assert rows == [
            (
                "unsupported_transaction_type",
                "exec_001",
                "txn_001",
                "usr_001",
                "refund",
                100.00,
            )
        ]
    finally:
        connection.close()

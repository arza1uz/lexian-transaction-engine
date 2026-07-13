from datetime import UTC, datetime
from pathlib import Path

import pandas as pd

from lexian_transaction_engine.analytics import build_all_marts, load_mart_sql
from lexian_transaction_engine.warehouse import (
    connect_warehouse,
    create_schema,
    write_fact_transactions,
    write_pipeline_executions,
    write_raw_transactions,
    write_user_balances,
)


def seed_analytics_warehouse(database_path: Path):
    connection = connect_warehouse(database_path)
    create_schema(connection)

    raw_transactions = pd.DataFrame(
        [
            {
                "execution_id": "exec_001",
                "source_file": "data/raw/transactions.csv",
                "source_row_number": 1,
                "transaction_id": "txn_001",
                "user_id": "usr_001",
                "transaction_timestamp_raw": "2026-01-01T10:00:00",
                "transaction_type": "deposit",
                "amount_raw": "100.00",
            },
            {
                "execution_id": "exec_001",
                "source_file": "data/raw/transactions.csv",
                "source_row_number": 2,
                "transaction_id": "txn_002",
                "user_id": "usr_001",
                "transaction_timestamp_raw": "2026-01-01T11:00:00",
                "transaction_type": "withdrawal",
                "amount_raw": "25.00",
            },
            {
                "execution_id": "exec_001",
                "source_file": "data/raw/transactions.csv",
                "source_row_number": 3,
                "transaction_id": "txn_003",
                "user_id": "usr_002",
                "transaction_timestamp_raw": "2026-01-01T12:00:00",
                "transaction_type": "deposit",
                "amount_raw": "50.00",
            },
        ]
    )

    fact_transactions = pd.DataFrame(
        [
            {
                "execution_id": "exec_001",
                "transaction_id": "txn_001",
                "user_id": "usr_001",
                "transaction_timestamp": datetime(2026, 1, 1, 10, 0, tzinfo=UTC),
                "transaction_type": "deposit",
                "amount": 100.00,
                "signed_amount": 100.00,
            },
            {
                "execution_id": "exec_001",
                "transaction_id": "txn_002",
                "user_id": "usr_001",
                "transaction_timestamp": datetime(2026, 1, 1, 11, 0, tzinfo=UTC),
                "transaction_type": "withdrawal",
                "amount": 25.00,
                "signed_amount": -25.00,
            },
            {
                "execution_id": "exec_001",
                "transaction_id": "txn_003",
                "user_id": "usr_002",
                "transaction_timestamp": datetime(2026, 1, 1, 12, 0, tzinfo=UTC),
                "transaction_type": "deposit",
                "amount": 50.00,
                "signed_amount": 50.00,
            },
        ]
    )

    user_balances = pd.DataFrame(
        [
            {
                "execution_id": "exec_001",
                "user_id": "usr_001",
                "balance": 75.00,
            },
            {
                "execution_id": "exec_001",
                "user_id": "usr_002",
                "balance": 65.00,
            },
        ]
    )

    pipeline_executions = pd.DataFrame(
        [
            {
                "execution_id": "exec_001",
                "started_at": datetime(2026, 1, 1, 10, 0, tzinfo=UTC),
                "finished_at": datetime(2026, 1, 1, 10, 1, tzinfo=UTC),
                "duration_seconds": 60.0,
                "status": "succeeded",
                "rows_read": 3,
                "rows_valid": 2,
                "rows_invalid": 1,
                "rows_processed": 3,
                "input_path": "data/raw/transactions.csv",
                "output_path": "data/reports/balances.csv",
                "error_message": None,
            }
        ]
    )

    write_raw_transactions(connection, raw_transactions)
    write_fact_transactions(connection, fact_transactions)
    write_user_balances(connection, user_balances)
    write_pipeline_executions(connection, pipeline_executions)

    return connection


def test_load_mart_sql_reads_mart_file() -> None:
    sql = load_mart_sql("mart_user_balances")

    assert "CREATE OR REPLACE VIEW mart_user_balances" in sql
    assert "fact_user_balances" in sql


def test_build_all_marts_creates_expected_views(tmp_path: Path) -> None:
    connection = seed_analytics_warehouse(tmp_path / "test.duckdb")

    try:
        built_marts = build_all_marts(connection)
        rows = connection.execute(
            """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_type = 'VIEW'
            ORDER BY table_name
            """
        ).fetchall()

        view_names = [row[0] for row in rows]

        assert built_marts == [
            "mart_user_balances",
            "mart_transaction_activity",
            "mart_pipeline_health",
            "mart_balance_validation",
            "mart_data_quality_summary",
        ]
        assert view_names == sorted(built_marts)
    finally:
        connection.close()


def test_mart_user_balances_returns_matched_status(tmp_path: Path) -> None:
    connection = seed_analytics_warehouse(tmp_path / "test.duckdb")

    try:
        build_all_marts(connection)
        rows = connection.execute(
            """
            SELECT validation_status, transaction_count
            FROM mart_user_balances
            WHERE execution_id = 'exec_001' AND user_id = 'usr_001'
            """
        ).fetchall()

        assert rows == [("matched", 2)]
    finally:
        connection.close()


def test_mart_pipeline_health_returns_warning_for_invalid_rows(tmp_path: Path) -> None:
    connection = seed_analytics_warehouse(tmp_path / "test.duckdb")

    try:
        build_all_marts(connection)
        rows = connection.execute(
            """
            SELECT health_status, valid_row_rate_pct, invalid_row_rate_pct
            FROM mart_pipeline_health
            WHERE execution_id = 'exec_001'
            """
        ).fetchall()

        assert rows == [("warning", 66.67, 33.33)]
    finally:
        connection.close()


def test_mart_balance_validation_flags_mismatch(tmp_path: Path) -> None:
    connection = seed_analytics_warehouse(tmp_path / "test.duckdb")

    try:
        build_all_marts(connection)
        rows = connection.execute(
            """
            SELECT validation_status, validation_severity, absolute_difference
            FROM mart_balance_validation
            WHERE execution_id = 'exec_001' AND user_id = 'usr_002'
            """
        ).fetchall()

        assert rows == [("mismatch", "critical", 15.00)]
    finally:
        connection.close()


def test_mart_transaction_activity_aggregates_volume(tmp_path: Path) -> None:
    connection = seed_analytics_warehouse(tmp_path / "test.duckdb")

    try:
        build_all_marts(connection)
        rows = connection.execute(
            """
            SELECT transaction_count, gross_amount, net_amount
            FROM mart_transaction_activity
            WHERE execution_id = 'exec_001'
                AND user_id = 'usr_001'
                AND transaction_type = 'withdrawal'
            """
        ).fetchall()

        assert rows == [(1, 25.00, -25.00)]
    finally:
        connection.close()


def test_mart_data_quality_summary_returns_status(tmp_path: Path) -> None:
    connection = seed_analytics_warehouse(tmp_path / "test.duckdb")

    try:
        build_all_marts(connection)
        rows = connection.execute(
            """
            SELECT raw_row_count, fact_transaction_count, data_quality_status
            FROM mart_data_quality_summary
            WHERE execution_id = 'exec_001'
            """
        ).fetchall()

        assert rows == [(3, 3, "warning")]
    finally:
        connection.close()

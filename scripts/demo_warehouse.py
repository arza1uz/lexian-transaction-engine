from datetime import UTC, datetime
from pathlib import Path

import pandas as pd

from lexian_transaction_engine.warehouse import (
    connect_warehouse,
    create_schema,
    execute_query,
    write_fact_transactions,
    write_pipeline_executions,
    write_raw_transactions,
    write_user_balances,
)

DATABASE_PATH = Path("data/warehouse/lexian_demo.duckdb")


def main() -> None:
    connection = connect_warehouse(DATABASE_PATH)

    try:
        create_schema(connection)

        raw_transactions = pd.DataFrame(
            [
                {
                    "execution_id": "exec_demo_001",
                    "source_file": "data/raw/transactions.csv",
                    "source_row_number": 1,
                    "transaction_id": "txn_001",
                    "user_id": "usr_001",
                    "transaction_timestamp_raw": "2026-01-01T10:00:00",
                    "transaction_type": "deposit",
                    "amount_raw": "100.00",
                },
                {
                    "execution_id": "exec_demo_001",
                    "source_file": "data/raw/transactions.csv",
                    "source_row_number": 2,
                    "transaction_id": "txn_002",
                    "user_id": "usr_001",
                    "transaction_timestamp_raw": "2026-01-02T10:00:00",
                    "transaction_type": "withdrawal",
                    "amount_raw": "25.00",
                },
            ]
        )

        fact_transactions = pd.DataFrame(
            [
                {
                    "execution_id": "exec_demo_001",
                    "transaction_id": "txn_001",
                    "user_id": "usr_001",
                    "transaction_timestamp": datetime(2026, 1, 1, 10, 0, tzinfo=UTC),
                    "transaction_type": "deposit",
                    "amount": 100.00,
                    "signed_amount": 100.00,
                },
                {
                    "execution_id": "exec_demo_001",
                    "transaction_id": "txn_002",
                    "user_id": "usr_001",
                    "transaction_timestamp": datetime(2026, 1, 2, 10, 0, tzinfo=UTC),
                    "transaction_type": "withdrawal",
                    "amount": 25.00,
                    "signed_amount": -25.00,
                },
            ]
        )

        user_balances = pd.DataFrame(
            [
                {
                    "execution_id": "exec_demo_001",
                    "user_id": "usr_001",
                    "balance": 75.00,
                }
            ]
        )

        pipeline_executions = pd.DataFrame(
            [
                {
                    "execution_id": "exec_demo_001",
                    "started_at": datetime(2026, 1, 1, 10, 0, tzinfo=UTC),
                    "finished_at": datetime(2026, 1, 1, 10, 1, tzinfo=UTC),
                    "duration_seconds": 60.0,
                    "status": "succeeded",
                    "rows_read": 2,
                    "rows_valid": 2,
                    "rows_invalid": 0,
                    "rows_processed": 2,
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

        print("User balances:")
        for row in execute_query(connection, "user_balances.sql"):
            print(row)

        print("Transaction summary:")
        for row in execute_query(connection, "transaction_summary.sql"):
            print(row)

        print("Execution summary:")
        for row in execute_query(connection, "execution_summary.sql"):
            print(row)

    finally:
        connection.close()


if __name__ == "__main__":
    main()

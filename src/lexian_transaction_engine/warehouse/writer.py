from collections.abc import Sequence

import duckdb
import pandas as pd

RAW_TRANSACTION_COLUMNS = [
    "execution_id",
    "source_file",
    "source_row_number",
    "transaction_id",
    "user_id",
    "transaction_timestamp_raw",
    "transaction_type",
    "amount_raw",
]

FACT_TRANSACTION_COLUMNS = [
    "execution_id",
    "transaction_id",
    "user_id",
    "transaction_timestamp",
    "transaction_type",
    "amount",
    "signed_amount",
]

USER_BALANCE_COLUMNS = [
    "execution_id",
    "user_id",
    "balance",
]

PIPELINE_EXECUTION_COLUMNS = [
    "execution_id",
    "started_at",
    "finished_at",
    "duration_seconds",
    "status",
    "rows_read",
    "rows_valid",
    "rows_invalid",
    "rows_processed",
    "input_path",
    "output_path",
    "error_message",
]


class MissingColumnsError(ValueError):
    """Raised when a dataframe is missing required warehouse columns."""


def validate_columns(
    dataframe: pd.DataFrame,
    required_columns: Sequence[str],
) -> None:
    """Validate that a dataframe contains the required warehouse columns."""
    missing_columns = [
        column for column in required_columns if column not in dataframe.columns
    ]

    if missing_columns:
        missing = ", ".join(missing_columns)
        raise MissingColumnsError(f"Missing required columns: {missing}")


def write_dataframe(
    connection: duckdb.DuckDBPyConnection,
    table_name: str,
    dataframe: pd.DataFrame,
    columns: Sequence[str],
) -> int:
    """Write a dataframe into a warehouse table."""
    validate_columns(dataframe, columns)

    if dataframe.empty:
        return 0

    selected = dataframe.loc[:, list(columns)]
    temporary_view = f"tmp_{table_name}"
    column_list = ", ".join(columns)

    connection.register(temporary_view, selected)

    try:
        connection.execute(
            f"""
            INSERT INTO {table_name} ({column_list})
            SELECT {column_list}
            FROM {temporary_view}
            """
        )
    finally:
        connection.unregister(temporary_view)

    return len(selected)


def write_raw_transactions(
    connection: duckdb.DuckDBPyConnection,
    dataframe: pd.DataFrame,
) -> int:
    """Write raw transaction rows into the warehouse."""
    return write_dataframe(
        connection,
        "raw_transactions",
        dataframe,
        RAW_TRANSACTION_COLUMNS,
    )


def write_fact_transactions(
    connection: duckdb.DuckDBPyConnection,
    dataframe: pd.DataFrame,
) -> int:
    """Write validated transaction facts into the warehouse."""
    return write_dataframe(
        connection,
        "fact_transactions",
        dataframe,
        FACT_TRANSACTION_COLUMNS,
    )


def write_user_balances(
    connection: duckdb.DuckDBPyConnection,
    dataframe: pd.DataFrame,
) -> int:
    """Write user balance facts into the warehouse."""
    return write_dataframe(
        connection,
        "fact_user_balances",
        dataframe,
        USER_BALANCE_COLUMNS,
    )


def write_pipeline_executions(
    connection: duckdb.DuckDBPyConnection,
    dataframe: pd.DataFrame,
) -> int:
    """Write pipeline execution metadata into the warehouse."""
    return write_dataframe(
        connection,
        "fact_pipeline_executions",
        dataframe,
        PIPELINE_EXECUTION_COLUMNS,
    )

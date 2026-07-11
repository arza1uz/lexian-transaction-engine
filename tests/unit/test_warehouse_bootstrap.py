from pathlib import Path

import duckdb

from lexian_transaction_engine.warehouse.bootstrap import initialize_warehouse


def test_initialize_warehouse_creates_database_with_expected_tables(
    tmp_path: Path,
) -> None:
    database_path = tmp_path / "lexian_test.duckdb"

    result_path = initialize_warehouse(database_path)

    assert result_path == database_path
    assert database_path.exists()

    connection = duckdb.connect(str(database_path))

    try:
        table_names = {
            row[0]
            for row in connection.execute("SHOW TABLES").fetchall()
        }

        assert "raw_transactions" in table_names
        assert "fact_transactions" in table_names
        assert "fact_user_balances" in table_names
        assert "fact_pipeline_executions" in table_names
    finally:
        connection.close()

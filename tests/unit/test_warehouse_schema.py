from pathlib import Path

from lexian_transaction_engine.warehouse import (
    connect_warehouse,
    create_schema,
    load_schema_sql,
)


def test_load_schema_sql_reads_schema_file() -> None:
    schema_sql = load_schema_sql()

    assert "CREATE TABLE IF NOT EXISTS raw_transactions" in schema_sql
    assert "CREATE TABLE IF NOT EXISTS fact_transactions" in schema_sql
    assert "CREATE TABLE IF NOT EXISTS fact_user_balances" in schema_sql
    assert "CREATE TABLE IF NOT EXISTS fact_pipeline_executions" in schema_sql


def test_connect_warehouse_creates_duckdb_connection(tmp_path: Path) -> None:
    database_path = tmp_path / "lexian_test.duckdb"

    connection = connect_warehouse(database_path)

    try:
        result = connection.execute("SELECT 1").fetchone()
        assert result == (1,)
    finally:
        connection.close()


def test_create_schema_creates_expected_tables(tmp_path: Path) -> None:
    database_path = tmp_path / "lexian_test.duckdb"
    connection = connect_warehouse(database_path)

    try:
        create_schema(connection)

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

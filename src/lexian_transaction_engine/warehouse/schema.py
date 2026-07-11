from pathlib import Path

import duckdb

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_SCHEMA_PATH = PROJECT_ROOT / "warehouse" / "schema.sql"


def load_schema_sql(schema_path: Path = DEFAULT_SCHEMA_PATH) -> str:
    """Load the local analytical warehouse schema SQL."""
    return schema_path.read_text(encoding="utf-8")


def create_schema(
    connection: duckdb.DuckDBPyConnection,
    schema_path: Path = DEFAULT_SCHEMA_PATH,
) -> None:
    """Create the local analytical warehouse schema."""
    connection.execute(load_schema_sql(schema_path))

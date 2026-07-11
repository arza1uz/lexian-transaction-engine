from pathlib import Path
from typing import Any

import duckdb

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_QUERIES_PATH = PROJECT_ROOT / "warehouse" / "queries"


def load_query(query_name: str, queries_path: Path = DEFAULT_QUERIES_PATH) -> str:
    """Load a SQL query from the warehouse queries directory."""
    query_path = queries_path / query_name

    if not query_path.exists():
        raise FileNotFoundError(f"Query file not found: {query_path}")

    return query_path.read_text(encoding="utf-8")


def execute_query(
    connection: duckdb.DuckDBPyConnection,
    query_name: str,
    queries_path: Path = DEFAULT_QUERIES_PATH,
) -> list[tuple[Any, ...]]:
    """Execute a named warehouse query and return all rows."""
    query = load_query(query_name, queries_path)
    return connection.execute(query).fetchall()

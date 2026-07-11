from pathlib import Path

import duckdb

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_WAREHOUSE_PATH = PROJECT_ROOT / "data" / "warehouse" / "lexian.duckdb"


def connect_warehouse(
    database_path: Path = DEFAULT_WAREHOUSE_PATH,
) -> duckdb.DuckDBPyConnection:
    """Create a DuckDB connection for the local analytical warehouse."""
    database_path.parent.mkdir(parents=True, exist_ok=True)
    return duckdb.connect(str(database_path))

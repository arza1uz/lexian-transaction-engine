from pathlib import Path

import duckdb

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_MARTS_PATH = PROJECT_ROOT / "analytics" / "marts"
DEFAULT_MART_NAMES = [
    "mart_user_balances",
    "mart_transaction_activity",
    "mart_pipeline_health",
    "mart_balance_validation",
    "mart_data_quality_summary",
]


def load_mart_sql(
    mart_name: str,
    marts_path: Path = DEFAULT_MARTS_PATH,
) -> str:
    """Load a mart SQL file by mart name."""
    mart_path = marts_path / f"{mart_name}.sql"
    return mart_path.read_text(encoding="utf-8")


def build_mart(
    connection: duckdb.DuckDBPyConnection,
    mart_name: str,
    marts_path: Path = DEFAULT_MARTS_PATH,
) -> None:
    """Build a single analytical mart in DuckDB."""
    connection.execute(load_mart_sql(mart_name, marts_path))


def build_all_marts(
    connection: duckdb.DuckDBPyConnection,
    marts_path: Path = DEFAULT_MARTS_PATH,
) -> list[str]:
    """Build all analytical marts and return their names."""
    built_marts: list[str] = []

    for mart_name in DEFAULT_MART_NAMES:
        build_mart(connection, mart_name, marts_path)
        built_marts.append(mart_name)

    return built_marts

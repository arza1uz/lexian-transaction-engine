from pathlib import Path

from lexian_transaction_engine.warehouse.connection import (
    DEFAULT_WAREHOUSE_PATH,
    connect_warehouse,
)
from lexian_transaction_engine.warehouse.schema import create_schema


def initialize_warehouse(
    database_path: Path = DEFAULT_WAREHOUSE_PATH,
) -> Path:
    """Initialize the local analytical warehouse and return its path."""
    connection = connect_warehouse(database_path)

    try:
        create_schema(connection)
    finally:
        connection.close()

    return database_path

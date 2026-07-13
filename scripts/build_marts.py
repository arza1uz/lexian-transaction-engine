from lexian_transaction_engine.analytics import build_all_marts
from lexian_transaction_engine.warehouse import connect_warehouse, create_schema


def main() -> None:
    """Build analytical marts against the default local warehouse."""
    connection = connect_warehouse()

    try:
        create_schema(connection)
        built_marts = build_all_marts(connection)
    finally:
        connection.close()

    print("Built marts:")
    for mart_name in built_marts:
        print(f"- {mart_name}")


if __name__ == "__main__":
    main()

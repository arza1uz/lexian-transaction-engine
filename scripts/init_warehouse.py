from lexian_transaction_engine.warehouse.bootstrap import initialize_warehouse


def main() -> None:
    warehouse_path = initialize_warehouse()
    print(f"Local analytical warehouse initialized at: {warehouse_path}")


if __name__ == "__main__":
    main()

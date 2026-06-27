import pandas as pd

from lexian_transaction_engine.reporter import generate_balance_report


def test_generate_balance_report_writes_csv(tmp_path):
    balances = pd.DataFrame(
        [
            {"user_id": "U002", "balance": 500},
            {"user_id": "U001", "balance": 750},
        ]
    )
    output_path = tmp_path / "balances.csv"

    report = generate_balance_report(balances, output_path)

    assert report.to_dict("records") == [
        {"user_id": "U001", "balance": 750},
        {"user_id": "U002", "balance": 500},
    ]
    assert output_path.exists()

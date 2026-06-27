from pathlib import Path

from lexian_transaction_engine.main import run_pipeline


def test_transaction_pipeline_generates_balance_report(tmp_path):
    report_path = tmp_path / "balances.csv"

    run_pipeline(
        input_path=Path("data/raw/transactions.csv"),
        report_path=report_path,
    )

    assert report_path.read_text() == (
        "user_id,balance\n"
        "U001,1050\n"
        "U002,800\n"
        "U003,1150\n"
        "U004,550\n"
    )

"""Command-line entry point for Lexian Transaction Engine."""

from pathlib import Path

from lexian_transaction_engine.loader import load_transactions
from lexian_transaction_engine.processor import calculate_balances
from lexian_transaction_engine.reporter import generate_balance_report
from lexian_transaction_engine.validator import validate_transactions

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INPUT_PATH = PROJECT_ROOT / "data" / "raw" / "transactions.csv"
DEFAULT_REPORT_PATH = PROJECT_ROOT / "data" / "reports" / "balances.csv"


def run_pipeline(
    input_path: Path = DEFAULT_INPUT_PATH,
    report_path: Path = DEFAULT_REPORT_PATH,
) -> None:
    """Run the v1 CSV transaction pipeline."""
    transactions = load_transactions(input_path)
    validated_transactions = validate_transactions(transactions)
    balances = calculate_balances(validated_transactions)
    report = generate_balance_report(balances, report_path)
    print(report.to_string(index=False))


def main():
    """Execute the transaction pipeline with default local paths."""
    run_pipeline()


if __name__ == "__main__":
    main()

from pathlib import Path

from lexian_transaction_engine.loader import load_transactions
from lexian_transaction_engine.observability import (
    Execution,
    ExecutionContext,
    configure_logger,
)
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
    execution = Execution.start(
        input_path=str(input_path),
        output_path=str(report_path),
    )
    logger = configure_logger()
    context = ExecutionContext(execution=execution, logger=logger)

    context.logger.info(
        (
            "Pipeline execution started | execution_id=%s | "
            "input_path=%s | output_path=%s"
        ),
        context.execution.execution_id,
        context.execution.input_path,
        context.execution.output_path,
    )

    try:
        transactions = load_transactions(input_path)
        rows_read = len(transactions)

        context.logger.info(
            "Transactions loaded | execution_id=%s | rows_read=%s",
            context.execution.execution_id,
            rows_read,
        )

        validated_transactions = validate_transactions(transactions)
        rows_valid = len(validated_transactions)
        rows_invalid = rows_read - rows_valid

        context.logger.info(
            (
                "Transactions validated | execution_id=%s | "
                "rows_valid=%s | rows_invalid=%s"
            ),
            context.execution.execution_id,
            rows_valid,
            rows_invalid,
        )

        balances = calculate_balances(validated_transactions)
        balances_generated = len(balances)

        context.logger.info(
            "Balances calculated | execution_id=%s | balances_generated=%s",
            context.execution.execution_id,
            balances_generated,
        )

        report = generate_balance_report(balances, report_path)

        context.execution.finish(
            rows_read=rows_read,
            rows_valid=rows_valid,
            rows_invalid=rows_invalid,
            rows_processed=rows_valid,
        )

        context.logger.info(
            (
                "Pipeline execution completed | execution_id=%s | "
                "status=%s | duration_seconds=%.4f"
            ),
            context.execution.execution_id,
            context.execution.status,
            context.execution.duration_seconds,
        )

        print(report.to_string(index=False))

    except Exception as exc:
        context.execution.fail(error_message=str(exc))
        context.logger.exception(
            (
                "Pipeline execution failed | execution_id=%s | "
                "status=%s | error=%s"
            ),
            context.execution.execution_id,
            context.execution.status,
            context.execution.error_message,
        )
        raise


def main() -> None:
    """Execute the transaction pipeline with default local paths."""
    run_pipeline()


if __name__ == "__main__":
    main()
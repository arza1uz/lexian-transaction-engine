from datetime import UTC

from lexian_transaction_engine.observability import Execution, ExecutionStatus


def test_execution_start_creates_running_execution():
    execution = Execution.start(
        input_path="data/raw/transactions.csv",
        output_path="data/reports/balances.csv",
    )

    assert execution.execution_id
    assert execution.started_at.tzinfo == UTC
    assert execution.status == ExecutionStatus.RUNNING
    assert execution.input_path == "data/raw/transactions.csv"
    assert execution.output_path == "data/reports/balances.csv"


def test_execution_finish_marks_success_and_records_counts():
    execution = Execution.start()

    execution.finish(
        rows_read=10,
        rows_valid=8,
        rows_invalid=2,
        rows_processed=8,
    )

    assert execution.status == ExecutionStatus.SUCCESS
    assert execution.finished_at is not None
    assert execution.duration_seconds is not None
    assert execution.rows_read == 10
    assert execution.rows_valid == 8
    assert execution.rows_invalid == 2
    assert execution.rows_processed == 8


def test_execution_fail_marks_failed_and_records_error():
    execution = Execution.start()

    execution.fail(error_message="CSV file not found")

    assert execution.status == ExecutionStatus.FAILED
    assert execution.finished_at is not None
    assert execution.duration_seconds is not None
    assert execution.error_message == "CSV file not found"
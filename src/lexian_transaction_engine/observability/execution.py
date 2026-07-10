from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum
from uuid import uuid4


class ExecutionStatus(StrEnum):
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"


@dataclass
class Execution:
    execution_id: str
    started_at: datetime
    finished_at: datetime | None = None
    duration_seconds: float | None = None
    status: ExecutionStatus = ExecutionStatus.RUNNING
    rows_read: int = 0
    rows_valid: int = 0
    rows_invalid: int = 0
    rows_processed: int = 0
    input_path: str | None = None
    output_path: str | None = None
    error_message: str | None = None

    @classmethod
    def start(
        cls,
        input_path: str | None = None,
        output_path: str | None = None,
    ) -> "Execution":
        return cls(
            execution_id=str(uuid4()),
            started_at=datetime.now(UTC),
            input_path=input_path,
            output_path=output_path,
        )

    def finish(
        self,
        rows_read: int = 0,
        rows_valid: int = 0,
        rows_invalid: int = 0,
        rows_processed: int = 0,
    ) -> None:
        self.finished_at = datetime.now(UTC)
        self.duration_seconds = (
            self.finished_at - self.started_at
        ).total_seconds()
        self.status = ExecutionStatus.SUCCESS
        self.rows_read = rows_read
        self.rows_valid = rows_valid
        self.rows_invalid = rows_invalid
        self.rows_processed = rows_processed

    def fail(self, error_message: str) -> None:
        self.finished_at = datetime.now(UTC)
        self.duration_seconds = (
            self.finished_at - self.started_at
        ).total_seconds()
        self.status = ExecutionStatus.FAILED
        self.error_message = error_message
import logging
from dataclasses import dataclass

from lexian_transaction_engine.observability.execution import Execution


@dataclass
class ExecutionContext:
    execution: Execution
    logger: logging.Logger
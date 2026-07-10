import logging

from lexian_transaction_engine.observability import Execution, ExecutionContext


def test_execution_context_groups_execution_and_logger():
    execution = Execution.start()
    logger = logging.getLogger("test_logger")

    context = ExecutionContext(execution=execution, logger=logger)

    assert context.execution == execution
    assert context.logger == logger
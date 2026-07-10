import logging

from lexian_transaction_engine.observability import configure_logger


def test_configure_logger_returns_logger_with_handler():
    logger = configure_logger("test_lexian_logger")

    assert logger.name == "test_lexian_logger"
    assert logger.level == logging.INFO
    assert logger.handlers
    assert logger.propagate is False


def test_configure_logger_does_not_duplicate_handlers():
    logger = configure_logger("test_lexian_logger_no_duplicates")
    initial_handler_count = len(logger.handlers)

    logger = configure_logger("test_lexian_logger_no_duplicates")

    assert len(logger.handlers) == initial_handler_count
.PHONY: install test lint format run validate

install:
	python -m pip install -e ".[dev]"

test:
	PYTHONPATH=src python -m pytest

lint:
	python -m ruff check .

format:
	python -m ruff format .

run:
	PYTHONPATH=src python -m lexian_transaction_engine.main

validate: lint test run

init-warehouse:
	PYTHONPATH=src python scripts/init_warehouse.py

demo-warehouse:
	PYTHONPATH=src python scripts/demo_warehouse.py

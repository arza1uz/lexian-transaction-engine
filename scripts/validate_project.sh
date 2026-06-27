#!/usr/bin/env bash
set -euo pipefail

python -m ruff check .
PYTHONPATH=src python -m pytest
PYTHONPATH=src python -m lexian_transaction_engine.main

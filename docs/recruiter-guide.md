# Recruiter Guide

## What This Repo Solves

Lexian Transaction Engine processes synthetic financial transactions and produces user balances through a clear CSV batch pipeline.

## Skills Demonstrated

- Python data engineering with pandas.
- Schema and business-rule validation.
- Unit and integration testing.
- Lightweight CI and linting.
- Product-minded technical documentation.
- Incremental system design without over-engineering.

## Quick Review Path

1. Read `README.md`.
2. Inspect `src/lexian_transaction_engine/validator.py`.
3. Inspect `src/lexian_transaction_engine/processor.py`.
4. Review `tests/integration/test_transaction_pipeline.py`.
5. Skim `docs/system-design.md` and `docs/roadmap.md`.

## Planned Improvements

Future stages include reconciliation, analytical storage, orchestration, streaming, cloud deployment, ML pipelines, and AI assistants. These are documented as learning unlocks rather than implemented prematurely.

## Why This Is Not A Tutorial Clone

The repository is framed as a product service inside a fictional fintech ecosystem. It includes business context, ADRs, RFCs, CI, tests, and a roadmap that explain engineering tradeoffs beyond basic code examples.

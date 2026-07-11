# Changelog

## [Unreleased]

### Added

- RFC 0003 for the local analytical warehouse design.
- DuckDB-based local warehouse connection and schema creation utilities.
- Initial warehouse schema for raw transactions, transaction facts, user balances, and pipeline executions.
- SQL query examples for balances, transaction summaries, execution summaries, and data quality checks.
- Warehouse writer utilities for loading pandas dataframes into analytical tables.
- Warehouse bootstrap script and Makefile target for local initialization.

## [Unreleased]

- Operational observability in progress.
- Execution tracking in progress.
- Structured logging in progress.
- ExecutionContext in progress.
- Pipeline lifecycle logs in progress.

## [1.0.0] - Portfolio V1

- Professional repository structure.
- Synthetic transaction dataset.
- CSV loading.
- Validation for required columns, duplicate transaction IDs, supported types, and valid amounts.
- Balance calculation.
- Report generation.
- Tests.
- CI.
- Documentation.
- ADRs and RFCs.

## [0.1.0]

- Flattened the repository into a product-oriented Lexian Transaction Engine layout.
- Added v1 CSV transaction loading, validation, processing, and reporting.
- Added tests, CI, documentation, ADRs, and RFC scaffolding.

# Changelog

## Unreleased

### Added

- Added Analytics Engineering Layer with reusable marts.
- Added metrics and model definitions.
- Added mart builder script.
- Added tests for mart creation and validation outputs.

## [1.2.0] - Warehouse Analytics Queries

### Added

- Additional warehouse analytics queries for user balances by execution, transaction volume, pipeline health, balance validation, and anomaly detection.
- Unit tests covering analytical SQL query execution against the local DuckDB warehouse.

## [1.1.0] - Local Analytical Warehouse Foundation

### Added

- RFC 0003 for the local analytical warehouse design.
- DuckDB-based local warehouse connection and schema creation utilities.
- Initial warehouse schema for raw transactions, transaction facts, user balances, and pipeline executions.
- SQL query examples for balances, transaction summaries, execution summaries, and data quality checks.
- Warehouse writer utilities for loading pandas dataframes into analytical tables.
- Warehouse bootstrap script and Makefile target for local initialization.

## [1.0.0] - Portfolio V1 + Operational Observability Foundation

### Added

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
- Operational observability foundation.
- Execution tracking.
- Structured logging.
- ExecutionContext.
- Pipeline lifecycle logs.

## [0.1.0]

- Flattened the repository into a product-oriented Lexian Transaction Engine layout.
- Added v1 CSV transaction loading, validation, processing, and reporting.
- Added tests, CI, documentation, ADRs, and RFC scaffolding.

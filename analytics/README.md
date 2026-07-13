# Analytics Engineering Layer

The analytics layer contains reusable analytical marts for Lexian's local DuckDB warehouse. It turns warehouse facts and execution metadata into business-facing models that can support BI, validation, reconciliation, and operational review.

This layer is inspired by analytics engineering practices, but intentionally does not use dbt yet. The current implementation keeps the project lightweight while establishing clear mart SQL, metric definitions, model definitions, and validation outputs.

## Structure

- `marts/` contains SQL view definitions for reusable analytical outputs.
- `definitions/metrics.yml` documents core metrics and their grains.
- `definitions/models.yml` documents mart contracts, source tables, ownership, and status.

## Marts

- `mart_user_balances` compares stored user balances with SQL-calculated balances.
- `mart_transaction_activity` aggregates transaction volume and value by execution, user, and transaction type.
- `mart_pipeline_health` exposes execution-level operational health metrics.
- `mart_balance_validation` classifies balance validation results by severity.
- `mart_data_quality_summary` summarizes raw, fact, balance, and execution metadata quality.

## Local Build

Build marts against the local DuckDB warehouse:

```bash
make build-marts
```

The build script creates the warehouse schema first, so it can run safely against an empty local database.

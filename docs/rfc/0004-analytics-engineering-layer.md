# RFC 0004: Analytics Engineering Layer

## 1. Business Context

Lexian now has transaction processing, operational observability, a local DuckDB warehouse, and warehouse analytics queries. The next step is to create reusable analytical models that can support BI, validation, reconciliation, and operational review.

The warehouse layer stores facts and execution metadata. The analytics layer turns those facts into stable, business-facing marts with documented metrics, model definitions, and validation outputs.

## 2. Problem

Warehouse queries are useful, but they are still individual SQL files. They do not yet represent a modeled analytics layer with reusable marts, metric definitions, and validation outputs.

Without this layer, downstream analysis has to repeatedly rebuild business logic for balances, pipeline health, transaction activity, and data quality checks.

## 3. Goals

- Create business-facing analytical marts.
- Define reusable metrics.
- Define model contracts.
- Add validation outputs for balances and data quality.
- Keep the implementation local with DuckDB.
- Prepare for reconciliation and graph auditability.

## 4. Non-Goals

- No dbt yet.
- No cloud yet.
- No dashboards yet.
- No reconciliation matching yet.
- No graph database yet.
- No ML or AI yet.

## 5. Proposed Solution

Create an `analytics/` layer with two responsibilities:

- `analytics/marts/` stores reusable SQL mart definitions as DuckDB views.
- `analytics/definitions/` documents metrics and model contracts in YAML-style files.

Add a small Python builder under `src/lexian_transaction_engine/analytics/` and a local script at `scripts/build_marts.py` to create the mart views against the DuckDB warehouse.

## 6. Mart Definitions

### mart_user_balances

- Grain: one row per `execution_id` and `user_id`.
- Source tables: `fact_user_balances`, `fact_transactions`.
- Business purpose: compare stored pipeline balances against SQL-calculated balances.
- Key metrics: stored balance, SQL-calculated balance, balance difference, validation status, transaction count.

### mart_transaction_activity

- Grain: one row per `execution_id`, `user_id`, and `transaction_type`.
- Source tables: `fact_transactions`.
- Business purpose: expose reusable transaction volume and amount aggregates.
- Key metrics: transaction count, gross amount, net amount, first transaction timestamp, last transaction timestamp.

### mart_pipeline_health

- Grain: one row per `execution_id`.
- Source tables: `fact_pipeline_executions`.
- Business purpose: summarize operational health for each pipeline execution.
- Key metrics: valid row rate, invalid row rate, processing efficiency, health status.

### mart_balance_validation

- Grain: one row per `execution_id` and `user_id`.
- Source tables: `fact_user_balances`, `fact_transactions`.
- Business purpose: provide validation-focused balance outputs with severity classification.
- Key metrics: stored balance, SQL-calculated balance, absolute difference, validation status, validation severity.

### mart_data_quality_summary

- Grain: one row per `execution_id`.
- Source tables: `raw_transactions`, `fact_transactions`, `fact_user_balances`, `fact_pipeline_executions`.
- Business purpose: summarize execution-level data quality across raw, fact, balance, and operational metadata.
- Key metrics: raw row count, fact transaction count, balance record count, invalid row count, duplicate raw transaction count, data quality status.

## 7. Acceptance Criteria

- Marts exist as SQL files.
- `metrics.yml` exists.
- `models.yml` exists.
- `build_marts.py` can create views in DuckDB.
- Tests validate mart creation and analytical outputs.
- Existing tests pass.

## Status

Accepted / In Progress

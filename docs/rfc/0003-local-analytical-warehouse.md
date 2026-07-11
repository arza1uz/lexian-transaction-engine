# RFC 0003: Local Analytical Warehouse

## Business Context

Lexian Transaction Engine can currently process synthetic transaction files, validate business rules, calculate user balances, generate reports, and expose basic operational observability.

However, the output still lives primarily as files and logs. This limits the ability of Operations, Finance, and Analytics teams to query historical results, audit pipeline executions, compare outputs across runs, and answer business questions using SQL.

To support the next stage of the portfolio, the Transaction Engine needs a local analytical warehouse.

## Problem

The current system can answer questions about a single run, but it cannot easily answer historical or analytical questions such as:

- How many transactions were processed per execution?
- Which transaction types dominate volume?
- How many rows were valid or invalid over time?
- What was each user's balance after each execution?
- Can balances be recalculated using SQL and compared with Python outputs?
- Which pipeline executions failed or had abnormal row counts?

Without persistent analytical tables, the system remains file-based and difficult to audit.

## Goals

- Introduce a local analytical warehouse using DuckDB.
- Preserve raw transaction rows for auditability.
- Store validated transaction facts for SQL-based analysis.
- Store user balance facts for historical analysis.
- Store pipeline execution metadata for operational analytics.
- Keep the first warehouse implementation simple, local, and easy to run.
- Prepare the project for future analytics engineering work with dbt.

## Non-Goals

- Do not introduce cloud infrastructure yet.
- Do not use Redshift, BigQuery, or Snowflake yet.
- Do not introduce dbt in this RFC.
- Do not introduce orchestration tools such as Airflow or Mage yet.
- Do not replace the existing Python pipeline.
- Do not build dashboards yet.

## Proposed Solution

Add a local warehouse layer based on DuckDB.

The initial warehouse will include:

- warehouse/schema.sql
- warehouse/README.md
- warehouse/queries/user_balances.sql
- warehouse/queries/transaction_summary.sql
- warehouse/queries/execution_summary.sql
- warehouse/queries/data_quality_checks.sql

The Python package will later include:

- src/lexian_transaction_engine/warehouse/connection.py
- src/lexian_transaction_engine/warehouse/schema.py
- src/lexian_transaction_engine/warehouse/writer.py

## Data Model

| Table | Grain | Primary Key | Purpose |
| --- | --- | --- | --- |
| raw_transactions | One source file row per execution | execution_id, source_row_number | Preserve what arrived before validation |
| fact_transactions | One valid transaction per execution | execution_id, transaction_id | Analyze valid financial movement |
| fact_user_balances | One user balance per execution | execution_id, user_id | Analyze balances over time |
| fact_pipeline_executions | One pipeline execution | execution_id | Analyze pipeline reliability and run metadata |

## Design Principles

### Preserve Raw Data

Raw data should be stored before transformation. Invalid values should not be discarded before they can be audited.

### Separate Raw From Facts

Raw tables preserve what arrived. Fact tables store validated, analysis-ready records.

### Track Execution Lineage

Every warehouse record should include execution_id when relevant. This allows outputs to be traced back to the pipeline run that produced them.

### Keep It Local First

DuckDB is intentionally chosen for V3 because it supports analytical SQL locally without requiring a database server or cloud infrastructure.

## Future Extensions

Future versions may add:

- dbt models
- dimensional models
- reconciliation tables
- graph auditability
- orchestration
- cloud storage
- Redshift or BigQuery integration

## Acceptance Criteria

- Warehouse schema is documented.
- Table grain is explicitly defined.
- Primary keys are defined.
- Initial SQL queries are included.
- Local generated warehouse files are ignored by Git.
- Existing tests continue passing.
- No cloud infrastructure is introduced.

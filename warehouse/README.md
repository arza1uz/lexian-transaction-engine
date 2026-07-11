# Local Analytical Warehouse

This directory contains the first local analytical warehouse design for Lexian Transaction Engine.

The goal is to move beyond file-based outputs and introduce persistent analytical tables that can be queried with SQL.

## Current Scope

V3 focuses on local warehouse foundations using DuckDB.

The warehouse stores:

- raw transaction rows received from source files,
- validated transaction facts,
- user balance facts,
- pipeline execution metadata.

## Tables

| Table | Grain | Purpose |
| --- | --- | --- |
| raw_transactions | One row per source file row per execution | Preserve source data for auditability |
| fact_transactions | One valid transaction per execution | Analyze financial movement |
| fact_user_balances | One user balance per execution | Analyze balances over time |
| fact_pipeline_executions | One pipeline run | Analyze operational reliability |

## Design Principles

- Preserve raw data before transformation.
- Keep valid analytical facts separate from raw inputs.
- Track every row back to an execution ID.
- Make operational metadata queryable.
- Keep the first implementation local and simple before introducing cloud infrastructure.

## Query Examples

The queries directory contains SQL examples for:

- user balances,
- transaction summaries,
- execution summaries,
- data quality checks.

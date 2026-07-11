# Roadmap

This repository keeps the Transaction Engine roadmap short. The broader 12-month portfolio roadmap lives in the Portfolio Hub.

| Version | Portfolio Month | Status | Focus | Milestone |
| --- | --- | --- | --- | --- |
| V1 | Month 1 | Released | Batch Transaction Engine | Python package, tests, CI, docs, synthetic transaction processing |
| V2 | Month 2 | Released | Operational Observability | Structured logging, execution tracking, pipeline lifecycle, RFC 0002 |
| V3 | Month 3 | Released | SQL + Warehouse Foundations | DuckDB analytical warehouse, schema design, facts, and execution metadata |
| V3.1 | Month 3 | Released | Warehouse Analytics Queries | SQL queries for balances, transaction volume, pipeline health, validation, and data quality |
| V4 | Month 4 | Planned | Analytics Engineering Layer | dbt-style models, tests, documentation, KPI marts |
| V5 | Month 5 | Planned | AWS Data Pipeline Prototype | S3/Glue/Athena/Redshift-oriented pipeline prototype |
| V6 | Month 6 | Planned | Reconciliation + Graph Auditability | Matching logic plus graph-based audit trail |

## Principle

Each version should add capability because the business scenario needs it, not because a tool belongs on a checklist.

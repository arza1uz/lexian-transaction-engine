# System Design

## Why Batch CSV First

Lexian is at an MVP stage in this portfolio. A nightly CSV file is a realistic first integration pattern for early operational reporting, manual exports, and partner handoffs. It keeps the first version focused on correctness and explainability.

## Why Simple Python Modules First

The current product needs clear business logic more than distributed infrastructure. Small modules make it easy to inspect the loader, validator, processor, and reporter independently.

## Why Not Kafka, Spark, Airflow, Or Cloud Yet

Those tools become useful when there is enough volume, latency pressure, coordination complexity, or operational risk to justify them. Adding them too early would hide the core business rules behind infrastructure noise.

## Evolution Triggers

The architecture should evolve when Lexian needs:

- More reliable storage than CSV files.
- Reconciliation against external partners.
- Scheduled or dependency-aware workflows.
- Near-real-time balance updates.
- Auditable ledgers and stricter financial controls.
- Platform-level observability, security, and cost governance.

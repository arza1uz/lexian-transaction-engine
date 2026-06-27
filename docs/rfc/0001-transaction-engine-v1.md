# RFC 0001: Transaction Engine V1

## Business Problem

Lexian needs a trustworthy first transaction pipeline that can process synthetic deposits and withdrawals while making validation rules explicit.

## Scope

- Load CSV transactions.
- Validate schema, uniqueness, supported types, and amount rules.
- Calculate balances by user.
- Generate a balance report.
- Cover behavior with unit and integration tests.

## Non-Goals

- Real customer data.
- Kafka, Spark, Airflow, cloud deployment, ML, or AI systems.
- Full ledger accounting.
- Reconciliation against external partners.

## Proposed Architecture

CSV input flows through Loader, Validator, Processor, and Reporter modules. The output is a CSV balance report.

## Validation Rules

- Required columns must exist.
- Transaction IDs must be unique.
- Transaction type must be `deposit` or `withdrawal`.
- Amount must be numeric and greater than zero.

## Expected Outputs

The pipeline writes `data/reports/balances.csv` with `user_id` and `balance` columns.

## Testing Strategy

Use unit tests for each module and an integration test for the end-to-end CSV pipeline.

## Future Extensions

Future RFCs may introduce reconciliation, storage, orchestration, APIs, streaming, cloud deployment, ML pipelines, and AI assistants when the business case is clear.

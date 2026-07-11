# RFC 0002: Operational Readiness

## Status

Accepted / Released in v1.0.0

## Business Context

Lexian Transaction Engine is now able to process synthetic transaction files and generate user balance reports.

However, Operations needs better visibility into each pipeline execution. Before this RFC, the pipeline could run successfully or fail without leaving enough operational context to understand what happened.

## Problem

The system did not clearly expose:

- when a pipeline execution started,
- which input file was processed,
- which output file was generated,
- how many rows were read,
- how many rows were validated,
- how many balances were generated,
- whether the execution succeeded or failed,
- how long the execution took.

Without this visibility, failures are harder to detect and investigate.

## Goals

- Make each pipeline execution traceable.
- Introduce an execution ID for each run.
- Add structured lifecycle logs.
- Capture basic execution metadata.
- Keep observability concerns separate from business logic.
- Preserve the current transaction processing behavior.

## Non-Goals

- No external observability platform.
- No metrics backend.
- No tracing system.
- No dashboard.
- No Airflow, Kafka, Spark, or cloud logging yet.
- No persistent execution history yet.

## Scope Boundary

This RFC covers local execution metadata, execution context, structured logging, and lifecycle visibility. Advanced monitoring, metrics, tracing, dashboards, and cloud observability are intentionally deferred to future milestones.

## Proposed Solution

Introduce a lightweight observability package:

```text
src/lexian_transaction_engine/observability/
├── __init__.py
├── context.py
├── execution.py
└── logger.py
```

The package introduces:

- `Execution`: represents a single pipeline execution.
- `ExecutionContext`: groups execution state and logger.
- `configure_logger`: configures a standard Python logger.

## Design Principles

### Single Responsibility

Each component has one responsibility:

- `Execution` represents execution state.
- `ExecutionContext` carries shared execution dependencies.
- `logger.py` configures logging.
- `main.py` orchestrates the pipeline.

### Low Coupling

Loader, Validator, Processor, and Reporter should not configure logging themselves.

### Business Logic Isolation

Observability should not change the core processing rules.

## Logging Strategy

Use Python's standard `logging` module.

Logs should include:

- timestamp,
- level,
- logger name,
- message,
- execution ID,
- key operational fields.

Example:

```text
2026-06-29T21:04:07Z | INFO | lexian_transaction_engine | Pipeline execution started | execution_id=4036352b-3236-4f18-8872-9539ad5ff93b
```

## Execution Fields

`Execution` tracks:

- `execution_id`
- `started_at`
- `finished_at`
- `duration_seconds`
- `status`
- `rows_read`
- `rows_valid`
- `rows_invalid`
- `rows_processed`
- `input_path`
- `output_path`
- `error_message`

## Testing Strategy

Add unit tests for:

- execution creation,
- successful execution finish,
- failed execution finish,
- context grouping,
- logger configuration,
- logger handler duplication prevention.

Existing integration tests must continue passing.

## Acceptance Criteria

- Every run creates an execution ID.
- Pipeline logs start and completion.
- Pipeline logs row counts.
- Pipeline logs generated balances.
- Pipeline logs failures with error details.
- Observability code is separated from business modules.
- Existing tests continue passing.
- New observability tests are added.

# ADR 0002: Start With Batch CSV Processing

## Status

Accepted

## Context

Lexian is in its earliest stage. A nightly CSV is realistic for an MVP. More complex tools should appear only when the business requires them.

## Decision

Start the Transaction Engine with batch CSV processing.

## Consequences

- Faster learning and implementation.
- Clearer business logic.
- Easier testing.
- Future migration path to databases, orchestration, and streaming.

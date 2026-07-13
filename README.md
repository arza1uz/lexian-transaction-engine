# Lexian Transaction Engine

![CI](https://github.com/arza1uz/lexian-transaction-engine/actions/workflows/ci.yml/badge.svg)

**Production-minded batch transaction processing and local analytics for a fictional fintech data system.**

Lexian Transaction Engine processes synthetic fintech transactions, validates business rules, calculates balances, captures operational execution context, and exposes local analytical warehouse outputs through DuckDB and SQL queries.

Lexian is fictional and uses synthetic data only. This repository does not contain real customer data, employer data, Klar internal data, or confidential information.

## Released Versions

| Release | Scope |
| --- | --- |
| v1.0.0 | Batch transaction processing and operational observability |
| v1.1.0 | Local analytical warehouse foundation |
| v1.2.0 | Warehouse analytics queries |

## Current Capabilities

- Synthetic CSV transaction ingestion
- Transaction validation
- Balance calculation
- Operational execution tracking
- Structured logging
- DuckDB local warehouse
- SQL analytics queries
- Data quality and validation queries
- Tests and CI

## Architecture

```mermaid
flowchart LR
    A[CSV Transactions] --> B[Loader]
    B --> C[Validator]
    C --> D[Processor]
    D --> E[Reporter]
    D --> F[DuckDB Warehouse]
    F --> G[SQL Analytics Queries]
```

## Run Locally

```bash
make install
make run
make test
make lint
```

The package command is:

```bash
python -m lexian_transaction_engine.main
```

## Repository Structure

```text
.
├── data/
├── docs/
├── scripts/
├── src/lexian_transaction_engine/
├── tests/
├── warehouse/
├── Makefile
├── pyproject.toml
└── README.md
```

## Documentation

- [Business Context](docs/business-context.md)
- [Architecture](docs/architecture.md)
- [Development Focus](docs/roadmap.md)
- [Local Analytical Warehouse](warehouse/README.md)
- [ADRs](docs/adr/README.md)
- [RFCs](docs/rfc/README.md)

## Current Development Focus

Current development is focused on the Analytics Engineering Layer and Validation Layer.

Future work will extend the system into reconciliation, break management, graph auditability, cloud data workflows, ML/Risk, and AI-assisted investigation.

## Portfolio Context

This repository is not a tutorial clone and not a giant monorepo. It is a focused technical project designed to demonstrate data engineering, analytics engineering, fintech data systems, documentation, testing, and operational thinking.

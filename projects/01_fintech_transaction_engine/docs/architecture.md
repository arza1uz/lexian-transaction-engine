# Architecture

## Goal

Build a simplified fintech transaction processing engine.

---

## Modules

### loader.py

Responsibility:

Read transaction files from CSV.

Input:

CSV file.

Output:

Transactions in memory.

---

### validator.py

Responsibility:

Validate transaction data before processing.

Input:

Transactions.

Output:

Valid transactions and validation errors.

---

### processor.py

Responsibility:

Calculate balances and transaction metrics.

Input:

Validated transactions.

Output:

Processed transaction results.

---

### reporter.py

Responsibility:

Generate reports for users.

Input:

Processed results.

Output:

CSV reports and summaries.

---

### main.py

Responsibility:

Coordinate the execution of all modules.
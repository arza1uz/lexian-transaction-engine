"""Validation rules for transaction input data."""

from __future__ import annotations

import pandas as pd

REQUIRED_COLUMNS = ["transaction_id", "user_id", "timestamp", "type", "amount"]
SUPPORTED_TRANSACTION_TYPES = {"deposit", "withdrawal"}


def validate_transactions(transactions: pd.DataFrame) -> pd.DataFrame:
    """Validate transaction records and return a normalized copy.

    Business rule for v1: transaction amounts must be numeric and strictly
    greater than zero. Withdrawals are represented by type, not by negative
    amounts.
    """
    errors: list[str] = []
    missing_columns = [
        column for column in REQUIRED_COLUMNS if column not in transactions.columns
    ]
    if missing_columns:
        errors.append(f"Missing required columns: {', '.join(missing_columns)}")

    if errors:
        raise ValueError("; ".join(errors))

    validated = transactions.copy()

    if validated["transaction_id"].duplicated().any():
        duplicate_ids = (
            validated.loc[
                validated["transaction_id"].duplicated(keep=False),
                "transaction_id",
            ]
            .astype(str)
            .unique()
        )
        errors.append(f"Duplicate transaction IDs: {', '.join(duplicate_ids)}")

    validated["type"] = validated["type"].astype(str).str.strip().str.lower()
    unsupported_types = sorted(
        set(validated["type"].dropna()) - SUPPORTED_TRANSACTION_TYPES
    )
    if unsupported_types:
        errors.append(f"Unsupported transaction types: {', '.join(unsupported_types)}")

    numeric_amounts = pd.to_numeric(validated["amount"], errors="coerce")
    invalid_amount_mask = numeric_amounts.isna()
    if invalid_amount_mask.any():
        invalid_ids = (
            validated.loc[invalid_amount_mask, "transaction_id"].astype(str).tolist()
        )
        errors.append(
            f"Non-numeric amount values for transactions: {', '.join(invalid_ids)}"
        )

    non_positive_amount_mask = numeric_amounts <= 0
    if non_positive_amount_mask.any():
        invalid_ids = (
            validated.loc[non_positive_amount_mask, "transaction_id"]
            .astype(str)
            .tolist()
        )
        errors.append(
            "Amounts must be greater than zero for transactions: "
            + ", ".join(invalid_ids)
        )

    if errors:
        raise ValueError("; ".join(errors))

    validated["amount"] = numeric_amounts
    return validated

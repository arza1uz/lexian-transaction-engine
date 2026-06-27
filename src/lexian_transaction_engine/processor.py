"""Transaction processing logic."""

import pandas as pd


def calculate_balances(transactions: pd.DataFrame) -> pd.DataFrame:
    """Calculate ending balances by user from validated transactions."""
    processed = transactions.copy()
    processed["signed_amount"] = processed["amount"].where(
        processed["type"] == "deposit",
        -processed["amount"],
    )

    balances = (
        processed.groupby("user_id", as_index=False)["signed_amount"]
        .sum()
        .rename(columns={"signed_amount": "balance"})
        .sort_values("user_id")
        .reset_index(drop=True)
    )
    return balances

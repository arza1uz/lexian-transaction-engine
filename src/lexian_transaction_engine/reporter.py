"""Reporting helpers for processed transaction results."""

from pathlib import Path

import pandas as pd


def generate_balance_report(
    balances: pd.DataFrame,
    output_path: Path | None = None,
) -> pd.DataFrame:
    """Prepare and optionally persist the user balance report."""
    report = balances.sort_values("user_id").reset_index(drop=True)

    if output_path is not None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        report.to_csv(output_path, index=False)

    return report

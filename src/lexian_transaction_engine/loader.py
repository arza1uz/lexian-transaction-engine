"""CSV loading utilities for Lexian Transaction Engine."""

from pathlib import Path

import pandas as pd


def load_transactions(file_path: Path) -> pd.DataFrame:
    """Load transactions from a CSV file."""
    if not file_path.exists():
        raise FileNotFoundError(f"Transaction file not found: {file_path}")
    if not file_path.is_file():
        raise IsADirectoryError(f"{file_path} is a directory")
    if file_path.suffix != ".csv":
        raise ValueError(f"{file_path} extension is not supported")
    return pd.read_csv(file_path)

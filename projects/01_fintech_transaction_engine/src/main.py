from pathlib import Path 
from loader import load_transactions

def main():
    project_root = Path(__file__).parent.parent
    data_path = project_root / "data" / "raw" / "transactions.csv"
    transactions=load_transactions(data_path)
 


if __name__ == "__main__":
    main()
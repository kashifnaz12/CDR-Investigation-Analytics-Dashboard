
import pandas as pd
from pathlib import Path

def load_file(file_path: str) -> pd.DataFrame:
    """
    Load CSV or Excel files safely.
    """
    path = Path(file_path)
    
    if path.suffix.lower() == ".csv":
        df = pd.read_csv(path, dtype=str)
    elif path.suffix.lower() in [".xls", ".xlsx"]:
        df = pd.read_excel(path, dtype=str)
    else:
        raise ValueError("Unsupported file format")
    
    df["source_file"] = path.name
    return df

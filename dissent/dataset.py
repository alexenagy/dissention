# Standard library
from pathlib import Path

# Third-party libraries
import pandas as pd
import typer
from loguru import logger
from tqdm import tqdm

# Local application imports
from dissent.config import RAW_DATA_DIR, PROCESSED_DATA_DIR

app = typer.Typer()

def main():
    """
    Memory-efficient merge of opinions with opinion clusters and dockets.

    Output guarantees:
    - One row per opinion
    - court_id is NULL if unavailable
    - date_filed is NULL if unavailable
    """
    
    parquets = [pd.read_parquet(f) for f in tqdm(PROCESSED_DATA_DIR.rglob("shard_*.parquet"))]
    df = pd.concat(parquets)

    print(df.head())
    df["year"] = df["date_filed"].astype(str).str.extract(r"(\d{4})")[0].astype(int) #regx
    
    df = df[df["year"] > 1897]
    df = df[df["year"] < 2026]
    df = df[df["court_type"] == "S"]
    df.to_parquet(PROCESSED_DATA_DIR / "dataset.parquet")

if __name__ == "__main__":
    main()

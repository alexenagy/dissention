from pathlib import Path
import pandas as pd
import typer
from loguru import logger
from tqdm import tqdm
from dissent.config import RAW_DATA_DIR, PROCESSED_DATA_DIR, INTERIM_DATA_DIR

app = typer.Typer()

def load_dime():
    dime = pd.read_csv(
        RAW_DATA_DIR / "contribDB_judicial.csv.gz",
        compression="gzip",
        usecols=["recipient.name", "candidate.cfscore", "recipient.state", "seat"],
        encoding="latin-1",
    )
    dime = dime[dime["seat"] == "state:judicial:supreme"]
    dime["last_name"] = dime["recipient.name"].str.split(",").str[0].str.strip().str.title()
    dime = dime[~dime["last_name"].str.contains(" ", na=False)]
    return dime.groupby(["last_name", "recipient.state"])["candidate.cfscore"].mean().reset_index()

def main():
    parquets = [pd.read_parquet(f) for f in tqdm(INTERIM_DATA_DIR.rglob("shard_*.parquet"))]
    df = pd.concat(parquets)

    df["year"] = df["date_filed"].astype(str).str.extract(r"(\d{4})")[0].astype(int)
    df = df[df["year"] > 1897]
    df = df[df["year"] < 2026]
    df = df[df["court_type"] == "S"]

    # Merge CF-scores
    dime = load_dime()
    df["state"] = df["court_jurisdiction"].str.extract(r",\s*([A-Z]{2})$")
    df["judges_list"] = df["judges"].str.split(",")
    df_exploded = df.explode("judges_list")
    df_exploded["last_name"] = df_exploded["judges_list"].str.strip().str.split().str[0].str.title()
    df_exploded = df_exploded.merge(
        dime,
        left_on=["last_name", "state"],
        right_on=["last_name", "recipient.state"],
        how="left"
    )
    logger.info(f"Unique justices matched: {df_exploded['last_name'].nunique()}")

    df_exploded.to_parquet(PROCESSED_DATA_DIR / "dataset.parquet")

if __name__ == "__main__":
    main()
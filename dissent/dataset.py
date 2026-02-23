from pathlib import Path
import pandas as pd
import typer
from loguru import logger
from tqdm import tqdm
from dissent.config import RAW_DATA_DIR, PROCESSED_DATA_DIR, INTERIM_DATA_DIR

app = typer.Typer()


def load_dime():
    """
    Load and clean DIME judicial CF-scores.
    Filters to state supreme court justices only.
    Returns deduplicated dataframe with last_name, recipient.state, candidate.cfscore.
    """
    dime = pd.read_csv(
        RAW_DATA_DIR / "contribDB_judicial.csv.gz",
        compression="gzip",
        usecols=["recipient.name", "candidate.cfscore", "recipient.state", "seat"],
        encoding="latin-1",
    )
    dime = dime[dime["seat"] == "state:judicial:supreme"]
    dime["last_name"] = (
        dime["recipient.name"].str.split(",").str[0].str.strip().str.title()
    )
    # Filter out committee names (contain spaces)
    dime = dime[~dime["last_name"].str.contains(" ", na=False)]
    return (
        dime.groupby(["last_name", "recipient.state"])["candidate.cfscore"]
        .mean()
        .reset_index()
    )


def extract_text(opinions):
    """Extract and concatenate opinion text from nested opinions column into a flat string."""
    if opinions is None:
        return None
    texts = []
    for o in opinions:
        if isinstance(o, dict):
            t = o.get("opinion_text")
            if t:
                texts.append(t)
    return " ".join(texts) if texts else None


def main():
    """
    Merge opinion shards, filter by year and court type, merge CF-scores,
    and add a flat opinion_text column alongside the nested opinions column.

    Output guarantees:
    - One row per judge-opinion pair (exploded on judges)
    - candidate.cfscore is NULL if justice not matched in DIME
    - abs_cfscore is the absolute value of candidate.cfscore (ideological intensity)
    - opinion_text is a flat string of all opinion text (for Wordscores)
    - opinions column is kept nested (for EMI per-opinion scoring)
    """
    parquets = []
    for f in tqdm(sorted(INTERIM_DATA_DIR.rglob("shard_*.parquet"))):
        try:
            parquets.append(pd.read_parquet(f))
        except Exception as e:
            print(f"Skipping {f.name}: {e}")

    df = pd.concat(parquets, ignore_index=True)
    logger.info(f"Total rows loaded: {len(df)}")

    df["year"] = df["date_filed"].astype(str).str.extract(r"(\d{4})")[0].astype(int)
    df = df[df["court_type"] == "S"]

    # Add flat opinion_text column for Wordscores (keeps nested opinions for EMI)
    logger.info("Extracting opinion text...")
    df["opinion_text"] = df["opinions"].apply(extract_text)

    # Load and merge CF-scores
    dime = load_dime()
    logger.info(f"Unique supreme court justices in DIME: {len(dime)}")

    # Extract state abbreviation from court_jurisdiction e.g. "Tennessee, TN" -> "TN"
    df["state"] = df["court_jurisdiction"].str.extract(r",\s*([A-Z]{2})$")

    # Explode judges column into one row per judge
    df["judges_list"] = df["judges"].str.split(",")
    df_exploded = df.explode("judges_list")
    df_exploded["last_name"] = (
        df_exploded["judges_list"].str.strip().str.split().str[0].str.title()
    )

    # Merge on last name and state (left join to keep all opinions)
    df_exploded = df_exploded.merge(
        dime,
        left_on=["last_name", "state"],
        right_on=["last_name", "recipient.state"],
        how="left",
    )

    logger.info(f"Unique justices matched: {df_exploded['last_name'].nunique()}")
    logger.info(
        f"Rows with CF-scores: {df_exploded['candidate.cfscore'].notna().sum()} "
        f"/ {len(df_exploded)}"
    )

    # Add absolute CF-score column (ideological intensity, distance from zero)
    df_exploded["abs_cfscore"] = df_exploded["candidate.cfscore"].abs()

    df_exploded.to_parquet(PROCESSED_DATA_DIR / "dataset.parquet")
    logger.success(f"Saved dataset to {PROCESSED_DATA_DIR / 'dataset.parquet'}")


if __name__ == "__main__":
    main()
from pathlib import Path
import pandas as pd
import pyarrow.dataset as ds
import typer
from loguru import logger
from tqdm import tqdm
from dissent.config import RAW_DATA_DIR, PROCESSED_DATA_DIR, INTERIM_DATA_DIR

app = typer.Typer()

STATE_ABBREV_TO_NAME = {
    "AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas",
    "CA": "California", "CO": "Colorado", "CT": "Connecticut", "DE": "Delaware",
    "FL": "Florida", "GA": "Georgia", "HI": "Hawaii", "ID": "Idaho",
    "IL": "Illinois", "IN": "Indiana", "IA": "Iowa", "KS": "Kansas",
    "KY": "Kentucky", "LA": "Louisiana", "ME": "Maine", "MD": "Maryland",
    "MA": "Massachusetts", "MI": "Michigan", "MN": "Minnesota", "MS": "Mississippi",
    "MO": "Missouri", "MT": "Montana", "NE": "Nebraska", "NV": "Nevada",
    "NH": "New Hampshire", "NJ": "New Jersey", "NM": "New Mexico", "NY": "New York",
    "NC": "North Carolina", "ND": "North Dakota", "OH": "Ohio", "OK": "Oklahoma",
    "OR": "Oregon", "PA": "Pennsylvania", "RI": "Rhode Island", "SC": "South Carolina",
    "SD": "South Dakota", "TN": "Tennessee", "TX": "Texas", "UT": "Utah",
    "VT": "Vermont", "VA": "Virginia", "WA": "Washington", "WV": "West Virginia",
    "WI": "Wisconsin", "WY": "Wyoming"
}

GARBAGE_TOKENS = {
    "per", "curiam", "percuriam", "and", "c.j.", "p.j.", "jj.", "j.",
    "chief", "associate", "senior", "justice", "justices", "judge", "judges",
    "hon", "honorable", "writ", "consideration", "grant", "granted",
    "the", "court", "by", "in", "of", "with", "for"
}

DISSENT_TYPES = {"040dissent", "035concurrenceinpart"}


def normalize_name(name):
    """
    Normalize justice names for matching by lowercasing and
    removing apostrophes and spaces.
    """
    if pd.isna(name):
        return None
    return name.lower().replace("'", "").replace(" ", "").strip()


def extract_last_name(name_str):
    """
    Extract last name from a judge name string, handling common formatting
    issues in the COLD Cases judges field:
    - Strips titles and honorifics (C.J., P.J., Hon., etc.)
    - Reconstructs multi-part names (O'Connor, Van de Walle, Mc names)
    - Returns None for garbage tokens
    """
    if pd.isna(name_str):
        return None

    parts = name_str.strip().split()
    if not parts:
        return None

    parts = [p for p in parts if p.lower().rstrip(".") not in GARBAGE_TOKENS]
    if not parts:
        return None

    name = " ".join(parts)

    if len(parts) == 2 and parts[0].lower() in {"o", "mc", "mac", "de", "van", "von", "la", "le"}:
        name = "".join(parts)

    return name.strip().title() if name.strip() else None


def load_pajid():
    """
    Load PAJID ideology scores (Brace, Langer & Hall 2000).
    Covers all 50 state supreme courts 1970-2019.
    Returns one row per judge-year with normalized name for matching.
    Higher PAJID = more liberal, 50 = ideological center.
    """
    pajid = pd.read_csv(RAW_DATA_DIR / "ideology_data.csv")
    pajid = pajid[pajid["pajid"].notna()]
    pajid["last_name_normalized"] = pajid["j_name"].apply(normalize_name)
    return pajid[["statename", "year", "last_name_normalized", "pajid"]]


def extract_text(opinions):
    """Extract dissent and concurrence-in-part opinion text."""
    if opinions is None:
        return None
    texts = []
    for o in opinions:
        if isinstance(o, dict):
            if o.get("type") in DISSENT_TYPES:
                t = o.get("opinion_text")
                if t:
                    texts.append(t)
    return texts if texts else None


def main():
    """
    Load opinion shards and combine them into a single dataframe, filter
    by year (1965-2025) and court type, merge PAJID ideology scores onto
    opinions by matching judge last name, state, and year, and explode
    to one row per individual opinion.

    Output guarantees:
    - One row per dissent or concurrence-in-part opinion (exploded from nested opinions column)
    - One row per judge per opinion (exploded on judges)
    - pajid is NULL if justice not matched in PAJID dataset
    - abs_pajid is the absolute deviation from 50 (ideological intensity)
    - opinion_text is the text of the individual opinion (for Wordscores)
    """
    pajid = load_pajid()
    logger.info(f"Unique judge-years in PAJID: {len(pajid)}")

    temp_dir = INTERIM_DATA_DIR / "temp_processed"
    temp_dir.mkdir(exist_ok=True)

    for f in tqdm(sorted(INTERIM_DATA_DIR.rglob("shard_*.parquet"))):
        try:
            df_shard = pd.read_parquet(f)
            df_shard["year"] = df_shard["date_filed"].astype(str).str.extract(r"(\d{4})")[0].astype(int)
            df_shard = df_shard[(df_shard["year"] >= 1965) & (df_shard["year"] <= 2025)]
            df_shard = df_shard[df_shard["court_type"] == "S"]
            df_shard["opinion_text"] = df_shard["opinions"].apply(extract_text)
            df_shard = df_shard[df_shard["opinion_text"].notna()]
            df_shard = df_shard.explode("opinion_text")
            df_shard = df_shard.drop(columns=["opinions"])
            df_shard.to_parquet(temp_dir / f.name)
        except Exception as e:
            logger.warning(f"Skipping {f.name}: {e}")

    logger.info("Loading processed shards...")
    dataset = ds.dataset(temp_dir, format="parquet")
    df = dataset.to_table().to_pandas()
    logger.info(f"Total rows loaded: {len(df)}")

    df["state"] = df["court_jurisdiction"].str.extract(r",\s*([A-Z]{2})$")
    df["statename"] = df["state"].map(STATE_ABBREV_TO_NAME)

    df["judges_list"] = df["judges"].str.split(",")
    df_exploded = df.explode("judges_list")
    del df

    df_exploded["last_name"] = df_exploded["judges_list"].apply(extract_last_name)
    df_exploded = df_exploded.dropna(subset=["last_name"])
    df_exploded["last_name_normalized"] = df_exploded["last_name"].apply(normalize_name)

    df_exploded = df_exploded.merge(
        pajid,
        on=["statename", "year", "last_name_normalized"],
        how="left",
    )

    match_rate = df_exploded["pajid"].notna().mean()
    logger.info(f"Unique justices matched: {df_exploded['last_name'].nunique()}")
    logger.info(
        f"Rows with PAJID scores: {df_exploded['pajid'].notna().sum()} "
        f"/ {len(df_exploded)} ({match_rate:.2%})"
    )

    df_exploded["abs_pajid"] = (df_exploded["pajid"] - 50).abs()

    df_exploded.to_parquet(PROCESSED_DATA_DIR / "dataset.parquet")
    logger.success(f"Saved dataset to {PROCESSED_DATA_DIR / 'dataset.parquet'}")


if __name__ == "__main__":
    main()
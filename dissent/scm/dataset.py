# Make data

# Import packages

from loguru import logger
import typer
import sys
import pandas as pd
import numpy as np

from dissent.config import PROCESSED_DATA_DIR, INTERIM_DATA_DIR

app = typer.Typer()


def load_dataset(filename: str, description: str) -> pd.DataFrame:
    """Load a CSV file with error handling and logging."""
    try:
        df = pd.read_csv((INTERIM_DATA_DIR / "scm" / filename))
        logger.success(f"{description} found")
        return df
    except FileNotFoundError:
        logger.critical(f"{description} not found")
        sys.exit(1)

@app.command()
def main():
    # Define datasets to load
    datasets = {
        "campaignfinance": ("campaignfinance.csv", "Campaign finance data"),
        "courtprof": ("courtprof.csv", "Court professionalization data"),
        "capappeals": ("capappeals.csv", "Capital appeals data"),
        "caplowerlag1": ("caplowerlag1.csv", "Lower court capital appeals data"),
        "dissents": ("docket.csv", "Number of opinions, number of dissents, and criminal procedure docket data"),
        "ideospread": ("ideospread.csv", "Ideological spread data"),
        "citizenideo": ("citizenideo.csv", "Citizen ideology data"),
        "govtideo": ("govtideo.csv", "Government ideology data"),
        "misc": ("misc.csv", "Term length, number of justices, election structure, and election competitiveness data"),
    }
    
    # Load all datasets
    dfs = {key: load_dataset(filename, desc) for key, (filename, desc) in datasets.items()}
    
    # Merge datasets sequentially
    merge_order = ["campaignfinance", "courtprof", "capappeals", "caplowerlag1", 
                   "dissents", "ideospread", "citizenideo", "govtideo", "misc"]
    
    df = dfs[merge_order[0]]
    for dataset_name in merge_order[1:]:
        df = pd.merge(df, dfs[dataset_name], on=["Year", "Court"])
    
    logger.success("Merged successfully")
    
    # Compute ratios
    
    df["DissentRate"] = df["Dissents"] / df["Opinions"]
    
    # Explicitly set to 0 when Opinions is 0 (to avoid NaN from 0/0)
    df.loc[df["Opinions"] == 0, "DissentRate"] = 0.0

    
    # Save final dataset
    df.to_csv(PROCESSED_DATA_DIR / "scm_dataset.csv", index=False)
    logger.success("Dataset saved successfully")


if __name__ == "__main__":
    app()
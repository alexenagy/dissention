"""
NC dissent rate over time, using SCM dataset.

Reads the merged SCM dataset from data/processed/scm_dataset.csv and
plots the annual dissent rate for North Carolina as a simple line chart.
"""

import matplotlib.pyplot as plt
import pandas as pd
from dissent.config import PROCESSED_DATA_DIR, FIGURES_DIR


def main() -> None:
    # Load SCM dataset (output of dissent.scm.dataset.main)
    df = pd.read_csv(PROCESSED_DATA_DIR / "scm_dataset.csv")

    nc = df[df["Court"] == "NC"].copy()
    nc = nc.sort_values("Year")

    # Ensure DissentRate column exists (older files may not have it)
    if "DissentRate" not in nc.columns:
        nc["DissentRate"] = nc["Dissents"] / nc["Opinions"]
        nc.loc[nc["Opinions"] == 0, "DissentRate"] = 0.0

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(nc["Year"], nc["DissentRate"], color="black", linewidth=2)

    ax.set_xlabel("Year")
    ax.set_ylabel("Proportion of Published Opinions\nAccompanied by a Dissent")
    ax.set_title("North Carolina Dissent Rate Over Time")

    ax.set_xlim(nc["Year"].min(), nc["Year"].max())
    ax.set_ylim(0, max(0.06, nc["DissentRate"].max() * 1.1))

    ax.set_xticks(sorted(nc["Year"].unique()))
    ax.tick_params(axis="x", rotation=45)

    out_path = FIGURES_DIR / "nc_dissent_rate.png"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(out_path, dpi=300)
    plt.close(fig)
    print(f"Saved: {out_path}")


if __name__ == "__main__":
    main()


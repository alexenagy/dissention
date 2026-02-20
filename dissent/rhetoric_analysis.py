"""
Compare EMI across judicial selection methods (partisan, nonpartisan, appointment).

Loads EMI data merged with selection_mechanisms.csv,
then computes descriptive statistics and statistical tests.
"""

import pandas as pd
from scipy import stats

from dissent.config import INTERIM_DATA_DIR, PROCESSED_DATA_DIR
from dissent.rhetoric_over_time import (
    court_to_state_abbrev,
    load_selection_methods,
    SELECTION_LABELS,
)


def load_emi_by_selection() -> pd.DataFrame:
    """Load EMI parquet, merge with selection method; return df with year, emi, selection_mechanism."""
    emi = pd.read_parquet(PROCESSED_DATA_DIR / "processed_parquets_emi.parquet")
    emi = emi.dropna(subset=["emi", "year", "court_jurisdiction"]).copy()
    emi["court"] = emi["court_jurisdiction"].apply(court_to_state_abbrev)
    emi = emi.dropna(subset=["court"])
    emi["year"] = emi["year"].astype(int)
    selection = load_selection_methods()
    emi = emi.merge(
        selection,
        on=["year", "court"],
        how="inner",
    )
    return emi[["year", "rhetoric_score", "selection_mechanism"]].copy()


def descriptive_stats(df: pd.DataFrame) -> pd.DataFrame:
    """Summary statistics by selection mechanism."""
    return (
        df.groupby("selection_mechanism")["rhetoric_score"]
        .agg(
            [
                ("count", "count"),
                ("mean", "mean"),
                ("median", "median"),
                ("std", "std"),
                ("min", "min"),
                ("max", "max"),
                ("q25", lambda x: x.quantile(0.25)),
                ("q75", lambda x: x.quantile(0.75)),
            ]
        )
        .round(4)
    )


def run_kruskal_wallis(df: pd.DataFrame) -> tuple[float, float]:
    """Kruskal-Wallis H-test: do EMI distributions differ across selection methods? Returns (statistic, p-value)."""
    groups = [df.loc[df["selection_mechanism"] == code, "emi"].values for code in SELECTION_LABELS]
    groups = [g[~pd.isna(g)] for g in groups if len(g) > 0]
    if len(groups) < 2:
        return float("nan"), float("nan")
    return stats.kruskal(*groups)


def run_pairwise_mannwhitney(df: pd.DataFrame) -> pd.DataFrame:
    """Pairwise Mann-Whitney U tests between selection methods. Returns table of p-values."""
    codes = list(SELECTION_LABELS.keys())
    results = []
    for i, a in enumerate(codes):
        for b in codes[i + 1:]:
            da = df.loc[df["selection_mechanism"] == a, "emi"].dropna()
            db = df.loc[df["selection_mechanism"] == b, "emi"].dropna()
            if len(da) < 2 or len(db) < 2:
                continue
            stat, p = stats.mannwhitneyu(da, db, alternative="two-sided")
            results.append(
                {
                    "method_a": SELECTION_LABELS[a],
                    "method_b": SELECTION_LABELS[b],
                    "statistic": round(stat, 4),
                    "p_value": round(p, 4),
                }
            )
    return pd.DataFrame(results)


def main():
    df = load_emi_by_selection()

    # Descriptive statistics
    desc = descriptive_stats(df)
    print("--- Descriptive statistics by selection method ---")
    print(desc.to_string())
    print()

    # Kruskal-Wallis (overall difference)
    h, p = run_kruskal_wallis(df)
    print("--- Kruskal-Wallis H-test (EMI differs across methods?) ---")
    print(f"H = {h:.4f}, p = {p:.4f}")
    if p < 0.05:
        print("Result: Distributions differ significantly across selection methods (p < 0.05).")
    else:
        print("Result: No significant difference across methods (p >= 0.05).")
    print()

    # Pairwise comparisons
    pairwise = run_pairwise_mannwhitney(df)
    print("--- Pairwise Mann-Whitney U (two-sided) ---")
    print(pairwise.to_string(index=False))
    print()

    # Save summary tables
    INTERIM_DATA_DIR.mkdir(parents=True, exist_ok=True)
    desc_path = INTERIM_DATA_DIR / "emi_by_selection_method_summary.csv"
    desc.to_csv(desc_path)
    print(f"Saved summary table: {desc_path}")

    pairwise_path = INTERIM_DATA_DIR / "emi_by_selection_method_pairwise_tests.csv"
    pairwise.to_csv(pairwise_path, index=False)
    print(f"Saved pairwise tests: {pairwise_path}")


if __name__ == "__main__":
    main()
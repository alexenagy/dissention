'''
rhetoric_trend_significance.py

Analysis 2: Panel OLS trend regressions and level differences by selection mechanism.

PART A: Time trends
For each mechanism, fits a panel regression of raw rhetoric score on year
with state fixed effects and SEs clustered by state.

State fixed effects absorb time-invariant differences between courts so the
year coefficient captures within-state change over time, not cross-sectional
differences between states.

Clustered SEs account for serial correlation within states.

PART B: Level differences
Tests whether mechanism type predicts rhetoric level within states, using
only states that ever switched mechanism for identification. Nonpartisan is
the reference category. Controls for state FE and year.

Negative scores = more ideological
Positive scores = more conventional
Sample restricted to 1965-2019 for consistent court coverage.
'''

import pandas as pd
import statsmodels.formula.api as smf
from dissent.config import PROCESSED_DATA_DIR, INTERIM_DATA_DIR


MECHANISM_LABELS = {
    "P": "Partisan Elections",
    "N": "Nonpartisan Elections",
    "A": "Appointment",
    "R": "Retention",
}


def court_to_state_abbrev(court_jurisdiction):
    if pd.isna(court_jurisdiction):
        return None
    s = str(court_jurisdiction).strip()
    return s.split(", ")[-1].strip() if ", " in s else None


def sig_stars(p):
    return "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else "†" if p < 0.1 else ""


def main():
    print("Loading data...")
    rhetoric = pd.read_parquet(PROCESSED_DATA_DIR / "rhetoric_scores.parquet")
    rhetoric = rhetoric.dropna(subset=["rhetoric_score", "year", "court_jurisdiction"]).copy()
    rhetoric["court"] = rhetoric["court_jurisdiction"].apply(court_to_state_abbrev)
    rhetoric = rhetoric.dropna(subset=["court"])
    rhetoric["year"] = rhetoric["year"].astype(int)
    rhetoric = rhetoric[rhetoric["year"] <= 2019]

    # Annual mean raw score per state-year
    annual = (
        rhetoric.groupby(["court", "year"])["rhetoric_score"]
        .mean()
        .reset_index()
        .rename(columns={"rhetoric_score": "mean_score"})
    )

    selection = pd.read_csv(INTERIM_DATA_DIR / "selection_mechanisms.csv")
    df = annual.merge(selection, on=["year", "court"], how="inner")

    # -------------------------------------------------------------------------
    # PART A: TIME TRENDS
    # -------------------------------------------------------------------------
    print("=== Part A: Time Trends by Selection Mechanism ===")
    print("(Panel OLS with state fixed effects, SEs clustered by state)")
    print("Dependent variable: annual mean rhetoric score\n")
    print(f"{'Mechanism':<28} {'β(year)':>10} {'Cluster SE':>12} {'t':>8} {'p':>8} {'Sig':<6} {'N states':>9} {'N obs':>7}")
    print("-" * 85)

    # Overall trend — no fixed effects, opinion-level
    overall = smf.ols("rhetoric_score ~ year", data=rhetoric).fit()
    b, se, t, p = overall.params["year"], overall.bse["year"], overall.tvalues["year"], overall.pvalues["year"]
    print(f"{'Overall (no FE)':<28} {b:>10.6f} {se:>12.6f} {t:>8.3f} {p:>8.4f} {sig_stars(p):<6} {rhetoric['court'].nunique():>9} {len(rhetoric):>7}")
    print("-" * 85)

    for mech in ["P", "N", "A", "R"]:
        subset = df[df["selection_mechanism"] == mech].copy()
        n_states = subset["court"].nunique()
        n_obs = len(subset)
        if n_states < 2 or n_obs < 10:
            print(f"{MECHANISM_LABELS[mech]:<28} {'insufficient data':>10}")
            continue
        m = smf.ols("mean_score ~ year + C(court)", data=subset).fit(
            cov_type="cluster",
            cov_kwds={"groups": subset["court"]}
        )
        b, se, t, p = m.params["year"], m.bse["year"], m.tvalues["year"], m.pvalues["year"]
        print(f"{MECHANISM_LABELS[mech]:<28} {b:>10.6f} {se:>12.6f} {t:>8.3f} {p:>8.4f} {sig_stars(p):<6} {n_states:>9} {n_obs:>7}")

    # -------------------------------------------------------------------------
    # PART B: LEVEL DIFFERENCES
    # -------------------------------------------------------------------------
    print("\n=== Part B: Level Differences by Selection Mechanism ===")
    print("(Panel OLS with state fixed effects and year control, SEs clustered by state)")
    print("Dependent variable: annual mean rhetoric score")
    print("Reference category: Nonpartisan (N)\n")

    switcher_states = df.groupby("court")["selection_mechanism"].nunique()
    switchers = switcher_states[switcher_states > 1].index
    df_switchers = df[df["court"].isin(switchers)].copy()

    print(f"States with mechanism switches (used for identification): {len(switchers)}")
    print(f"Total state-year observations: {len(df_switchers)}\n")

    m_levels = smf.ols(
        "mean_score ~ C(selection_mechanism, Treatment('N')) + year + C(court)",
        data=df_switchers
    ).fit(
        cov_type="cluster",
        cov_kwds={"groups": df_switchers["court"]}
    )

    print(f"{'Mechanism vs. Nonpartisan':<35} {'β':>10} {'Cluster SE':>12} {'t':>8} {'p':>8} {'Sig':<6}")
    print("-" * 75)

    for mech, label in [("A", "Appointment"), ("R", "Retention"), ("P", "Partisan Elections")]:
        param_name = f"C(selection_mechanism, Treatment('N'))[T.{mech}]"
        if param_name not in m_levels.params:
            print(f"{label:<35} {'(not identified)':>10}")
            continue
        b, se, t, p = m_levels.params[param_name], m_levels.bse[param_name], m_levels.tvalues[param_name], m_levels.pvalues[param_name]
        print(f"{label:<35} {b:>10.6f} {se:>12.6f} {t:>8.3f} {p:>8.4f} {sig_stars(p):<6}")

    print("\n--- Raw mean rhetoric score by mechanism (unadjusted) ---")
    raw_means = df.groupby("selection_mechanism")["mean_score"].mean().sort_values()
    for mech, val in raw_means.items():
        print(f"  {MECHANISM_LABELS[mech]:<28} {val:>8.4f}")


if __name__ == "__main__":
    main()
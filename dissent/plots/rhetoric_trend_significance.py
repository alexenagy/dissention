'''
rhetoric_trend_significance.py

Analysis 2: Panel OLS trend regressions and level differences by selection mechanism.

PART A: Time trends
For each mechanism, fits a panel regression of annual mean rhetoric score on year
with state fixed effects and SEs clustered by state.

State fixed effects absorb time-invariant differences between courts so the
year coefficient captures within-state change over time, not cross-sectional
differences between states.

Clustered SEs account for serial correlation within states.

PART B: Level differences — electoral vs. appointment regimes
Tests whether mechanism type predicts rhetoric level within states.
Uses the full sample (not restricted to switchers) because appointment and
retention courts rarely switch, so restricting to switchers would drop the
courts most relevant to the electoral vs. appointment comparison.

Two contrast models are estimated:
  Model 1: Nonpartisan as reference — tests appointment and retention vs.
           any electoral regime, and partisan vs. nonpartisan specifically.
  Model 2: Partisan as reference — directly estimates the partisan vs.
           nonpartisan contrast and its relation to appointment/retention.

Controls for state FE and year in both models.

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


def run_level_model(df, reference, label):
    '''Run panel OLS level regression with given reference category.'''
    print(f"\n--- Model: reference = {label} ---")
    print(f"{'Mechanism':<35} {'β':>10} {'Cluster SE':>12} {'t':>8} {'p':>8} {'Sig':<6}")
    print("-" * 75)

    m = smf.ols(
        f"mean_score ~ C(selection_mechanism, Treatment('{reference}')) + year + C(court)",
        data=df
    ).fit(
        cov_type="cluster",
        cov_kwds={"groups": df["court"]}
    )

    mechs = [k for k in ["P", "N", "A", "R"] if k != reference]
    for mech in mechs:
        label_str = MECHANISM_LABELS[mech]
        param_name = f"C(selection_mechanism, Treatment('{reference}'))[T.{mech}]"
        if param_name not in m.params:
            print(f"{label_str:<35} {'(not identified)':>10}")
            continue
        b = m.params[param_name]
        se = m.bse[param_name]
        t = m.tvalues[param_name]
        p = m.pvalues[param_name]
        print(f"{label_str:<35} {b:>10.6f} {se:>12.6f} {t:>8.3f} {p:>8.4f} {sig_stars(p):<6}")

    print(f"\n  N states: {df['court'].nunique()}   N obs: {len(df)}")
    return m


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
    print("\n=== Part A: Time Trends by Selection Mechanism ===")
    print("(Panel OLS with state fixed effects and SEs clustered by state)")
    print("Dependent variable: annual mean rhetoric score\n")
    print(f"{'Mechanism':<28} {'β(year)':>10} {'Cluster SE':>12} {'t':>8} {'p':>8} {'Sig':<6} {'N states':>9} {'N obs':>7}")
    print("-" * 85)

    # Overall trend — annual means with state FE, consistent with mechanism models
    overall_m = smf.ols("mean_score ~ year + C(court)", data=df).fit(
        cov_type="cluster",
        cov_kwds={"groups": df["court"]}
    )
    b = overall_m.params["year"]
    se = overall_m.bse["year"]
    t = overall_m.tvalues["year"]
    p = overall_m.pvalues["year"]
    print(f"{'Overall (state FE)':<28} {b:>10.6f} {se:>12.6f} {t:>8.3f} {p:>8.4f} {sig_stars(p):<6} {df['court'].nunique():>9} {len(df):>7}")
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
        b = m.params["year"]
        se = m.bse["year"]
        t = m.tvalues["year"]
        p = m.pvalues["year"]
        print(f"{MECHANISM_LABELS[mech]:<28} {b:>10.6f} {se:>12.6f} {t:>8.3f} {p:>8.4f} {sig_stars(p):<6} {n_states:>9} {n_obs:>7}")

    # -------------------------------------------------------------------------
    # PART B: LEVEL DIFFERENCES
    # -------------------------------------------------------------------------
    print("\n=== Part B: Level Differences by Selection Mechanism ===")
    print("(Panel OLS with state fixed effects and year control, SEs clustered by state)")
    print("Dependent variable: annual mean rhetoric score")
    print("Full sample used — restricting to switchers would drop appointment/retention")
    print("courts that are central to the electoral vs. appointment comparison.\n")

    print("--- Raw mean rhetoric score by mechanism (unadjusted) ---")
    raw_means = df.groupby("selection_mechanism")["mean_score"].mean().sort_values(ascending=False)
    for mech, val in raw_means.items():
        print(f"  {MECHANISM_LABELS.get(mech, mech):<28} {val:>8.4f}")

    # Model 1: Nonpartisan reference
    # Tests appointment/retention vs. electoral regimes broadly,
    # and partisan vs. nonpartisan specifically
    run_level_model(df, reference="N", label="Nonpartisan")

    # Model 2: Partisan reference
    # Directly estimates partisan vs. nonpartisan contrast
    # and partisan vs. appointment/retention
    run_level_model(df, reference="P", label="Partisan")


if __name__ == "__main__":
    main()
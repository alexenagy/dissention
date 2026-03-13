'''
rhetoric_pajid_regression.py

Mediation analysis testing whether ideological spread mediates the effect
of selection mechanisms on rhetoric scores.

Theory: Partisan elections -> court homogeneity -> conventional rhetoric

Three steps:
  Step 1: Does selection mechanism predict ideological spread?
          (Does the mechanism cause homogeneity?)
  Step 2: Does ideological spread predict rhetoric?
          (Does homogeneity cause conventional rhetoric?)
  Step 3: Does mechanism effect on rhetoric shrink when spread is added?
          (Is spread mediating the relationship?)

All models use simple OLS with SEs clustered by state.
No fixed effects -- we are testing between-state structural differences.
Reference category: Nonpartisan Elections (N)
'''

import pandas as pd
import statsmodels.formula.api as smf
from scipy import stats
from dissent.config import PROCESSED_DATA_DIR, INTERIM_DATA_DIR, RAW_DATA_DIR


STATE_ABBREV = {
    'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR',
    'California': 'CA', 'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE',
    'Florida': 'FL', 'Georgia': 'GA', 'Hawaii': 'HI', 'Idaho': 'ID',
    'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA', 'Kansas': 'KS',
    'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD',
    'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS',
    'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV',
    'New Hampshire': 'NH', 'New Jersey': 'NJ', 'New Mexico': 'NM', 'New York': 'NY',
    'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH', 'Oklahoma': 'OK',
    'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC',
    'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT',
    'Vermont': 'VT', 'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV',
    'Wisconsin': 'WI', 'Wyoming': 'WY'
}


def court_to_state_abbrev(court_jurisdiction):
    if pd.isna(court_jurisdiction):
        return None
    s = str(court_jurisdiction).strip()
    return s.split(", ")[-1].strip() if ", " in s else None


def main():
    print("Loading rhetoric scores...")
    rhetoric = pd.read_parquet(PROCESSED_DATA_DIR / "rhetoric_scores.parquet")
    rhetoric = rhetoric.dropna(subset=["rhetoric_score", "year", "court_jurisdiction"]).copy()
    rhetoric["court"] = rhetoric["court_jurisdiction"].apply(court_to_state_abbrev)
    rhetoric = rhetoric.dropna(subset=["court"])
    rhetoric["year"] = rhetoric["year"].astype(int)
    rhetoric = rhetoric[rhetoric["year"] <= 2019]

    annual_rhetoric = (
        rhetoric.groupby(["court", "year"])["rhetoric_score"]
        .mean()
        .reset_index()
        .rename(columns={"rhetoric_score": "mean_rhetoric"})
    )

    print("Loading PAJID data...")
    pajid = pd.read_csv(RAW_DATA_DIR / "ideology_data.csv")
    pajid = pajid.dropna(subset=["pajid"])
    pajid["court"] = pajid["statename"].map(STATE_ABBREV)
    pajid = pajid.dropna(subset=["court"])

    spread = pajid.groupby(["court", "year"]).agg(
        pajid_spread=("pajid", lambda x: x.max() - x.min()),
    ).reset_index()

    df = annual_rhetoric.merge(spread, on=["court", "year"], how="inner")

    selection = pd.read_csv(INTERIM_DATA_DIR / "selection_mechanisms.csv")
    df = df.merge(selection, on=["court", "year"], how="left")

    df = df.dropna(subset=["selection_mechanism", "pajid_spread"])
    df = df[df["selection_mechanism"].isin(["P", "N", "A", "R"])]
    df["mech"] = df["selection_mechanism"]

    print(f"N observations: {len(df)}")
    print(f"N courts: {df['court'].nunique()}")
    print(f"Years: {df['year'].min()}-{df['year'].max()}")

    # =========================================================================
    # STEP 1: Does selection mechanism predict ideological spread?
    #
    # This tests the first link in the causal chain: do different selection
    # systems produce courts with different levels of ideological diversity?
    # The outcome is pajid_spread (max - min PAJID score per court-year).
    # If partisan elections produce homogenous courts, we expect a significant
    # negative coefficient on partisan elections relative to nonpartisan.
    # =========================================================================
    print("\n" + "="*70)
    print("STEP 1: Does mechanism predict ideological spread?")
    print("Outcome: pajid_spread (max - min PAJID per court-year)")
    print("Simple OLS, SEs clustered by state")
    print("Reference category: Nonpartisan Elections (N)")
    print("="*70)

    m1 = smf.ols(
        "pajid_spread ~ C(mech, Treatment('N'))",
        data=df
    ).fit(cov_type="cluster", cov_kwds={"groups": df["court"]})

    for mech, label in [("P", "Partisan Elections"), ("A", "Appointment"), ("R", "Retention")]:
        key = f"C(mech, Treatment('N'))[T.{mech}]"
        if key in m1.params:
            sig = "***" if m1.pvalues[key] < 0.001 else "**" if m1.pvalues[key] < 0.01 else "*" if m1.pvalues[key] < 0.05 else "+" if m1.pvalues[key] < 0.1 else ""
            print(f"  {label}: beta = {m1.params[key]:.4f}, "
                  f"SE = {m1.bse[key]:.4f}, "
                  f"t = {m1.tvalues[key]:.3f}, "
                  f"p = {m1.pvalues[key]:.4f} {sig}")
    print(f"N = {int(m1.nobs)}, R2 = {m1.rsquared:.4f}")

    # =========================================================================
    # STEP 2: Does ideological spread predict rhetoric?
    #
    # This tests the second link: do more ideologically diverse courts write
    # more ideologically in their dissents? The outcome is mean rhetoric score.
    # Mechanism dummies are included as controls so we are not confounding
    # spread with the mechanism effect. If spread predicts rhetoric after
    # controlling for mechanism, it is doing independent work.
    # =========================================================================
    print("\n" + "="*70)
    print("STEP 2: Does ideological spread predict rhetoric?")
    print("Outcome: mean rhetoric score")
    print("Simple OLS controlling for mechanism, SEs clustered by state")
    print("="*70)

    m2 = smf.ols(
        "mean_rhetoric ~ pajid_spread + C(mech, Treatment('N'))",
        data=df
    ).fit(cov_type="cluster", cov_kwds={"groups": df["court"]})

    print(f"  Ideological spread: beta = {m2.params['pajid_spread']:.4f}, "
          f"SE = {m2.bse['pajid_spread']:.4f}, "
          f"t = {m2.tvalues['pajid_spread']:.3f}, "
          f"p = {m2.pvalues['pajid_spread']:.4f}")
    print(f"N = {int(m2.nobs)}, R2 = {m2.rsquared:.4f}")

    # =========================================================================
    # STEP 3: Does the mechanism effect on rhetoric shrink when spread is added?
    #
    # This tests mediation directly. First we estimate the mechanism effect
    # on rhetoric WITHOUT spread (baseline). Then we add spread and check
    # whether the mechanism coefficients shrink. If they do, spread is
    # mediating part of the relationship between mechanism and rhetoric.
    # If they stay the same, spread is not on the causal pathway.
    # =========================================================================
    print("\n" + "="*70)
    print("STEP 3: Does adding spread shrink the mechanism effect?")
    print("Comparing mechanism effects with and without spread")
    print("Outcome: mean rhetoric score")
    print("Simple OLS, SEs clustered by state")
    print("="*70)

    m3a = smf.ols(
        "mean_rhetoric ~ C(mech, Treatment('N'))",
        data=df
    ).fit(cov_type="cluster", cov_kwds={"groups": df["court"]})

    m3b = smf.ols(
        "mean_rhetoric ~ pajid_spread + C(mech, Treatment('N'))",
        data=df
    ).fit(cov_type="cluster", cov_kwds={"groups": df["court"]})

    print(f"\n{'Mechanism':<25} {'Without spread':>15} {'With spread':>15} {'Change':>10}")
    print("-"*65)
    for mech, label in [("P", "Partisan"), ("A", "Appointment"), ("R", "Retention")]:
        key = f"C(mech, Treatment('N'))[T.{mech}]"
        if key in m3a.params and key in m3b.params:
            b_without = m3a.params[key]
            b_with = m3b.params[key]
            change = b_with - b_without
            print(f"  {label:<23} {b_without:>15.4f} {b_with:>15.4f} {change:>10.4f}")

    # =========================================================================
    # DESCRIPTIVE: Mean spread and rhetoric by mechanism
    # =========================================================================
    print("\n" + "="*70)
    print("DESCRIPTIVE: Mean spread and rhetoric by mechanism")
    print("="*70)
    desc = df.groupby("mech").agg(
        mean_spread=("pajid_spread", "mean"),
        mean_rhetoric=("mean_rhetoric", "mean"),
        n=("mean_rhetoric", "count")
    ).round(3)
    print(desc)

    # =========================================================================
    # T-TESTS: Is nonpartisan spread significantly different from other mechanisms?
    # =========================================================================
    print("\n" + "="*70)
    print("T-TESTS: Ideological spread -- Nonpartisan vs each mechanism")
    print("="*70)
    nonpartisan = df[df["mech"] == "N"]["pajid_spread"]
    for mech, label in [("P", "Partisan"), ("A", "Appointment"), ("R", "Retention")]:
        group = df[df["mech"] == mech]["pajid_spread"]
        t, p = stats.ttest_ind(nonpartisan, group)
        diff = nonpartisan.mean() - group.mean()
        sig = "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else "+" if p < 0.1 else ""
        print(f"  Nonpartisan vs {label}: diff = {diff:.3f}, t = {t:.3f}, p = {p:.4f} {sig}")


if __name__ == "__main__":
    main()
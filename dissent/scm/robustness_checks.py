"""
Approximate Python translation of `scm_robustness_checks.R`.

This module:
  - loads the merged SCM dataset,
  - builds an equal-weights synthetic control for NC,
  - reports pre/post MSPE and average treatment effect,
  - runs simple placebo and leave-one-out checks.

It does NOT implement the optimized Synth weights; instead it uses the
equal-weight synthetic that the R script also reports as a robustness check.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List

import numpy as np
import pandas as pd
from dissent.config import PROCESSED_DATA_DIR


TREATMENT_YEAR = 2018


@dataclass
class SCMResults:
    years: np.ndarray
    treated: np.ndarray
    synthetic: np.ndarray
    pre_years: np.ndarray
    post_years: np.ndarray


def load_scm_dataset() -> pd.DataFrame:
    df = pd.read_csv(PROCESSED_DATA_DIR / "scm_dataset.csv")
    # Ensure required columns exist
    if "DissentRate" not in df.columns:
        df["DissentRate"] = df["Dissents"] / df["Opinions"]
        df.loc[df["Opinions"] == 0, "DissentRate"] = 0.0
    return df


def build_equal_weight_synth(df: pd.DataFrame) -> SCMResults:
    years = np.sort(df["Year"].unique())

    treated = []
    synthetic = []
    for year in years:
        year_df = df[df["Year"] == year]
        nc_rate = year_df.loc[year_df["Court"] == "NC", "DissentRate"].mean()
        ctrl_rates = year_df.loc[year_df["Court"] != "NC", "DissentRate"].dropna()
        treated.append(nc_rate)
        synthetic.append(ctrl_rates.mean() if len(ctrl_rates) else np.nan)

    treated_arr = np.asarray(treated, dtype=float)
    synthetic_arr = np.asarray(synthetic, dtype=float)

    pre_years = years[years < TREATMENT_YEAR]
    post_years = years[years >= TREATMENT_YEAR]

    return SCMResults(
        years=years,
        treated=treated_arr,
        synthetic=synthetic_arr,
        pre_years=pre_years,
        post_years=post_years,
    )


def mspe(y_true: np.ndarray, y_hat: np.ndarray, mask: np.ndarray) -> float:
    diff = y_true[mask] - y_hat[mask]
    return float(np.nanmean(diff**2))


def run_basic_checks():
    df = load_scm_dataset()
    res = build_equal_weight_synth(df)

    # Masks
    pre_mask = np.isin(res.years, res.pre_years)
    post_mask = np.isin(res.years, res.post_years)

    pre_mspe = mspe(res.treated, res.synthetic, pre_mask)
    post_mspe = mspe(res.treated, res.synthetic, post_mask)
    ate = float(np.nanmean(res.treated[post_mask] - res.synthetic[post_mask]))

    print("\n=== BASIC FIT (EQUAL-WEIGHTS SYNTHETIC) ===")
    print(f"Pre-treatment MSPE : {pre_mspe:.4f}")
    print(f"Post-treatment MSPE: {post_mspe:.4f}")
    print(f"MSPE ratio (Post/Pre): {post_mspe / pre_mspe:.2f}" if pre_mspe > 0 else "MSPE ratio: NA")
    print(f"Average treatment effect (ATE, NC - synth, post): {ate:.4f}")

    # Placebo-like pre-treatment effects (as in the R script)
    placebo_years: List[int] = [2014, 2015, 2016, 2017]
    print("\n=== PLACEBO 'EFFECTS' IN PRE-TREATMENT PERIOD ===")
    for py in placebo_years:
        mask = (res.years >= py) & pre_mask
        if mask.sum() == 0:
            continue
        ate_py = float(np.nanmean(res.treated[mask] - res.synthetic[mask]))
        print(f"  {py} ({TREATMENT_YEAR - py} yrs pre): ATE = {ate_py:8.4f}")

    print(f"  {TREATMENT_YEAR} (actual post) : ATE = {ate:8.4f}")

    # Leave-one-out style sensitivity for equal-weights synthetic
    print("\n=== LEAVE-ONE-OUT (EQUAL-WEIGHTS) SENSITIVITY ===")
    control_courts = sorted(df.loc[df["Court"] != "NC", "Court"].unique())
    results = []
    post_years_list = sorted(res.post_years)

    for exclude in control_courts:
        ate_loo_vals = []
        for year in post_years_list:
            year_df = df[(df["Year"] == year)]
            nc_rate = year_df.loc[year_df["Court"] == "NC", "DissentRate"].mean()
            ctrl = year_df.loc[
                (year_df["Court"] != "NC") & (year_df["Court"] != exclude),
                "DissentRate",
            ].dropna()
            if len(ctrl) == 0 or np.isnan(nc_rate):
                continue
            synth = ctrl.mean()
            ate_loo_vals.append(nc_rate - synth)

        if ate_loo_vals:
            ate_loo = float(np.nanmean(ate_loo_vals))
            results.append((exclude, ate_loo))

    if results:
        results.sort(key=lambda x: x[1])
        print("ATE when dropping each control court:\n")
        for court, val in results:
            print(f"  Exclude {court:<3}: ATE = {val:8.4f}")
        vals = np.array([v for _, v in results])
        print("\nRange:  ", f"{vals.min():.4f} to {vals.max():.4f}")
        print("Mean:   ", f"{vals.mean():.4f}")
        print("SD:     ", f"{vals.std(ddof=1):.4f}")
    else:
        print("No valid leave-one-out results (insufficient data).")


def main() -> None:
    run_basic_checks()


if __name__ == "__main__":
    main()


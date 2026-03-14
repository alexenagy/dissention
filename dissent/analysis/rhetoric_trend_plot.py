'''
rhetoric_trend_plot.py

Analysis 1: Time-series plot of mean raw rhetoric scores by selection mechanism.

Plots the annual mean rhetoric score for each mechanism type over time.
No detrending is applied — this shows the raw trajectories.

Negative scores = more discrepant language
Positive scores = more concordant language
'''

import pandas as pd
import plotly.graph_objects as go
from dissent.config import PROCESSED_DATA_DIR, INTERIM_DATA_DIR, FIGURES_DIR


MECHANISM_LABELS = {
    "P": "Partisan Elections",
    "N": "Nonpartisan Elections",
    "A": "Appointment",
    "R": "Retention",
}

MECHANISM_COLORS = {
    "P": "rgb(239, 85, 59)",
    "N": "rgb(99, 110, 250)",
    "A": "rgb(0, 204, 150)",
    "R": "rgb(171, 99, 250)",
}


def court_to_state_abbrev(court_jurisdiction):
    if pd.isna(court_jurisdiction):
        return None
    s = str(court_jurisdiction).strip()
    return s.split(", ")[-1].strip() if ", " in s else None


def main():
    print("Loading data...")
    rhetoric = pd.read_parquet(PROCESSED_DATA_DIR / "rhetoric_scores.parquet")
    rhetoric = rhetoric.dropna(subset=["rhetoric_score", "year", "court_jurisdiction"]).copy()
    rhetoric["court"] = rhetoric["court_jurisdiction"].apply(court_to_state_abbrev)
    rhetoric = rhetoric.dropna(subset=["court"])
    rhetoric["year"] = rhetoric["year"].astype(int)
    rhetoric = rhetoric[rhetoric["year"] <= 2019]

    # Annual mean raw rhetoric score per state (no detrending)
    annual = (
        rhetoric.groupby(["court", "year"])["rhetoric_score"]
        .mean()
        .reset_index()
        .rename(columns={"rhetoric_score": "mean_score"})
    )

    # Merge with selection mechanism — inner join keeps only state-years
    # where we have both rhetoric data and a known mechanism
    selection = pd.read_csv(INTERIM_DATA_DIR / "selection_mechanisms.csv")
    df = annual.merge(selection, on=["year", "court"], how="inner")

    fig = go.Figure()
    for mech in ["P", "N", "A", "R"]:
        subset = df[df["selection_mechanism"] == mech]
        annual_mech = subset.groupby("year")["mean_score"].mean().reset_index()
        fig.add_trace(go.Scatter(
            x=annual_mech["year"],
            y=annual_mech["mean_score"],
            mode="lines",
            name=MECHANISM_LABELS[mech],
            line=dict(color=MECHANISM_COLORS[mech], width=2),
        ))

    fig.update_layout(
        title="Mean Rhetoric Score by Selection Mechanism Over Time<br>"
              "<sup>Negative = more discrepant; positive = more neutral</sup>",
        xaxis_title="Year",
        yaxis_title="Mean rhetoric score",
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Arial", size=12),
        legend=dict(orientation="h", y=-0.15, x=0.5, xanchor="center"),
        width=900, height=500,
    )
    fig.update_xaxes(showgrid=False, showline=True, linewidth=0.5, linecolor="black")
    fig.update_yaxes(showgrid=True, gridcolor="rgba(0,0,0,0.08)",
                     showline=True, linewidth=0.5, linecolor="black")

    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    fig.write_image(FIGURES_DIR / "rhetoric_by_mechanism.png", scale=3)
    fig.write_html(FIGURES_DIR / "rhetoric_by_mechanism.html")
    print("Saved: rhetoric_by_mechanism.png")


if __name__ == "__main__":
    main()
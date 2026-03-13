'''
rhetoric_event_study.py

Analysis 3: Event study plots for states that switched judicial selection mechanisms.

For each switching state, compares the mean rhetoric score in the
6 years before vs. 6 years after the switch year. Results are grouped by
transition pair (from mechanism -> to mechanism) so that comparisons are
internally coherent — the direction of change only makes sense relative
to where the state started.

Output: one PNG per transition-pair group, with panels in rows of three.

Negative scores = more ideological language
Positive scores = more neutral language
'''

import math
import pandas as pd
import statsmodels.formula.api as smf
from scipy import stats
from scipy.stats import binomtest
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dissent.config import PROCESSED_DATA_DIR, INTERIM_DATA_DIR, FIGURES_DIR


# =============================================================================
# SWITCHERS
# States that changed their judicial selection mechanism.
# P = Partisan, N = Nonpartisan, A = Appointment, R = Retention
# =============================================================================
SWITCHERS = [
    ("FL", "P", "R", 1971),
    ("AZ", "N", "R", 1974),
    ("VT", "A", "R", 1974),
    ("SD", "N", "R", 1973),
    ("WY", "N", "R", 1973),
    ("KY", "P", "N", 1976),
    ("NM", "P", "R", 1989),
    ("MS", "P", "N", 1994),
    ("UT", "N", "R", 1985),
    ("NC", "P", "N", 2002),
    ("NC", "N", "P", 2018),
    ("WV", "P", "N", 2016),
]

# =============================================================================
# GROUPS
# One output PNG per transition pair, panels in rows of 3.
# =============================================================================
GROUPS = [
    {
        "filename": "event_study_retention.png",
        "title": "All Transitions → Retention",
        "row_height": 220,
        "vertical_spacing": 0.08,
        "switchers": [
            ("FL", "P", "R", 1971),
            ("AZ", "N", "R", 1974),
            ("VT", "A", "R", 1974),
            ("SD", "N", "R", 1973),
            ("WY", "N", "R", 1973),
            ("NM", "P", "R", 1989),
            ("UT", "N", "R", 1985),
        ],
    },
    {
        "filename": "event_study_nonpartisan.png",
        "title": "Partisan → Nonpartisan",
        "row_height": 300,
        "vertical_spacing": 0.15,
        "switchers": [
            ("KY", "P", "N", 1976),
            ("MS", "P", "N", 1994),
            ("NC", "P", "N", 2002),
            ("WV", "P", "N", 2016),
        ],
    },
    {
        "filename": "event_study_nc.png",
        "title": "North Carolina",
        "row_height": 350,
        "vertical_spacing": 0.15,
        "switchers": [
            ("NC", "P", "N", 2002),
            ("NC", "N", "P", 2018),
        ],
    },
]

MECHANISM_LABELS = {
    "P": "Partisan",
    "N": "Nonpartisan",
    "A": "Appointment",
    "R": "Retention",
}

# ±6 years around the switch year
WINDOW = 6

COLOR_PRE = "rgb(100, 181, 246)"
COLOR_POST = "rgb(186, 104, 200)"


def court_to_state_abbrev(court_jurisdiction):
    if pd.isna(court_jurisdiction):
        return None
    s = str(court_jurisdiction).strip()
    return s.split(", ")[-1].strip() if ", " in s else None


def compute_result(state, from_mech, to_mech, switch_year, annual):
    '''
    Computes pre/post mean rhetoric and t-test for one switching state.
    Pre period: [switch_year - WINDOW, switch_year - 1]
    Post period: [switch_year, switch_year + WINDOW]
    Returns None if fewer than 2 observations in either period.
    '''
    court_data = annual[annual["court"] == state].copy()

    pre = court_data[
        (court_data["year"] >= switch_year - WINDOW) &
        (court_data["year"] < switch_year)
    ]["mean"]

    post = court_data[
        (court_data["year"] >= switch_year) &
        (court_data["year"] <= switch_year + WINDOW)
    ]["mean"]

    if len(pre) < 2 or len(post) < 2:
        print(f"  Skipping {state} {switch_year}: insufficient data "
              f"(pre={len(pre)}, post={len(post)})")
        return None

    diff = post.mean() - pre.mean()
    t_stat, p_val = stats.ttest_ind(post, pre)
    sig = "***" if p_val < 0.001 else "**" if p_val < 0.01 else "*" if p_val < 0.05 else "†" if p_val < 0.1 else ""

    return {
        "State": state,
        "Switch": f"{MECHANISM_LABELS[from_mech]}→{MECHANISM_LABELS[to_mech]}",
        "Year": switch_year,
        "Pre mean": round(pre.mean(), 4),
        "Post mean": round(post.mean(), 4),
        "Diff (post-pre)": round(diff, 4),
        "t-stat": round(t_stat, 3),
        "p-value": round(p_val, 4),
        "Sig": sig,
        "_from": from_mech,
        "_to": to_mech,
    }


def make_subplot_panel(fig, row, col, state, switch_year, annual, result, legend_added):
    '''
    Draws one event-study panel into a subplot cell.
    Blue solid line = pre-switch years
    Purple dashed line = post-switch years
    Dotted horizontals = period means
    Vertical dashed line = switch year
    '''
    window_data = annual[
        (annual["court"] == state) &
        (annual["year"] >= switch_year - WINDOW) &
        (annual["year"] <= switch_year + WINDOW)
    ].sort_values("year")

    pre_data = window_data[window_data["year"] < switch_year]
    post_data = window_data[window_data["year"] >= switch_year]

    # Extend pre line one point into post for visual continuity
    pre_connected = pd.concat([pre_data, post_data.iloc[[0]]]) if not post_data.empty else pre_data

    show_pre_legend = not legend_added["pre"]
    show_post_legend = not legend_added["post"]

    fig.add_trace(go.Scatter(
        x=pre_connected["year"], y=pre_connected["mean"],
        mode="lines+markers",
        line=dict(color=COLOR_PRE, width=2),
        marker=dict(size=5),
        name="Pre-switch",
        showlegend=show_pre_legend,
        legendgroup="pre",
    ), row=row, col=col)
    legend_added["pre"] = True

    fig.add_trace(go.Scatter(
        x=post_data["year"], y=post_data["mean"],
        mode="lines+markers",
        line=dict(color=COLOR_POST, width=2, dash="dash"),
        marker=dict(size=5),
        name="Post-switch",
        showlegend=show_post_legend,
        legendgroup="post",
    ), row=row, col=col)
    legend_added["post"] = True

    if len(pre_data) > 0:
        fig.add_shape(
            type="line",
            x0=switch_year - WINDOW, x1=switch_year,
            y0=result["Pre mean"], y1=result["Pre mean"],
            line=dict(color=COLOR_PRE, width=1.5, dash="dot"),
            row=row, col=col,
        )

    if len(post_data) > 0:
        fig.add_shape(
            type="line",
            x0=switch_year, x1=switch_year + WINDOW,
            y0=result["Post mean"], y1=result["Post mean"],
            line=dict(color=COLOR_POST, width=1.5, dash="dot"),
            row=row, col=col,
        )

    fig.add_vline(x=switch_year, line=dict(color="black", width=1, dash="dot"),
                  row=row, col=col)

    fig.update_xaxes(
        range=[switch_year - WINDOW - 0.5, switch_year + WINDOW + 0.5],
        tickvals=[switch_year - WINDOW, switch_year, switch_year + WINDOW],
        ticktext=[str(switch_year - WINDOW), str(switch_year), str(switch_year + WINDOW)],
        tickfont=dict(size=8), row=row, col=col,
    )
    fig.update_yaxes(tickfont=dict(size=8), row=row, col=col)


def save_group_figure(group, all_results, annual):
    switchers = [s for s in group["switchers"] if (s[0], s[3]) in all_results]
    if not switchers:
        print(f"  Skipping {group['filename']} — no data available")
        return

    n = len(switchers)
    ncols = min(2, n)
    nrows = math.ceil(n / ncols)
    row_height = group.get("row_height", 300)
    vertical_spacing = group.get("vertical_spacing", 0.15)

    subplot_titles = [
        f"{s} ({MECHANISM_LABELS[f]}→{MECHANISM_LABELS[t]}, {y}) {all_results[(s, y)]['Sig']}"
        for s, f, t, y in switchers
    ]

    fig = make_subplots(
        rows=nrows, cols=ncols,
        subplot_titles=subplot_titles,
        vertical_spacing=vertical_spacing,
        horizontal_spacing=0.08,
    )

    legend_added = {"pre": False, "post": False}
    for i, (state, from_mech, to_mech, switch_year) in enumerate(switchers):
        row = i // ncols + 1
        col = i % ncols + 1
        make_subplot_panel(fig, row, col, state, switch_year, annual,
                           all_results[(state, switch_year)], legend_added)

    fig.update_layout(
        title=(
            group["title"] +
            "<br><sup>Dotted horizontal = period mean; negative = more ideological</sup>"
        ),
        height=row_height * nrows,
        width=800,
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Arial", size=10),
        legend=dict(orientation="h", y=-0.04, x=0.5, xanchor="center"),
    )
    fig.update_xaxes(showline=True, linewidth=0.5, linecolor="black",
                     mirror=False, showgrid=False, ticks="outside")
    fig.update_yaxes(showline=True, linewidth=0.5, linecolor="black",
                     mirror=False, showgrid=False, ticks="outside",
                     title_text="Rhetoric score")

    out_path = FIGURES_DIR / group["filename"]
    fig.write_image(out_path, scale=3)
    fig.write_html(str(out_path).replace(".png", ".html"))
    print(f"  Saved: {group['filename']}")


def main():
    print("Loading data...")
    rhetoric = pd.read_parquet(PROCESSED_DATA_DIR / "rhetoric_scores.parquet")
    rhetoric = rhetoric.dropna(subset=["rhetoric_score", "year", "court_jurisdiction"]).copy()
    rhetoric["court"] = rhetoric["court_jurisdiction"].apply(court_to_state_abbrev)
    rhetoric = rhetoric.dropna(subset=["court"])
    rhetoric["year"] = rhetoric["year"].astype(int)
    rhetoric = rhetoric[rhetoric["year"] <= 2019]

    annual = (
        rhetoric.groupby(["court", "year"])["rhetoric_score"]
        .mean()
        .reset_index()
        .rename(columns={"rhetoric_score": "mean"})
    )

    # Print results table
    print(f"=== Event Study: Pre/Post Rhetoric Scores (±{WINDOW} years) ===")
    print(f"{'State':<6} {'Switch':<48} {'Year':>6} {'Pre':>8} {'Post':>8} "
          f"{'Diff':>8} {'t':>8} {'p':>8}")
    print("-" * 90)

    all_results = {}
    for state, from_mech, to_mech, switch_year in SWITCHERS:
        key = (state, switch_year)
        r = compute_result(state, from_mech, to_mech, switch_year, annual)
        if r is not None:
            all_results[key] = r
            print(f"{r['State']:<6} {r['Switch']:<48} {r['Year']:>6} "
                  f"{r['Pre mean']:>8.4f} {r['Post mean']:>8.4f} "
                  f"{r['Diff (post-pre)']:>8.4f} {r['t-stat']:>8.3f} "
                  f"{r['p-value']:>8.4f} {r['Sig']:<6}")

    # Sign test summary by destination mechanism
    print("\n--- Summary by destination mechanism ---")
    df_full = pd.DataFrame(list(all_results.values()))
    for to_mech, label in [("R", "→ Retention"), ("N", "→ Nonpartisan"), ("P", "→ Partisan")]:
        subset = df_full[df_full["_to"] == to_mech]
        if subset.empty:
            continue
        neg = (subset["Diff (post-pre)"] < 0).sum()
        pos = (subset["Diff (post-pre)"] > 0).sum()
        mean_diff = subset["Diff (post-pre)"].mean()
        n = len(subset)
        sign_p = binomtest(max(neg, pos), n, 0.5).pvalue
        print(f"  {label}: n={n}, mean diff={mean_diff:.4f}, "
              f"negative={neg}/{n}, positive={pos}/{n}, sign test p={sign_p:.4f}")

    # Save figures
    print("\n--- Saving figures ---")
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    for group in GROUPS:
        save_group_figure(group, all_results, annual)


if __name__ == "__main__":
    main()
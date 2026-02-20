# Standard library
from pathlib import Path

# Third-party libraries
import numpy as np
import pandas as pd
import typer
from loguru import logger
from tqdm import tqdm
from gensim.models import Word2Vec
from sklearn.decomposition import PCA
import plotly.graph_objects as go
import plotly.express as px

# Local application imports
from dissent.config import FIGURES_DIR, PROCESSED_DATA_DIR, MODELS_DIR, INTERIM_DATA_DIR

app = typer.Typer()

def semantic_corner():
    """Create semantic corner plot with global inset map."""
    model_path = MODELS_DIR / "word2vec_checkpoint_00031.model"
    model = Word2Vec.load(str(model_path))

    # ----- GLOBAL PCA -----
    all_words = model.wv.index_to_key
    all_vectors = np.array([model.wv[word] for word in all_words])

    pca = PCA(n_components=2, random_state=42)
    all_proj = pca.fit_transform(all_vectors)

    df_global = pd.DataFrame({
        "x": all_proj[:, 0],
        "y": all_proj[:, 1],
        "word": all_words
    })

    # ----- SEMANTIC CORNER -----
    anchors = ["political", "judge", "court"]
    top_n = 30

    words_to_plot = set(anchors)
    for anchor in anchors:
        for word, _ in model.wv.most_similar(anchor, topn=top_n):
            words_to_plot.add(word)

    words_to_plot = list(words_to_plot)
    corner_vectors = np.array([model.wv[word] for word in words_to_plot])
    corner_proj = pca.transform(corner_vectors)

    df_corner = pd.DataFrame({
        "x": corner_proj[:, 0],
        "y": corner_proj[:, 1],
        "word": words_to_plot
    })

    # Bounding box for corner in global space
    x_min, x_max = df_corner["x"].min(), df_corner["x"].max()
    y_min, y_max = df_corner["y"].min(), df_corner["y"].max()

    # ----- FIGURE -----
    fig = go.Figure()

    # MAIN VIEW: Semantic corner (zoomed)
    fig.add_trace(go.Scatter(
        x=df_corner["x"],
        y=df_corner["y"],
        mode="markers+text",
        text=df_corner["word"],
        textposition="top center",
        marker=dict(size=9),
        name="Semantic Corner"
    ))

    # INSET: Global space (mini-map)
    fig.add_trace(go.Scatter(
        x=df_global["x"],
        y=df_global["y"],
        mode="markers",
        marker=dict(size=2, opacity=0.3),
        name="Global Space",
        xaxis="x2",
        yaxis="y2",
        hoverinfo="skip"
    ))

    # Bounding box on inset
    fig.add_shape(
        type="rect",
        x0=x_min,
        x1=x_max,
        y0=y_min,
        y1=y_max,
        xref="x2",
        yref="y2",
        line=dict(width=2),
    )

    # Layout: define inset axes
    fig.update_layout(
        title="Semantic Corner with Global Inset Map (PCA)",
        width=900,
        height=900,

        xaxis=dict(domain=[0, 1], title="PCA 1"),
        yaxis=dict(domain=[0, 1], title="PCA 2"),

        xaxis2=dict(domain=[0.70, 0.98], anchor="y2", showgrid=False, title=""),
        yaxis2=dict(domain=[0.70, 0.98], anchor="x2", showgrid=False, title=""),

        showlegend=False
    )
    fig.write_html("semantic_corner_plot.html")
    fig.write_image("semantic_corner_plot.png", scale = 4)
    fig.show()

@app.command()
def main(): 
    """Graph rhetoric scores over time by court, split by judicial selection method."""
    SELECTION_CSV = INTERIM_DATA_DIR / "selection_mechanisms.csv"
    
    SELECTION_LABELS = {
        "P": "Partisan Elections",
        "N": "Nonpartisan Elections",
        "A": "Appointment",
    }
    
    def load_selection_methods() -> pd.DataFrame:
        return pd.read_csv(SELECTION_CSV)
    
    def court_to_state_abbrev(court_jurisdiction: str) -> str | None:
        """Extract state abbreviation from court_jurisdiction (e.g. 'North Carolina, NC' -> 'NC')."""
        if pd.isna(court_jurisdiction):
            return None
        s = str(court_jurisdiction).strip()
        if ", " in s:
            return s.split(", ")[-1].strip()
        return None
    
    # Load rhetoric scores
    rhetoric_path = PROCESSED_DATA_DIR / "processed_rhetoric_score.parquet"
    rhetoric = pd.read_parquet(rhetoric_path)
    
    # Clean and add court (state abbreviation)
    rhetoric = rhetoric.dropna(subset=["rhetoric_score", "year", "court_jurisdiction"]).copy()
    rhetoric["court"] = rhetoric["court_jurisdiction"].apply(court_to_state_abbrev)
    rhetoric = rhetoric.dropna(subset=["court"])
    rhetoric["year"] = rhetoric["year"].astype(int)
    
    # Load selection method per (year, court)
    selection = load_selection_methods()
    rhetoric = rhetoric.merge(
        selection,
        on=["year", "court"],
        how="inner",
    )
    rhetoric = rhetoric[["year", "rhetoric_score", "selection_mechanism"]]
    
    # By (year, selection_mechanism): mean and 25th/75th percentiles of rhetoric scores
    stats = (
        rhetoric.groupby(["year", "selection_mechanism"])["rhetoric_score"]
        .agg(
            [
                ("mean", "mean"),
                ("p25", lambda x: x.quantile(0.25)),
                ("p75", lambda x: x.quantile(0.75)),
            ]
        )
        .reset_index()
    )
    
    fig = go.Figure()
    colors = {"P": "rgba(31, 119, 180, 0.3)", "N": "rgba(44, 160, 44, 0.3)", "A": "rgba(255, 127, 0, 0.3)"}
    line_colors = {"P": "#1f77b4", "N": "#2ca02c", "A": "#ff7f0e"}
    
    for code in SELECTION_LABELS:
        df = stats[stats["selection_mechanism"] == code].sort_values("year")
        if df.empty:
            continue
        label = SELECTION_LABELS[code]
        c = line_colors.get(code, "#888")
        fill_c = colors.get(code, "rgba(128,128,128,0.2)")
        # Shaded band (25th–75th percentile)
        fig.add_trace(
            go.Scatter(
                x=df["year"].tolist() + df["year"].tolist()[::-1],
                y=df["p75"].tolist() + df["p25"].tolist()[::-1],
                fill="toself",
                fillcolor=fill_c,
                line=dict(width=0),
                name=f"{label} (25th–75th %ile)",
                legendgroup=label,
                showlegend=True,
            )
        )
        # Mean line
        fig.add_trace(
            go.Scatter(
                x=df["year"],
                y=df["mean"],
                name=f"{label} (mean)",
                line=dict(color=c, width=2),
                legendgroup=label,
            )
        )
    
    fig.update_layout(
        title="Rhetoric Scores Over Time by Selection Mechanism (Mean and 25th/75th Percentiles)",
        xaxis_title="Year",
        yaxis_title="Rhetoric Score",
        hovermode="x unified",
        width=650,
        height=400,
        font=dict(size=10),
    )
    
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    png_path = FIGURES_DIR / "rhetoric_scores_over_time_by_selection_mechanism.png"
    html_path = FIGURES_DIR / "rhetoric_scores_over_time_by_selection_mechanism.html"
    fig.write_image(png_path, scale=6, engine="kaleido")
    fig.write_html(html_path)
    print(f"Saved PNG: {png_path}")
    print(f"Saved HTML: {html_path}")
    fig.show()

if __name__ == "__main__":
    main()

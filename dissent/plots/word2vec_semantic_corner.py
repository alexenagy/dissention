import numpy as np
import pandas as pd
from gensim.models import Word2Vec
from sklearn.decomposition import PCA
import plotly.graph_objects as go
import typer
from dissent.config import FIGURES_DIR, MODELS_DIR

app = typer.Typer()

C_CORNER = "#1e88e5"   # blue  — neighbor points
C_TEXT   = "#8e24aa"   # purple — word labels
C_GLOBAL = "#9c27b0"   # purple — inset dots
C_BOX    = "#1e88e5"   # blue  — bounding box

@app.command()
def main():
    """Create semantic corner plot with global inset map."""
    model_path = MODELS_DIR / "iteration_0009/word2vec_checkpoint_00031.model"
    model = Word2Vec.load(str(model_path))

    # ----- GLOBAL PCA -----
    all_words = model.wv.index_to_key
    all_vectors = np.array([model.wv[word] for word in all_words])

    pca = PCA(n_components=2, random_state=42)
    all_proj = pca.fit_transform(all_vectors)

    df_global = pd.DataFrame({
        "x": all_proj[:, 0],
        "y": all_proj[:, 1],
        "word": all_words,
    })

    # ----- SEMANTIC CORNER -----
    anchors = ["respectfully"]
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
        "word": words_to_plot,
    })

    x_min, x_max = df_corner["x"].min(), df_corner["x"].max()
    y_min, y_max = df_corner["y"].min(), df_corner["y"].max()

    df_anchor    = df_corner[df_corner["word"].isin(anchors)]
    df_neighbors = df_corner[~df_corner["word"].isin(anchors)]

    # ----- FIGURE -----
    fig = go.Figure()

    # Neighbor points — blue dots, purple labels
    fig.add_trace(go.Scatter(
        x=df_neighbors["x"],
        y=df_neighbors["y"],
        mode="markers+text",
        text=df_neighbors["word"],
        textposition="top center",
        marker=dict(size=9, color=C_CORNER),
        textfont=dict(color=C_TEXT, size=11),
        name="Neighbors",
    ))

    # Anchor — larger dark blue diamond, dark purple label
    fig.add_trace(go.Scatter(
        x=df_anchor["x"],
        y=df_anchor["y"],
        mode="markers+text",
        text=df_anchor["word"],
        textposition="top center",
        marker=dict(size=14, color="#0d47a1", symbol="diamond"),
        textfont=dict(color="#4a148c", size=13, family="Arial Black"),
        name="Anchor",
    ))

    # Inset: global space — purple dots
    fig.add_trace(go.Scatter(
        x=df_global["x"],
        y=df_global["y"],
        mode="markers",
        marker=dict(size=2, color=C_GLOBAL, opacity=0.25),
        name="Global Space",
        xaxis="x2",
        yaxis="y2",
        hoverinfo="skip",
    ))

    # Bounding box on inset — blue
    fig.add_shape(
        type="rect",
        x0=x_min, x1=x_max,
        y0=y_min, y1=y_max,
        xref="x2", yref="y2",
        line=dict(color=C_BOX, width=2),
    )

    fig.update_layout(
        title="Semantic Corner with Global Inset Map (PCA)",
        width=900, height=900,
        xaxis=dict(domain=[0, 1], title="PCA 1"),
        yaxis=dict(domain=[0, 1], title="PCA 2"),
        xaxis2=dict(domain=[0.70, 0.98], anchor="y2", showgrid=False, title=""),
        yaxis2=dict(domain=[0.70, 0.98], anchor="x2", showgrid=False, title=""),
        showlegend=False,
    )

    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    fig.write_html(str(FIGURES_DIR / "semantic_corner_plot.html"))
    fig.write_image(str(FIGURES_DIR / "semantic_corner_plot.png"), scale=4)
    print(f"Saved to {FIGURES_DIR}")

if __name__ == "__main__":
    app()
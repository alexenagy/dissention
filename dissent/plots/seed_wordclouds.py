"""
Word clouds for ideological and nonideological seed words.
Font size scales with the absolute discriminative score.
"""
import random
import pandas as pd
from wordcloud import WordCloud
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from dissent.config import INTERIM_DATA_DIR, FIGURES_DIR

ideo_words  = (INTERIM_DATA_DIR / "ideological_seed_words.txt").read_text().split()
nideo_words = (INTERIM_DATA_DIR / "nonideological_seed_words.txt").read_text().split()

df = pd.read_csv(INTERIM_DATA_DIR / "wordscores_vocabulary.csv")

def get_freqs(words, score_col):
    merged = (pd.DataFrame({"word": words})
              .merge(df[["word", score_col]], on="word", how="left"))
    merged[score_col] = merged[score_col].fillna(merged[score_col].median()).abs()
    return dict(zip(merged["word"], merged[score_col]))

ideo_freq  = get_freqs(ideo_words,  "ideological_diff")
nideo_freq = get_freqs(nideo_words, "nonideological_diff")

def make_color_func(colors):
    def color_func(word, font_size, position, orientation, random_state=None, **kwargs):
        return random.choice(colors)
    return color_func

# Light blues (ideological), light purples (nonideological) — darker shades
IDEO_COLORS  = ["#1565c0", "#1976d2", "#1e88e5", "#2196f3", "#42a5f5", "#64b5f6"]
NIDEO_COLORS = ["#6a1b9a", "#7b1fa2", "#8e24aa", "#9c27b0", "#ab47bc", "#ba68c8"]

COMMON = dict(
    width=800, height=500,
    background_color="white",
    prefer_horizontal=0.85,
    min_font_size=10,
    max_font_size=120,
    relative_scaling=0.6,
    collocations=False,
)

wc_ideo  = WordCloud(color_func=make_color_func(IDEO_COLORS),  **COMMON).generate_from_frequencies(ideo_freq)
wc_nideo = WordCloud(color_func=make_color_func(NIDEO_COLORS), **COMMON).generate_from_frequencies(nideo_freq)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 5))
fig.patch.set_facecolor("#fafafa")

ax1.imshow(wc_ideo,  interpolation="bilinear")
ax1.axis("off")
ax1.set_title("Ideological Dictionary",
              fontsize=13, fontweight="bold", color="#000000", pad=10)

ax2.imshow(wc_nideo, interpolation="bilinear")
ax2.axis("off")
ax2.set_title("Conventional Dictionary",
              fontsize=13, fontweight="bold", color="#000000", pad=10)

plt.tight_layout(rect=[0, 0.04, 1, 1])

OUT_PATH = FIGURES_DIR / "seed_wordclouds.png"
OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
plt.savefig(OUT_PATH, dpi=300, bbox_inches="tight", facecolor="#fafafa")
plt.close()
print(f"Saved: {OUT_PATH}")
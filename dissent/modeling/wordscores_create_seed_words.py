from pathlib import Path
import numpy as np
import pandas as pd
from loguru import logger
from sklearn.feature_extraction.text import TfidfVectorizer
from dissent.config import MODELS_DIR, PROCESSED_DATA_DIR, RAW_DATA_DIR


def compute_wordscores(df, text_col="opinion_text", score_col="candidate.cfscore", top_n=500):
    """
    Implement Wordscores (Laver, Benoit & Garry 2003) using CF-scores as reference anchors.

    Reference texts: justices at ideological extremes (top and bottom 10th percentile
    of CF-scores, i.e. most liberal and most conservative)
    Virgin texts: justices closer to 0 (moderate, less ideological)

    This allows us to identify:
    1. Words associated with ideological rhetoric (from extreme justices)
    2. Words associated with moderate/less ideological rhetoric (from centrist justices)
    """
    # Step 1: Define reference texts (ideological extremes) and virgin texts (moderates)
    upper = df[score_col].quantile(0.90)   # most conservative
    lower = df[score_col].quantile(0.10)   # most liberal

    # Reference: ideologically extreme justices (both liberal and conservative)
    ref_df = df[(df[score_col] >= upper) | (df[score_col] <= lower)].copy()

    # Virgin: moderate justices (closer to 0)
    virgin_df = df[(df[score_col] > lower) & (df[score_col] < upper)].copy()

    logger.info(f"Reference texts (ideological extremes): {len(ref_df)}")
    logger.info(f"Virgin texts (moderates): {len(virgin_df)}")
    logger.info(f"Reference CF-score range: [{ref_df[score_col].min():.3f}, {ref_df[score_col].max():.3f}]")
    logger.info(f"Virgin CF-score range: [{virgin_df[score_col].min():.3f}, {virgin_df[score_col].max():.3f}]")

    # Step 2: Compute word frequencies for reference texts
    vectorizer = TfidfVectorizer(
        max_features=top_n,
        min_df=10,
        stop_words="english",
        token_pattern=r"(?u)\b[a-zA-Z]{3,}\b",
    )

    ref_matrix = vectorizer.fit_transform(ref_df[text_col])
    vocab = vectorizer.get_feature_names_out()

    # Step 3: Compute wordscore for each word
    # Use absolute CF-score so both liberal (-1) and conservative (1) extremes
    # are treated as equally ideological reference points
    ref_scores_raw = ref_df[score_col].values
    ref_scores_abs = np.abs(ref_scores_raw)  # distance from 0 = ideological intensity
    ref_dense = ref_matrix.toarray()

    word_freq_total = ref_dense.sum(axis=0)
    word_score_weighted = (ref_dense * ref_scores_abs[:, np.newaxis]).sum(axis=0)

    wordscores = np.where(
        word_freq_total > 0,
        word_score_weighted / word_freq_total,
        0,
    )

    # Step 4: Build results dataframe
    # Higher wordscore = more associated with ideological extremes
    # Lower wordscore = more associated with moderate justices
    results = pd.DataFrame(
        {
            "word": vocab,
            "wordscore": wordscores,
            "total_freq": word_freq_total,
        }
    ).sort_values("wordscore", ascending=False)

    # Step 5: Score virgin texts (moderates)
    virgin_matrix = vectorizer.transform(virgin_df[text_col])
    virgin_dense = virgin_matrix.toarray()

    virgin_scores = np.where(
        virgin_dense.sum(axis=1).clip(min=1) > 0,
        (virgin_dense * wordscores[np.newaxis, :]).sum(axis=1)
        / virgin_dense.sum(axis=1).clip(min=1),
        0,
    )

    virgin_df = virgin_df.copy()
    virgin_df["wordscore_estimate"] = virgin_scores

    return results, virgin_df


def extract_text(opinions):
    """Extract and concatenate opinion text from nested opinions column."""
    if opinions is None:
        return None
    texts = []
    for o in opinions:
        t = o.get("opinion_text")
        if t:
            texts.append(t)
    return " ".join(texts) if texts else None


def main():
    # Load opinions with CF-scores already merged in by dataset.py
    df = pd.read_parquet(PROCESSED_DATA_DIR / "dataset.parquet")
    logger.info(f"Loaded {len(df)} rows")

    # Drop rows without CF-score
    df = df.dropna(subset=["candidate.cfscore"])
    logger.info(f"Rows with CF-scores: {len(df)}")

    # Extract opinion text from nested opinions column
    df["opinion_text"] = df["opinions"].apply(extract_text)
    df = df.dropna(subset=["opinion_text"])
    logger.info(f"Rows with opinion text: {len(df)}")

    # Run wordscores
    word_results, virgin_results = compute_wordscores(df)

    # Words most associated with ideological extremes (political rhetoric)
    print("\nWords most associated with IDEOLOGICAL EXTREMES (political rhetoric seed candidates):")
    print(word_results.head(50).to_string())

    # Words most associated with moderate justices (evidence-based rhetoric)
    print("\nWords most associated with MODERATE justices (evidence-based seed candidates):")
    print(word_results.tail(50).to_string())

    # Save results
    word_results.to_csv(MODELS_DIR / "wordscores_vocabulary.csv", index=False)
    virgin_results[["id", "last_name", "state", "candidate.cfscore", "wordscore_estimate"]].to_csv(
        MODELS_DIR / "wordscores_virgin_texts.csv", index=False
    )
    logger.success(f"Saved word scores to {MODELS_DIR / 'wordscores_vocabulary.csv'}")


if __name__ == "__main__":
    main()
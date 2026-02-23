# Standard library
from pathlib import Path

# Third-party libraries
import numpy as np
import pandas as pd
from loguru import logger
from sklearn.feature_extraction.text import TfidfVectorizer

# Local application imports
from dissent.config import MODELS_DIR, PROCESSED_DATA_DIR, INTERIM_DATA_DIR


def compute_wordscores(df, text_col="opinion_text", score_col="candidate.cfscore", top_n=500):
    """
    Implement Wordscores (Laver, Benoit & Garry 2003) using CF-scores as reference anchors.

    Reference text 1: most ideologically extreme 25% of cases by mean absolute CF-score
    Reference text 2: least ideologically extreme 25% of cases by mean absolute CF-score

    Wordscores are computed separately for each reference group. Words are ranked by
    the difference between their ideological score and their nonideological score:
    - High difference = associated with ideological justices -> ideological seed candidates
    - Low difference (or negative) = associated with nonideological justices -> nonideological seed candidates
    """
    df = df.copy()
    df["cf_score_abs"] = df[score_col].abs()

    # Reference text 1: most ideologically extreme 25%
    ideological_cutoff = df["cf_score_abs"].quantile(0.75)
    ideological_df = df[df["cf_score_abs"] >= ideological_cutoff].copy()

    # Reference text 2: least ideologically extreme 25% (closest to 0)
    nonideological_cutoff = df["cf_score_abs"].quantile(0.25)
    nonideological_df = df[df["cf_score_abs"] <= nonideological_cutoff].copy()

    logger.info(f"Reference text 1 (ideological, |CF| >= {ideological_cutoff:.3f}): {len(ideological_df)}")
    logger.info(f"Reference text 2 (nonideological, |CF| <= {nonideological_cutoff:.3f}): {len(nonideological_df)}")

    # Fit vectorizer on combined reference texts to get shared vocabulary
    vectorizer = TfidfVectorizer(
        max_features=top_n,
        min_df=10,
        stop_words="english",
        token_pattern=r"(?u)\b[a-zA-Z]{3,}\b",
    )
    vectorizer.fit(pd.concat([ideological_df[text_col], nonideological_df[text_col]]))
    vocab = vectorizer.get_feature_names_out()

    def group_wordscores(group_df, abs_scores):
        """Compute wordscores for a reference group weighted by absolute CF-score."""
        matrix = vectorizer.transform(group_df[text_col]).toarray()
        freq_total = matrix.sum(axis=0)
        score_weighted = (matrix * abs_scores[:, np.newaxis]).sum(axis=0)
        return np.where(freq_total > 0, score_weighted / freq_total, 0)

    # Compute wordscores for each reference group
    ideological_scores = group_wordscores(ideological_df, ideological_df["cf_score_abs"].values)
    nonideological_scores = group_wordscores(nonideological_df, nonideological_df["cf_score_abs"].values)

    # Difference score: high = more associated with ideological justices
    diff_scores = ideological_scores - nonideological_scores

    results = pd.DataFrame(
        {
            "word": vocab,
            "ideological_wordscore": ideological_scores,
            "nonideological_wordscore": nonideological_scores,
            "diff_score": diff_scores,
            "total_freq_ideological": vectorizer.transform(ideological_df[text_col]).toarray().sum(axis=0),
            "total_freq_nonideological": vectorizer.transform(nonideological_df[text_col]).toarray().sum(axis=0),
        }
    ).sort_values("diff_score", ascending=False)

    return results, ideological_df, nonideological_df


def main():
    # Load only the columns needed for Wordscores — skips nested opinions column
    df = pd.read_parquet(
        PROCESSED_DATA_DIR / "dataset.parquet",
        columns=["id", "year", "court_jurisdiction", "state", "last_name", "candidate.cfscore", "abs_cfscore", "opinion_text"]
    )
    logger.info(f"Loaded {len(df)} rows")

    # Drop rows without CF-score
    df = df.dropna(subset=["candidate.cfscore"])
    logger.info(f"Rows with CF-scores: {len(df)}")

    # Drop rows without opinion text
    df = df.dropna(subset=["opinion_text"])
    logger.info(f"Rows with opinion text: {len(df)}")

    # Run wordscores
    word_results, ideological_df, nonideological_df = compute_wordscores(df)

    # Words most associated with ideological justices (top of diff_score)
    print("\nWords most associated with IDEOLOGICAL justices (ideological seed candidates):")
    print(word_results.head(50).to_string())

    # Words most associated with nonideological justices (bottom of diff_score)
    print("\nWords most associated with NONIDEOLOGICAL justices (nonideological seed candidates):")
    print(word_results.tail(50).to_string())

    # Save full vocabulary
    word_results.to_csv(INTERIM_DATA_DIR / "wordscores_vocabulary.csv", index=False)

    # Save top 50 ideological seed words
    with open(INTERIM_DATA_DIR / "ideological_seed_words.txt", "w") as f:
        f.write("\n".join(word_results.head(50)["word"].tolist()))

    # Save bottom 50 nonideological seed words
    with open(INTERIM_DATA_DIR / "nonideological_seed_words.txt", "w") as f:
        f.write("\n".join(word_results.tail(50)["word"].tolist()))

    logger.success(f"Saved word scores and seed dictionaries to {INTERIM_DATA_DIR}")


if __name__ == "__main__":
    main()
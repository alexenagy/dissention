import multiprocessing as mp
import numpy as np
import pandas as pd
from loguru import logger
from nltk.corpus import stopwords, words
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from dissent.config import MODELS_DIR, PROCESSED_DATA_DIR, INTERIM_DATA_DIR

nlp = None
stop_words = None
english_words = None


def init_worker():
    """Load spaCy and NLTK resources once per worker process."""
    global nlp, stop_words, english_words
    nlp = spacy.load("en_core_web_lg", disable=["parser", "ner"])
    nlp.max_length = 10000000
    stop_words = set(stopwords.words("english"))
    english_words = set(words.words())


def preprocess_text(text):
    """
    Preprocess opinion text to match Word2Vec training pipeline.

    Steps:
    1. Tokenize and lemmatize with spaCy
    2. Lowercase
    3. Remove non-alphabetic tokens
    4. Remove stopwords
    5. Filter to English words only
    Returns a single string of space-joined lemmas for TF-IDF compatibility.
    """
    doc = nlp(text)
    tokens = [
        token.lemma_.lower()
        for token in doc
        if token.is_alpha
        and token.text.lower() not in stop_words
        and token.lemma_.lower() in english_words
    ]
    return " ".join(tokens)


def preprocess_corpus(texts, n_workers=24):
    """Preprocess a list of opinion texts in parallel."""
    with mp.Pool(processes=n_workers, initializer=init_worker) as pool:
        processed = list(pool.imap(preprocess_text, texts))
    return processed


def compute_wordscores(df, text_col="opinion_text", score_col="pajid", top_n=500, n_workers=24):
    """
    Construct discrepant and concordant seed word dictionaries using
    PAJID scores as reference anchors, following the logic of Wordscores
    (Laver, Benoit & Garry 2003). Opinions are split into discrepantly
    extreme and moderate reference groups based on absolute deviation from
    PAJID center (50).

    For each dictionary:
    - Discrepant words: highest discrepant_diff (discrepant_wordscore - concordant_wordscore)
    - Concordant words: highest concordant_diff (concordant_wordscore - discrepant_wordscore)

    Both dictionaries select words that are maximally distinctive to their
    respective group, not just highly scored in absolute terms.

    Preprocessing matches the Word2Vec training pipeline exactly so that
    seed words are guaranteed to exist in the Word2Vec vocabulary.
    """
    df = df.copy()

    # PAJID is centered at 50 — discrepant intensity is deviation from center
    df["abs_pajid"] = (df[score_col] - 50).abs()

    # Reference text 1: most discrepantly extreme 10% (closest to PAJID score 0 and 100)
    liberal_cutoff = df["abs_pajid"].quantile(0.95)
    liberal_df = df[df["abs_pajid"] >= liberal_cutoff].copy()

    conservative_cutoff = df["abs_pajid"].quantile(0.05)
    conservative_df = df[df["abs_pajid"] <= conservative_cutoff].copy()

    discrepant_df = pd.concat([liberal_df, conservative_df])

    # Reference text 2: least discrepantly extreme 10% (closest to PAJID score 50)

    liberal_cutoff = df["abs_pajid"].quantile(0.55)
    liberal_df = df[df["abs_pajid"] <= liberal_cutoff].copy()

    conservative_cutoff = df["abs_pajid"].quantile(0.45)
    conservative_df = df[df["abs_pajid"] >= conservative_cutoff].copy()

    concordant_df = pd.merge(liberal_df, conservative_df, how = "inner")

    # Preprocess both groups using same pipeline as Word2Vec training
    logger.info("Preprocessing discrepant reference texts...")
    discrepant_df["processed_text"] = preprocess_corpus(
        discrepant_df[text_col].tolist(), n_workers=n_workers
    )

    logger.info("Preprocessing concordant reference texts...")
    concordant_df["processed_text"] = preprocess_corpus(
        concordant_df[text_col].tolist(), n_workers=n_workers
    )

    # Fit vectorizer on combined preprocessed texts
    # No stopword removal or lowercasing here since already handled in preprocessing
    vectorizer = TfidfVectorizer(
        max_features=top_n,
        min_df=10,
        token_pattern=r"(?u)\b[a-zA-Z]{3,}\b",
    )
    vectorizer.fit(pd.concat([
        discrepant_df["processed_text"],
        concordant_df["processed_text"]
    ]))
    vocab = vectorizer.get_feature_names_out()

    def group_wordscores(group_df, abs_scores):
        """Compute wordscores for a reference group weighted by absolute PAJID deviation."""
        matrix = vectorizer.transform(group_df["processed_text"]).toarray()
        freq_total = matrix.sum(axis=0)
        score_weighted = (matrix * abs_scores[:, np.newaxis]).sum(axis=0)
        return np.where(freq_total > 0, score_weighted / freq_total, 0)

    # Compute wordscores for each reference group
    logger.info("Computing wordscores...")
    discrepant_scores = group_wordscores(discrepant_df, discrepant_df["abs_pajid"].values)
    concordant_scores = group_wordscores(concordant_df, concordant_df["abs_pajid"].values)

    results = pd.DataFrame(
        {
            "word": vocab,
            "discrepant_wordscore": discrepant_scores,
            "concordant_wordscore": concordant_scores,
            "discrepant_diff": discrepant_scores - concordant_scores,
            "concordant_diff": concordant_scores - discrepant_scores,
            "total_freq_discrepant": vectorizer.transform(
                discrepant_df["processed_text"]
            ).toarray().sum(axis=0),
            "total_freq_concordant": vectorizer.transform(
                concordant_df["processed_text"]
            ).toarray().sum(axis=0),
        }
    ).sort_values("discrepant_diff", ascending=False)

    return results, discrepant_df, concordant_df


def main():
    # Load only the columns needed — opinion_text is the flat extracted text
    # column used for scoring; the nested opinions column is not needed here
    df = pd.read_parquet(
        PROCESSED_DATA_DIR / "dataset.parquet",
        columns=[
            "id", "year", "court_jurisdiction", "state",
            "last_name", "pajid", "opinion_text"
        ]
    )
    logger.info(f"Loaded {len(df)} rows")

    # Drop rows without PAJID score
    df = df.dropna(subset=["pajid"])
    logger.info(f"Rows with PAJID scores: {len(df)}")

    # Drop rows without opinion text
    df = df.dropna(subset=["opinion_text"])
    logger.info(f"Rows with opinion text: {len(df)}")

    # Run wordscores
    word_results, discrepant_df, concordant_df = compute_wordscores(df)

    # Words most distinctive to discrepant justices
    print("\nWords most associated with DISCREPANT justices:")
    print(word_results.sort_values("discrepant_diff", ascending=False).head(50)["word"].to_string(index=False))

    # Words most distinctive to concordant justices
    print("\nWords most associated with CONCORDANT justices:")
    print(word_results.sort_values("concordant_diff", ascending=False).head(50)["word"].to_string(index=False))

    # Save full vocabulary
    word_results.to_csv(INTERIM_DATA_DIR / "wordscores_vocabulary.csv", index=False)

    # Save top 50 discrepant seed words
    with open(INTERIM_DATA_DIR / "discrepant_seed_words.txt", "w") as f:
        f.write("\n".join(
            word_results.sort_values("discrepant_diff", ascending=False)
            .head(50)["word"].tolist()
        ))

    # Save top 50 concordant seed words
    with open(INTERIM_DATA_DIR / "concordant_seed_words.txt", "w") as f:
        f.write("\n".join(
            word_results.sort_values("concordant_diff", ascending=False)
            .head(50)["word"].tolist()
        ))

    logger.success(f"Saved word scores and seed dictionaries to {INTERIM_DATA_DIR}")


if __name__ == "__main__":
    main()
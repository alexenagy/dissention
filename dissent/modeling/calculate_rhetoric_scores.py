from pathlib import Path
from sys import stdout
from tqdm import tqdm
import typer
from gensim.models import Word2Vec
import numpy as np
import pandas as pd
from nltk.corpus import stopwords, words
from sklearn.metrics.pairwise import cosine_similarity
import pyarrow.parquet as pq
import multiprocessing as mp
import spacy
from dissent.config import PROCESSED_DATA_DIR, INTERIM_DATA_DIR, MODELS_DIR

app = typer.Typer()

model_path = MODELS_DIR / "iteration_0009/word2vec_checkpoint_00031.model"

model = None
ideological_vectors = None
nonideological_vectors = None
ideological_mean = None
nonideological_mean = None
nlp = None
stop_words = None
english_words = None


def init_worker():
    """
    Runs once per CPU core to load heavy assets into RAM.
    """
    global model, ideological_vectors, nonideological_vectors, ideological_mean, nonideological_mean, nlp, stop_words, english_words

    # 1. Load Model
    model = Word2Vec.load(str(model_path))

    # 2. Pre-load NLP tools
    nlp = spacy.load("en_core_web_lg")
    nlp.max_length = 10000000
    stop_words = set(stopwords.words("english"))
    english_words = set(words.words())

    # 3. Pre-calculate dictionary vectors and concept means
    def get_vectors_from_file(filename):
        vecs = []
        path = INTERIM_DATA_DIR / filename
        if path.exists():
            with open(path, "r") as f:
                for line in f:
                    word = line.strip()
                    if word in model.wv:
                        vecs.append(model.wv[word])
        return vecs

    ideological_vectors = get_vectors_from_file("ideological_dictionary.txt")
    nonideological_vectors = get_vectors_from_file("nonideological_dictionary.txt")

    # Pre-compute concept vectors by averaging seed word embeddings (EMI methodology)
    ideological_mean = np.array(ideological_vectors).mean(axis=0, keepdims=True) if ideological_vectors else None
    nonideological_mean = np.array(nonideological_vectors).mean(axis=0, keepdims=True) if nonideological_vectors else None

    print(f"DEBUG: Loaded {len(ideological_vectors)} ideological vectors.")
    print(f"DEBUG: Loaded {len(nonideological_vectors)} nonideological vectors.")
    if len(ideological_vectors) == 0:
        print("CRITICAL: No ideological dictionary words were found in the Model Vocabulary!")
    if len(nonideological_vectors) == 0:
        print("CRITICAL: No nonideological dictionary words were found in the Model Vocabulary!")


# --- WORKER FUNCTIONS ---

def preprocess_text(text):
    """Tokenize, lowercase, remove stopwords, lemmatize with spaCy, and filter English words."""
    doc = nlp(text)
    return [
        token.lemma_.lower()
        for token in doc
        if token.is_alpha and token.text.lower() not in stop_words and token.lemma_.lower() in english_words
    ]


def calculate_distance(token_mean, concept_mean):
    """
    Cosine similarity between averaged document token vector and averaged concept vector.
    Follows EMI methodology: both document and concept are represented as single mean vectors.
    """
    if token_mean is None or concept_mean is None:
        return None
    return cosine_similarity(concept_mean, token_mean)[0][0]


def length_adjust(df, score_col):
    """
    Adjust rhetoric scores for opinion length following EMI methodology:
    1. Bin opinions by token count into deciles
    2. Subtract bin mean from each score
    3. Apply Z-transform within each bin
    """
    df = df.copy()
    df["length_bin"] = pd.qcut(df["token_count"], q=10, duplicates="drop")
    df[score_col] = df.groupby("length_bin")[score_col].transform(
        lambda x: (x - x.mean()) / x.std() if x.std() > 0 else x - x.mean()
    )
    return df


def process_batch(df_batch):
    """
    Explode opinions, compute rhetoric score per opinion, return with token counts
    for length adjustment.
    """
    df_batch = df_batch.explode("opinions")

    results = []
    for _, row in df_batch.iterrows():
        op = row["opinions"]
        if not isinstance(op, dict):
            continue
        text = op.get("opinion_text")
        if not text:
            continue

        tokens = preprocess_text(text)
        token_vectors = [model.wv[t] for t in tokens if t in model.wv]
        if not token_vectors:
            continue

        # Average all token embeddings into a single document vector (EMI methodology)
        token_mean = np.array(token_vectors).mean(axis=0, keepdims=True)

        ideological_score = calculate_distance(token_mean, ideological_mean)
        nonideological_score = calculate_distance(token_mean, nonideological_mean)

        if ideological_score is not None and nonideological_score is not None:
            results.append({
                "id": row["id"],
                "rhetoric_score": nonideological_score - ideological_score,
                "token_count": len(token_vectors),
            })

    if not results:
        return pd.DataFrame(columns=["id", "rhetoric_score", "token_count"])

    return pd.DataFrame(results)


def batch_inputs():
    input_file = PROCESSED_DATA_DIR / "dataset.parquet"
    parquet_file = pq.ParquetFile(input_file)

    batch_size = 100

    print(f"Streaming batches (size {batch_size})...", file=stdout)

    batch_generator = (
        b.to_pandas() for b in parquet_file.iter_batches(
            batch_size=batch_size,
            columns=["id", "opinions"]
        )
    )

    total_expected = (parquet_file.metadata.num_rows // batch_size) + 1

    with mp.Pool(processes=24, initializer=init_worker) as pool:
        processed_chunks = list(
            tqdm(
                pool.imap_unordered(process_batch, batch_generator),
                total=total_expected,
                desc="Processing Opinions",
                mininterval=10,
                maxinterval=30,
                dynamic_ncols=True
            )
        )

    print("Concatenating scores...", file=stdout)
    rhetoric_score_df = pd.concat(processed_chunks, ignore_index=True)

    # Length adjustment across full dataset before aggregating to case level
    print("Applying length adjustment...", file=stdout)
    rhetoric_score_df = length_adjust(rhetoric_score_df, "rhetoric_score")

    # Collapse multiple opinions per case into a single mean rhetoric score
    print("Aggregating to case level...", file=stdout)
    rhetoric_score_df = rhetoric_score_df.groupby("id")["rhetoric_score"].mean().reset_index()

    print("Loading metadata (year and jurisdiction)...", file=stdout)
    metadata_df = pd.read_parquet(
        input_file,
        columns=["id", "year", "court_jurisdiction"]
    )

    print("Merging and final filtering...", file=stdout)
    final_df = metadata_df.merge(rhetoric_score_df, on="id", how="left")
    final_df = final_df[["court_jurisdiction", "year", "rhetoric_score"]]

    output_path = PROCESSED_DATA_DIR / "processed_rhetoric_scores.parquet"
    final_df.to_parquet(output_path)

    print(f"Success! Saved to {output_path}", file=stdout)
    print(final_df.head(), file=stdout)


@app.command()
def main():
    batch_inputs()


if __name__ == "__main__":
    app()
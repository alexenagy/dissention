# Standard library
from pathlib import Path
from sys import stdout

# Third-party libraries
from tqdm import tqdm
import typer
from gensim.models import Word2Vec
import numpy as np
import pandas as pd
from nltk.corpus import stopwords, words
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.metrics.pairwise import cosine_similarity
import pyarrow.parquet as pq
import multiprocessing as mp

# Local application imports
from dissent.config import PROCESSED_DATA_DIR, INTERIM_DATA_DIR, MODELS_DIR

app = typer.Typer()

import nltk
REQUIRED_RESOURCES = [
    'stopwords', 
    'words', 
    'punkt', 
    'wordnet', 
    'omw-1.4',
    'punkt_tab'
]

for resource in REQUIRED_RESOURCES:
    try:
        if resource == 'punkt' or resource == 'punkt_tab':
            nltk.data.find(f'tokenizers/{resource}')
        else:
            nltk.data.find(f'corpora/{resource}')
    except LookupError:
        print(f"Downloading NLTK resource: {resource}")
        nltk.download(resource)

model_path = MODELS_DIR / "word2vec_checkpoint_00031.model"

model = None 
politics_vectors = None
evidence_vectors = None
lemmatizer = None
stop_words = None
english_words = None


def init_worker():
    """
    Runs once per CPU core to load heavy assets into RAM.
    """
    global model, politics_vectors, evidence_vectors, lemmatizer, stop_words, english_words
    
    # 1. Load Model
    model = Word2Vec.load(str(model_path))
    
    # 2. Pre-load NLP tools
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words("english"))
    english_words = set(words.words())

    # 3. Pre-calculate Seed Vectors
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

    politics_vectors = get_vectors_from_file("politics_dictionary.txt")
    evidence_vectors = get_vectors_from_file("evidence_dictionary.txt")

    print(f"DEBUG: Loaded {len(politics_vectors)} politics vectors.")
    print(f"DEBUG: Loaded {len(evidence_vectors)} evidence vectors.")
    if len(politics_vectors) == 0:
        print("CRITICAL: No politics seed words were found in the Model Vocabulary!")


# --- WORKER FUNCTIONS ---

def preprocess_text(text):
    """Tokenize, lowercase, remove stopwords, lemmatize, and filter English words."""
    tokens = word_tokenize(text.lower())
    return [
        lemma
        for word in tokens
        if word.isalpha() and word not in stop_words
        for lemma in [lemmatizer.lemmatize(word)]
        if lemma in english_words
    ]


def calculate_distance(tokens, seed_vectors):
    """Mean cosine similarity between token vectors and seed vectors."""
    if not tokens or not seed_vectors:
        return None
    
    seed_matrix = np.array(seed_vectors)
    token_vectors = [model.wv[t] for t in tokens if t in model.wv]
    if not token_vectors:
        return None
    
    token_matrix = np.array(token_vectors)
    return np.mean(cosine_similarity(seed_matrix, token_matrix))


def process_batch(df_batch):
    """
    Explode opinions, compute rhetoric score per opinion, then average per case ID.
    """
    df_batch = df_batch.explode("opinions")

    def fast_rhetoric_score(op):
        if not isinstance(op, dict):
            return None
        text = op.get("opinion_text")
        if not text:
            return None

        tokens = preprocess_text(text)
        a = calculate_distance(tokens, politics_vectors)
        b = calculate_distance(tokens, evidence_vectors)
        return b - a if (a is not None and b is not None) else None

    df_batch["rhetoric_score"] = df_batch["opinions"].apply(fast_rhetoric_score)

    # Collapse multiple opinions per case into a single mean rhetoric score
    return df_batch.groupby("id")["rhetoric_score"].mean().reset_index()


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
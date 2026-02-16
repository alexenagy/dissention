# Standard library
from pathlib import Path
from sys import stdout

# Third-party libraries
from loguru import logger
from tqdm import tqdm
import typer
from gensim.models import Word2Vec
import numpy as np
import pandas as pd
from nltk.corpus import stopwords, words
from nltk.tokenize import word_tokenize
from nltk.stem.porter import *
from nltk.stem import WordNetLemmatizer
from multiprocessing import Pool
from sklearn.metrics.pairwise import cosine_similarity
from tqdm.contrib.concurrent import process_map
import pyarrow.parquet as pq
import multiprocessing as mp
import os

# Local application imports
from dissent.config import FIGURES_DIR, PROCESSED_DATA_DIR, RAW_DATA_DIR, DATA_DIR, MODELS_DIR

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
        # Check if resource exists
        if resource == 'punkt' or resource == 'punkt_tab':
            nltk.data.find(f'tokenizers/{resource}')
        else:
            nltk.data.find(f'corpora/{resource}')
    except LookupError:
        print(f"Downloading NLTK resource: {resource}")
        nltk.download(resource)

model_path = MODELS_DIR / "word2vec_checkpoint_00031.model"

model = None 
intuition_vectors = None
evidence_vectors = None
lemmatizer = None
stop_words = None
english_words = None

def init_worker():
    """
    Runs once per CPU core to load heavy assets into RAM.
    """
    global model, intuition_vectors, evidence_vectors, lemmatizer, stop_words, english_words
    
    # 1. Load Model
    model = Word2Vec.load(str(model_path))
    
    # 2. Pre-load NLP tools
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words("english"))
    english_words = set(words.words())

    # 3. Pre-calculate Seed Vectors
    def get_vectors_from_file(filename):
        vecs = []
        path = PROCESSED_DATA_DIR / filename
        if path.exists():
            with open(path, "r") as f:
                for line in f:
                    word = line.strip()
                    if word in model.wv:
                        vecs.append(model.wv[word])
        return vecs

    intuition_vectors = get_vectors_from_file("intuition")
    evidence_vectors = get_vectors_from_file("evidence")

    # Add this inside init_worker() right after get_vectors_from_file calls:
    print(f"DEBUG: Loaded {len(intuition_vectors)} intuition vectors.")
    print(f"DEBUG: Loaded {len(evidence_vectors)} evidence vectors.")
    if len(intuition_vectors) == 0:
        print("CRITICAL: No intuition seed words were found in the Model Vocabulary!")

# --- WORKER FUNCTIONS ---

def preprocess_text(text):
    # Uses the global variables from init_worker
    tokens = word_tokenize(text.lower())
    return [
        lemmatizer.lemmatize(word)
        for word in tokens
        if word.isalpha() and word not in stop_words
        # removed the check for 'and word in english_words' above
    ]

def calculate_distance(tokens, seed_vectors):
    if not tokens or not seed_vectors:
        return None
        
    token_vectors = []
    for token in tokens:
        if token in model.wv:
            token_vectors.append(model.wv[token])
            
    if not token_vectors:
        return None

    return np.mean(cosine_similarity(seed_vectors, token_vectors))

def process_single_row(row_data):
    text = row_data.get("opinion_text")
    if not text:
        return None

    try:
        tokens = preprocess_text(text)
        a = calculate_distance(tokens, intuition_vectors)
        b = calculate_distance(tokens, evidence_vectors)
        
        if a is not None and b is not None:
            return b - a
    except Exception:
        return None
    return None

def process_batch(df_batch):
    # Explode and immediately drop rows with empty text to save iterations
    df_batch = df_batch.explode("opinions")
    
    def fast_emi(op):
        if not isinstance(op, dict): return None
        text = op.get("opinion_text")
        if not text: return None
        
        # Optimized inner loop: Only process words the model actually knows
        tokens = word_tokenize(text.lower())
        valid_tokens = []
        for word in tokens:
            # Check model vocab BEFORE expensive lemmatization
            if word in model.wv and word.isalpha() and word not in stop_words:
                lemma = lemmatizer.lemmatize(word)
                if lemma in model.wv:
                    valid_tokens.append(lemma)
        
        a = calculate_distance(valid_tokens, intuition_vectors)
        b = calculate_distance(valid_tokens, evidence_vectors)
        return b - a if (a is not None and b is not None) else None

    df_batch["emi"] = df_batch["opinions"].apply(fast_emi)
    return df_batch[["id", "emi"]]

def batch_inputs():
    input_file = PROCESSED_DATA_DIR / "dataset.parquet"
    parquet_file = pq.ParquetFile(input_file)
    
    # Smaller batch size (e.g., 100 rows per batch) makes tqdm move and keeps workers busy
    batch_size = 100 
    
    print(f"Streaming batches (size {batch_size})...", file=stdout)
    
    # Use a generator to stream data instead of loading all batches into a list first to save RAM
    batch_generator = (
        b.to_pandas() for b in parquet_file.iter_batches(
            batch_size=batch_size, 
            columns=["id", "opinions"]
        )
    )

    # Estimate total batches for tqdm
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

    # 3. Concatenate EMI Results
    print("Concatenating scores...", file=stdout)
    emi_df = pd.concat(processed_chunks, ignore_index=True)

    # 4. Load Metadata separately
    # We explicitly list ONLY the columns we want to bypass the 'Nested data' error
    print("Loading metadata (year and jurisdiction)...", file=stdout)
    metadata_df = pd.read_parquet(
        input_file, 
        columns=["id", "year", "court_jurisdiction"]
    )

    # 5. Merge and Filter
    print("Merging and final filtering...", file=stdout)
    final_df = metadata_df.merge(emi_df, on="id", how="left")
    
    # Keep only the three relevant columns
    final_df = final_df[["court_jurisdiction", "year", "emi"]]

    # 6. Save Final
    output_path = PROCESSED_DATA_DIR / "processed_parquets_emi.parquet"
    final_df.to_parquet(output_path)
    
    print(f"Success! Saved to {output_path}", file=stdout)
    print(final_df.head(), file=stdout)

def run_diagnostics(num_samples=5):
    # 1. Manually trigger the asset loading
    print("--- 1. Loading Assets ---")
    init_worker()
    
    # 2. Load a small sample SAFELY
    print(f"\n--- 2. Loading {num_samples} Samples ---")
    input_file = PROCESSED_DATA_DIR / "dataset.parquet"
    
    # Use iter_batches to avoid the ArrowNotImplementedError
    parquet_file = pq.ParquetFile(input_file)

    # Just take the first batch and the first few rows
    batch = next(parquet_file.iter_batches(batch_size=num_samples, columns=["id", "opinions"]))
    df = batch.to_pandas()
    
    df = df.explode("opinions")

    for i, row in df.iterrows():
        print(f"\n>>> Checking Case ID: {row['id']}")
        op = row.get("opinions")
        
        if not isinstance(op, dict):
            print(f"ERROR: Opinion column is {type(op)}, not a dictionary.")
            continue
            
        text = op.get("opinion_text", "")
        if not text:
            print("ERROR: 'opinion_text' key is missing or empty in the dictionary.")
            continue
            
        print(f"Raw Text Length: {len(text)} characters")
        
        # Check Preprocessing
        tokens = preprocess_text(text)
        print(f"Tokens after NLP (first 10): {tokens[:10]}")
        print(f"Total Tokens remaining: {len(tokens)}")
        
        if len(tokens) == 0:
            print("WARNING: No tokens left after preprocessing!")
            continue

        # Check Individual Distances
        dist_a = calculate_distance(tokens, intuition_vectors)
        dist_b = calculate_distance(tokens, evidence_vectors)
        
        print(f"Intuition Distance: {dist_a}")
        print(f"Evidence Distance: {dist_b}")
        
        if dist_a is not None and dist_b is not None:
            print(f"FINAL EMI SCORE: {dist_b - dist_a}")
        else:
            print("RESULT: EMI calculation returned None because vectors were empty.")

@app.command()
def main():
    batch_inputs()
    # run_diagnostics()

''' alex/aerith
#model = Word2Vec.load(str(model_path)) #type casting 1 + int("1")

def loop():
    input_file = PROCESSED_DATA_DIR / "dataset.parquet"
    
    # 1. Use ParquetFile to manage reading
    parquet_file = pq.ParquetFile(input_file)
    
    processed_chunks = []

    # 2. Iterate over the file in batches (Row Groups)
    # Using tqdm to show progress is helpful here
    print(f"Processing {parquet_file.num_row_groups} batches...", file=stdout)
    
    for batch in tqdm(parquet_file.iter_batches(), total=parquet_file.num_row_groups):
        # Convert strictly the current batch to pandas
        # This avoids the "chunked array" error because a single batch is usually contiguous
        df_batch = batch.to_pandas()
        df_batch = df_batch.explode("opinions")

        emis = []
        for i, row in df_batch.iterrows():
            try:
                # Use .get() safely on the dictionary
                text = row["opinions"].get("opinion_text") if isinstance(row["opinions"], dict) else None
                
                if text:
                    tokens = preprocess_text(text)
                    a = calculate_intuition_distance(tokens) 
                    b = calculate_evidence_distance(tokens)
                    # print(b - a) # Optional: Comment out to reduce terminal clutter
                    emis.append(b - a)
                else:
                    emis.append(None)
            except Exception as e:
                # Good to log the specific error if possible, but keeping your logic:
                emis.append(None)
                continue
        
        df_batch["emi"] = emis
        processed_chunks.append(df_batch)

    # 3. Combine all processed batches and save
    if processed_chunks:
        full_df = pd.concat(processed_chunks, ignore_index=True)
        full_df.to_parquet(PROCESSED_DATA_DIR / "processed_parquets_emi.parquet")
        print("Processing complete.", file=stdout)
    else:
        print("No data processed.", file=stdout)

def preprocess_text(text):
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words("english"))
    english_words = set(words.words())
    tokens = word_tokenize(text.lower())
    tokens = [
        lemmatizer.lemmatize(word)
        for word in tokens
        if word.isalpha() and word not in stop_words and word in english_words
    ]
    return tokens

def calculate_intuition_distance(tokens):
    intuition_vectors = []
    token_vectors = []
    for token in tokens:
        try:
            vector = model.wv[token]
            token_vectors.append(vector)
        except:
            continue
    with open(DATA_DIR / "intuition_seed_words.txt") as data:
        words = data.readlines()
        for word in words:
            vector = model.wv[word.replace("\n","")]
            intuition_vectors.append(vector)
    return np.mean(cosine_similarity(intuition_vectors, token_vectors))

def calculate_evidence_distance(tokens):
    evidence_vectors = []
    token_vectors = []
    for token in tokens:
        try:
            vector = model.wv[token]
            token_vectors.append(vector)
        except:
            continue
    with open(DATA_DIR / "evidence_seed_words.txt") as data:
        words = data.readlines()
        for word in words:
            vector = model.wv[word.replace("\n","")]
            evidence_vectors.append(vector)
    return np.mean(cosine_similarity(evidence_vectors, token_vectors))

@app.command()
def main():
    
    loop()

    seed_word_files = [DATA_DIR / "evidence_seed_words.txt", DATA_DIR / "intuition_seed_words.txt"]
    for f in seed_word_files:
        output_file = f.name
        output_file = output_file.replace("_seed_words.txt","_dictionary")
        expanded_key_words = []
        with open(f, "r") as data:
            seed_words = data.readlines()
            with open(DATA_DIR / output_file, "w") as output_data: #data is an interface, textio wrapper
                for w in seed_words:
                    output_data.write(w)
            print(type(data))
        for word in seed_words:
            cleaned_word = word.replace("\n","")
            similar = model.wv.most_similar(cleaned_word)
            for s in similar:
                if s[1] > 0.5:
                    expanded_key_words.append(s[0])
        with open(DATA_DIR / output_file, "a") as data: #data is an interface, textio wrapper
            for w in expanded_key_words:
                data.write(w + "\n")
            print(type(data))
   
   # with open(for f in seed_word_files)
   # words_to_test = 
    
   # for w in words_to_test:
   #    sims = model.wv.most_similar(w)
'''

if __name__ == "__main__":
    app()

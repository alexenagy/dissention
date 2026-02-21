import logging
import os
from multiprocessing import Pool
from pathlib import Path
import pandas as pd
import spacy
from gensim.models import Word2Vec
from loguru import logger
from nltk.corpus import stopwords, words
from tqdm import tqdm
from dissent.config import INTERIM_DATA_DIR, MODELS_DIR, RAW_DATA_DIR

# Configuration
logging.basicConfig(
    format="%(asctime)s : %(levelname)s : %(message)s",
    level=logging.INFO,
)
OUTPUT_DIR = MODELS_DIR / "iteration_0009"
_ = os.makedirs(OUTPUT_DIR, exist_ok=True)
WORKERS = 64


def init_worker():
    global nlp
    nlp = spacy.load("en_core_web_lg", disable=["parser", "ner"])
    nlp.max_length = 2000000


def preprocess_text(text):
    """
    Preprocess text for Word2Vec training.

    Steps:
    1. Tokenize and lemmatize with spaCy
    2. Lowercase
    3. Remove non-alphabetic tokens
    4. Remove stopwords
    5. Filter to English words only
    """
    doc = nlp(text)
    stop_words = set(stopwords.words("english"))
    english_words = set(words.words())
    return [
        token.lemma_.lower()
        for token in doc
        if token.is_alpha and token.text.lower() not in stop_words and token.lemma_.lower() in english_words
    ]


def main():
    """
    Train Word2Vec model on state supreme court opinions.

    Pipeline:
    1. Initialize Word2Vec model with skip-gram architecture
    2. For each raw data shard:
       a. Load and filter to state supreme courts only
       b. Extract opinion text from all opinions
       c. Preprocess text in parallel (tokenize, lemmatize, filter)
       d. Update vocabulary (first shard builds, subsequent update)
       e. Train model for 10 epochs on preprocessed text
       f. Save checkpoint after each shard
    3. Verify model quality with similarity check
    """

    # Step 1: Initialize Word2Vec model
    model = Word2Vec(
        vector_size=300,
        window=5,
        min_count=20,
        workers=WORKERS,
        sg=1,  # Skip-gram architecture
    )

    # Step 2: Process each data shard
    for i, file in tqdm(enumerate(RAW_DATA_DIR.rglob("part*")), desc="Processing shards"):
        docs = []

        # Step 2a: Load and filter data
        df = pd.read_parquet(file)
        print(f"Length before filtering: {len(df)}")
        df = df[df["court_type"] == "S"]  # State supreme courts only
        df["year"] = df["date_filed"].astype(str).str.extract(r"(\d{4})")[0].astype(int)
        df.to_parquet(INTERIM_DATA_DIR / f"shard_{i:05d}.parquet")

        # Step 2b: Extract opinion text
        for _, row in tqdm(df.iterrows(), total=len(df), desc="Extracting opinions"):
            opinions = row.get("opinions")
            if opinions is not None:
                for o in opinions:
                    opinion_text = o.get("opinion_text")
                    if opinion_text is not None:
                        docs.append(opinion_text)
                    else:
                        continue
            else:
                continue

        # Step 2c: Preprocess text in parallel
        with Pool(WORKERS, initializer=init_worker) as p:
            preprocessed_sentences = list(
                tqdm(p.imap(preprocess_text, docs), total=len(docs), desc="Preprocessing text")
            )

        # Step 2d: Build/update vocabulary
        if i == 0:
            model.build_vocab(preprocessed_sentences)
        else:
            model.build_vocab(preprocessed_sentences, update=True)

        if not model.wv.key_to_index:
            raise ValueError("Vocabulary is empty after build_vocab")

        # Step 2e: Train model
        model.train(
            preprocessed_sentences,
            total_examples=len(preprocessed_sentences),
            epochs=10,
        )

        # Step 2f: Save checkpoint
        model.save(str(OUTPUT_DIR / f"word2vec_checkpoint_{i:05d}.model"))
        logger.success(f"Checkpoint {i} saved. Word2Vec model generation complete.")

        # Step 3: Verify model quality
        try:
            similar_words = model.wv.most_similar("opinion", topn=5)
            print("Most similar words to 'opinion':", similar_words)
        except KeyError as e:
            print(f"KeyError: {e}")


if __name__ == "__main__":
    main()
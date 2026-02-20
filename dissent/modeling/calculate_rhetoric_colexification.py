# For analyzing how similar evidence/political dictionaries are to one another

# Standard library
import logging
import os

# Third-party libraries
import typer
from gensim.models import Word2Vec
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd
from tqdm import tqdm

# Local application imports
from dissent.config import MODELS_DIR, DATA_DIR

logging.basicConfig(
    format="%(asctime)s : %(levelname)s : %(message)s",
    level=logging.INFO,
)
app = typer.Typer()

@app.command()
def main():
    model_path = MODELS_DIR / "word2vec_checkpoint_00031.model"
    model = Word2Vec.load(str(model_path))

    # Load all words from txt files using rglob
    evidence_words = []
    politics_words = []
    
    txt_files = DATA_DIR.rglob("*.txt")
    
    for file_path in txt_files: 
        with open(file_path, "r") as f:  
            words_to_test = f.readlines()
            for word in words_to_test:
                words_cleaned = word.replace("\n","")
                if words_cleaned:
                    if "evidence" in file_path.name:
                        evidence_words.append(words_cleaned)
                    elif "politics" in file_path.name:
                        politics_words.append(words_cleaned)

    # Filter words that exist in the model's vocabulary
    valid_evidence = [w for w in evidence_words if w in model.wv]
    valid_politics = [w for w in politics_words if w in model.wv]
    
    if not valid_evidence or not valid_politics:
        print("Error: Need valid evidence and politics words")
        return
    
    # Get word vectors
    evidence_vectors = [model.wv[w] for w in valid_evidence]
    politics_vectors = [model.wv[w] for w in valid_politics]
    
    # Compute cosine similarity matrix
    similarity_matrix = cosine_similarity(evidence_vectors, politics_vectors)
    
    # Print matrix
    print(similarity_matrix)

if __name__ == "__main__":
    main()
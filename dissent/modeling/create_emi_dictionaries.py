# Standard library
from pathlib import Path

# Third-party libraries
from loguru import logger
from tqdm import tqdm
import typer
from gensim.models import Word2Vec

# Local application imports
from dissent.config import FIGURES_DIR, PROCESSED_DATA_DIR, DATA_DIR, MODELS_DIR, RAW_DATA_DIR

app = typer.Typer()

model_path = MODELS_DIR / "word2vec_checkpoint_00031.model"
model = Word2Vec.load(str(model_path))

@app.command()
def main():
    seed_word_files = [
        RAW_DATA_DIR / "evidence_seed_words.txt", 
        RAW_DATA_DIR / "intuition_seed_words.txt"
    ]
    
    # Store expanded words for each dictionary
    all_dictionaries = {}
    
    # Step 1: Expand each dictionary
    for f in seed_word_files:
        output_file = f.name.replace("_seed_words.txt", "")
        expanded_key_words = set()  # Use set to avoid duplicates
        
        with open(f, "r") as data:
            seed_words = [line.strip() for line in data.readlines()]
        
        # Add seed words
        all_words = set(seed_words)
        
        # Expand using Word2Vec
        for word in seed_words:
            try:
                similar = model.wv.most_similar(word)
                for s in similar:
                    if s[1] > 0.50:
                        expanded_key_words.add(s[0])
            except:
                continue
        
        # Combine seed + expanded
        all_words.update(expanded_key_words)
        all_dictionaries[output_file] = all_words
    
    # Step 2: Remove overlap between evidence and intuition
    evidence = all_dictionaries['evidence']
    intuition = all_dictionaries['intuition']
    overlap = evidence & intuition
    
    all_dictionaries['evidence'] = evidence - overlap
    all_dictionaries['intuition'] = intuition - overlap
    
    print(f"Removed {len(overlap)} overlapping words")
    
    # Step 3: Write final dictionaries
    for name, words in all_dictionaries.items():
        with open(PROCESSED_DATA_DIR / name, "w") as f:
            for w in sorted(words):
                f.write(w + "\n")
        print(f"Wrote {len(words)} words to {name}")

if __name__ == "__main__":
    app()
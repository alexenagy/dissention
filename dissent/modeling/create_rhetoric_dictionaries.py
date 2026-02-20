# Standard library
from pathlib import Path

# Third-party libraries
from tqdm import tqdm
import typer
from gensim.models import Word2Vec

# Local application imports
from dissent.config import INTERIM_DATA_DIR, MODELS_DIR, RAW_DATA_DIR

app = typer.Typer()

model_path = MODELS_DIR / "word2vec_checkpoint_00031.model"
model = Word2Vec.load(str(model_path))

@app.command()
def main():
    seed_word_files = [
        RAW_DATA_DIR / "evidence_seed_words.txt", 
        RAW_DATA_DIR / "politics_seed_words.txt"
    ]
    
    # Store expanded words for each dictionary
    all_dictionaries = {}
    
    # Step 1: Expand each dictionary
    for f in seed_word_files:
        # Explicit key names based on file content
        if "evidence" in f.name:
            dict_key = "evidence"
        elif "politics" in f.name:
            dict_key = "politics"
        else:
            raise ValueError(f"Unexpected filename: {f.name}")
        
        expanded_key_words = set()
        
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
        all_dictionaries[dict_key] = all_words
    
    # Step 2: Remove overlap between evidence and politics
    evidence = all_dictionaries['evidence']
    politics = all_dictionaries['politics']
    overlap = evidence & politics
    
    all_dictionaries['evidence'] = evidence - overlap
    all_dictionaries['politics'] = politics - overlap
    
    print(f"Removed {len(overlap)} overlapping words")
    
    # Step 3: Write final dictionaries
    for name, words in all_dictionaries.items():
        output_filename = f"{name}_dictionary.txt"
        with open(INTERIM_DATA_DIR / output_filename, "w") as f:
            for w in sorted(words):
                f.write(w + "\n")
        print(f"Wrote {len(words)} words to {output_filename}")

if __name__ == "__main__":
    app()
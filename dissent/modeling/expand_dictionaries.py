from pathlib import Path
from tqdm import tqdm
import typer
from gensim.models import Word2Vec
from dissent.config import PROCESSED_DATA_DIR, INTERIM_DATA_DIR, MODELS_DIR

app = typer.Typer()

model_path = MODELS_DIR / "iteration_0009/word2vec_checkpoint_00031.model"
model = Word2Vec.load(str(model_path))

@app.command()
def main():
    seed_word_files = [
        INTERIM_DATA_DIR / "discrepant_seed_words.txt",
        INTERIM_DATA_DIR / "concordant_seed_words.txt"
    ]

    # Store expanded words for each dictionary
    all_dictionaries = {}

    # Step 1: Expand each dictionary
    for f in seed_word_files:
        if "concordant" in f.name:
            dict_key = "concordant"
        elif "discrepant" in f.name:
            dict_key = "discrepant"
        else:
            raise ValueError(f"Unexpected filename: {f.name}")

        with open(f, "r") as data:
            seed_words = [line.strip() for line in data.readlines()]

        # Start with seed words
        all_words = set(seed_words)

        # Expand using Word2Vec nearest neighbors
        expanded_words = set()
        for word in seed_words:
            try:
                similar = model.wv.most_similar(word)
                for similar_word, similarity_score in similar:
                    if similarity_score > 0.65:
                        expanded_words.add(similar_word)
            except KeyError:
                continue

        # Combine seed + expanded
        all_words.update(expanded_words)
        all_dictionaries[dict_key] = all_words

        print(f"{dict_key}: {len(seed_words)} seed words expanded to {len(all_words)} total words")

    # Step 2: Remove overlap between discrepant and concordant
    discrepant = all_dictionaries["discrepant"]
    concordant = all_dictionaries["concordant"]
    overlap = discrepant & concordant

    all_dictionaries["discrepant"] = discrepant - overlap
    all_dictionaries["concordant"] = concordant - overlap

    print(f"Removed {len(overlap)} overlapping words")

    # Step 3: Write final dictionaries
    for name, dict_words in all_dictionaries.items():
        output_filename = f"{name}_dictionary.txt"
        with open(PROCESSED_DATA_DIR / output_filename, "w") as f:
            for w in sorted(dict_words):
                f.write(w + "\n")
        print(f"Wrote {len(dict_words)} words to {output_filename}")


if __name__ == "__main__":
    app()
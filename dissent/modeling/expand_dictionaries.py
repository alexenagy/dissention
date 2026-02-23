from pathlib import Path
from tqdm import tqdm
import typer
from gensim.models import Word2Vec
from dissent.config import INTERIM_DATA_DIR, MODELS_DIR

app = typer.Typer()

model_path = MODELS_DIR / "iteration_0009/word2vec_checkpoint_00031.model"
model = Word2Vec.load(str(model_path))

@app.command()
def main():
    seed_word_files = [
        INTERIM_DATA_DIR / "ideological_seed_words.txt",
        INTERIM_DATA_DIR / "nonideological_seed_words.txt"
    ]

    # Store expanded words for each dictionary
    all_dictionaries = {}

    # Step 1: Expand each dictionary
    for f in seed_word_files:
        if "nonideological" in f.name:
            dict_key = "nonideological"
        elif "ideological" in f.name:
            dict_key = "ideological"
        else:
            raise ValueError(f"Unexpected filename: {f.name}")

        expanded_words = set()

        with open(f, "r") as data:
            seed_words = [line.strip() for line in data.readlines()]

        # Start with seed words
        all_words = set(seed_words)

        # Expand using Word2Vec
        for word in seed_words:
            try:
                similar = model.wv.most_similar(word)
                for s in similar:
                    if s[1] > 0.65:
                        expanded_words.add(s[0])
            except:
                continue

        # Combine seed + expanded
        all_words.update(expanded_words)
        all_dictionaries[dict_key] = all_words

    # Step 2: Remove overlap between ideological and nonideological
    ideological = all_dictionaries["ideological"]
    nonideological = all_dictionaries["nonideological"]
    overlap = ideological & nonideological

    all_dictionaries["ideological"] = ideological - overlap
    all_dictionaries["nonideological"] = nonideological - overlap

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
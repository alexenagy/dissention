import logging
import os
import typer
from gensim.models import Word2Vec
from dissent.config import MODELS_DIR

logging.basicConfig(
    format="%(asctime)s : %(levelname)s : %(message)s",
    level=logging.INFO,
)
app = typer.Typer()

@app.command()
def main():
    model_path = MODELS_DIR / "iteration_0009/word2vec_checkpoint_00031.model"
    model = Word2Vec.load(str(model_path))

    words_to_test = [
        "respectfully",
    ]
    for w in words_to_test:
        sims = model.wv.most_similar(w)
        print(f"\n\nWords most similar to {w}:\n", str(sims))


if __name__ == "__main__":
    main()

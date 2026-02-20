# Just for testing/exploring word similarities

# Standard library
import logging
import os

# Third-party libraries
import typer
from gensim.models import Word2Vec

# Local application imports
from dissent.config import MODELS_DIR

logging.basicConfig(
    format="%(asctime)s : %(levelname)s : %(message)s",
    level=logging.INFO,
)
app = typer.Typer()

@app.command()
def main():
    model_path = MODELS_DIR / "word2vec_checkpoint_00031.model"
    model = Word2Vec.load(str(model_path))

    words_to_test = [
        "partisan",
    ]
    for w in words_to_test:
        sims = model.wv.most_similar(w)
        print(f"\n\nWords most similar to {w}:\n", str(sims))


if __name__ == "__main__":
    main()

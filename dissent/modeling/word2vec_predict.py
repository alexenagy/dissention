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
    model = Word2Vec.load(str(model_path)) #type casting 1 + int("1")

    words_to_test = [
        "evidence",
        '''
        "undemocratic",
        "concur",
        "murder",
        "constitution",
        "precedent",
        "abortion",
        "gender",
        "sex",
        "education",
        "religion",
        "homosexual",
        "woman",
        "female",
        "male",
        "freedom",
        "poverty",
        "partisan",
        "political",
        "wealth",
        "voting",
        "trump",
        "literalism",
        "riot",
        "insurrection",
        "equality",
        "strongly", 
        '''   
    ]
    for w in words_to_test:
        sims = model.wv.most_similar(w)
        print(f"\n\nWords most similar to {w}:\n", str(sims))


if __name__ == "__main__":
    main()

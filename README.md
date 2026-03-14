# dissention

Mixed‑methods analysis of dissenting opinion‑writing in U.S. state supreme courts.

The project combines:

- **Synthetic control methods** to study how changes in selection mechanisms (e.g. nonpartisan → partisan elections) affect dissent rates.
- **Computational textual analysis** (Word2Vec, Wordscores, and an Evidence‑Minus‑Intuition framework) to distinguish **discrepant** from **concordant** rhetoric in dissenting opinions.

The main research paper lives in `reports/article.md` (compiled to `reports/article.pdf`).

## Repository Overview

- `dissent/` — Python package with modeling and plotting code:
  - `dataset.py`: helpers for constructing the analysis dataset.
  - `modeling/`:
    - `train_word2vec.py`: train Word2Vec on the COLD Cases corpus.
    - `create_seed_words.py`: build initial discrepant vs. conventional seed vocabularies via Wordscores.
    - `expand_dictionaries.py`: expand seed dictionaries using Word2Vec.
    - `calculate_rhetoric_scores.py`: compute rhetoric scores for opinions.
  - `plots/`: scripts to reproduce all figures (rhetoric over time, by mechanism, event studies, semantic maps, etc.).
- `data/` — (created by the pipeline)
  - `raw/`: COLD Cases dataset downloaded from HuggingFace.
  - `interim/`: intermediate files (Wordscores vocabulary, seed word lists, expanded dictionaries).
  - `processed/`: final analysis datasets (e.g. `dataset.parquet`, `processed_rhetoric_scores.parquet`).
- `reports/`
  - `article.md`: manuscript for the paper.
  - `article.pdf`: compiled paper.
  - `references/`: primary and secondary bibliographies + CSL style.
  - `figures/`: exported figures used in the paper.
- `scripts/`: SLURM batch scripts (`w2v_train.sh`, `make_dataset.sh`, `calculate_rhetoric_scores.sh`) for the long‑running jobs.
- `docs/`: MkDocs configuration and user‑facing documentation (see `docs/docs/getting-started.md`).
- `pyproject.toml`: project metadata and Python dependencies.
- `Makefile`: self‑documenting make targets to run the pipeline.

## Installation

Requirements:

- Python 3.12 (managed via `uv`)
- `uv` for environment + dependency management
- GNU Make
- SLURM (or an equivalent batch system) for the long‑running jobs
- `huggingface-cli` for data download

Steps:

```bash
git clone https://github.com/alexenagy/dissention.git
cd dissention

# Create and activate a uv virtual environment
make create_environment
source .venv/bin/activate  # on macOS / Linux

# Install dependencies
make requirements
```

See all available make rules with:

```bash
make help
```

## Core Pipeline

The main analysis pipeline is orchestrated via the `Makefile`:

1. **Download data**

   ```bash
   make download
   ```

   - Downloads the COLD Cases dataset (`harvard-lil/cold-cases`) from HuggingFace into `data/raw/`.

2. **Train Word2Vec**

   ```bash
   make train
   ```

   - Runs the Word2Vec training stage (typically as a batch job on your cluster).
   - Filters COLD Cases to state supreme court opinions, preprocesses with spaCy, and trains a Word2Vec model.

3. **Build dataset**

   ```bash
   make dataset
   ```

   - Submits `scripts/make_dataset.sh` as a batch job on your cluster.
   - Merges opinion shards with CF‑scores from DIME and writes `data/processed/dataset.parquet`.

4. **Generate Wordscores seed vocabulary**

   ```bash
   make wordscores
   ```

   - Runs `dissent/modeling/create_seed_words.py`.
   - Produces `data/interim/wordscores_vocabulary.csv`.
   - You then manually curate:
     - `data/interim/discrepant_seed_words.txt`
     - `data/interim/concordant_seed_words.txt`
       (discrepant vs. concordant seed word lists)

5. **Expand dictionaries**

   ```bash
   make expand
   ```

   - Runs `dissent/modeling/expand_dictionaries.py` to expand seed dictionaries using Word2Vec similarity.

6. **Calculate rhetoric scores**

   ```bash
   make rhetoric
   ```

   - Submits `scripts/calculate_rhetoric_scores.sh` as a batch job on your cluster.
   - Runs `dissent/modeling/calculate_rhetoric_scores.py` and writes `data/processed/processed_rhetoric_scores.parquet`.

For a high‑level guide through this sequence, use:

```bash
make pipeline
```

This prints the intended order of operations and where manual steps are required. It does **not** automatically wait on HPC batch jobs; you must monitor them yourself with your scheduler’s tools (e.g. `squeue`, `qstat`, `bjobs`).

## Reproducing Figures

- Run analysis scripts from the project root, e.g.:

  ```bash
  uv run python dissent/analysis/rhetoric_event_study.py
  ```

  Outputs are written into `reports/figures/` and `dissent/analysis/` figure paths as configured in each script.

## Documentation

Project documentation is built with MkDocs (`docs/mkdocs.yml`). To serve the docs locally:

```bash
cd docs
uv run mkdocs serve
```

Then open the URL shown in your terminal (typically `http://127.0.0.1:8000`) to browse the docs, including the detailed getting started guide.

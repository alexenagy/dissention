# dissention

Mixed‑methods analysis of dissenting opinion‑writing in U.S. state supreme courts.

This project:

- studies how **judicial selection mechanisms** (partisan, nonpartisan, appointment, retention) shape dissent rates and dissenting rhetoric on state high courts;
- uses a **synthetic control design** to assess North Carolina’s 2018 switch from nonpartisan to partisan elections; and
- applies **computational text analysis** (Word2Vec, Wordscores, and an Evidence‑Minus‑Intuition rhetoric score) to 72,480 dissenting opinions to distinguish **discrepant** vs. **concordant** dissent.

## What lives where

- `dissent/` — Python package with all analysis code:
  - `config.py`: paths and global configuration.
  - `dataset.py`: build the panel dataset (COLD Cases + PAJID + covariates).
  - `modeling/`:
    - `train_word2vec.py`: train the Word2Vec model on COLD Cases.
    - `wordscores_create_seed_words.py`: construct discrepant/concordant seed vocabularies.
    - `expand_dictionaries.py`: expand seed vocabularies and write final dictionaries.
    - `calculate_rhetoric_scores.py`: compute rhetoric scores for each dissent.
  - `analysis/`: scripts that produce all figures and descriptive outputs used in the paper.
  - `scm/`: synthetic control (SCM) helpers for the North Carolina case and related robustness checks.
- `data/` — created by the pipeline:
  - `raw/`: COLD Cases corpus from HuggingFace.
  - `interim/`: intermediate files (Wordscores vocab, seed word lists, expanded dictionaries).
  - `processed/`: final datasets (`dataset.parquet`, `processed_rhetoric_scores.parquet`, etc.).
- `reports/`:
  - `article.md` / `article.pdf`: main manuscript.
  - `references/`: primary/secondary `.bib` files, CSL style, and the multiple‑bibliographies Lua filter.
  - `figures/`: exported figures.
- `Makefile`: entry points for the full pipeline (`download`, `train`, `dataset`, `wordscores`, `expand`, `rhetoric`, `pipeline`).

## How to use this repo

High‑level workflow:

1. Set up the environment with `uv` (`make create_environment`, then `make requirements`).
2. Run the **data + modeling pipeline** via the `Makefile` targets (see `docs/getting-started.md` for details).
3. Use the scripts in `dissent/analysis/` to regenerate figures and tables.

The rest of this documentation site goes into more detail on each stage of the pipeline and how the analysis connects back to the questions about judicial independence and dissent in state supreme courts.


# Getting Started

This page explains how to set up the `dissention` environment, run the full research pipeline, and reproduce the paper and figures in this repository.

## System Dependencies

- **Python**: 3.12 (managed with `uv`)
- **uv**: for environment + dependency management
- **GNU Make**
- **Batch scheduler** on your HPC (e.g. SLURM, PBS, LSF, Grid Engine) for the long‑running training / dataset / rhetoric jobs
- **huggingface-cli**: for downloading the COLD Cases dataset
- **pandoc ≥ 2.4** and a LaTeX engine (e.g. `xelatex`) to build the paper PDF

## Installation

1. Clone the repository:
   - `git clone https://github.com/alexenagy/dissention.git`
   - `cd dissention`
2. Create a virtual environment:
   - `make create_environment`
   - Activate it:
     - macOS / Linux: `source .venv/bin/activate`
     - Windows (PowerShell): `.venv\Scripts\Activate.ps1`
3. Install Python dependencies:
   - `make requirements`

You can see all available `make` targets with:

```bash
make help
```

## Core Pipeline

The core analysis pipeline is orchestrated via `make` targets. By default, some targets (`make train`, `make dataset`, `make rhetoric`) are intended to run as **batch jobs** on a cluster, but you can:

- keep the existing behavior if your HPC uses a SLURM‑like scheduler, or
- edit the corresponding rules in the `Makefile` to:
  - swap `sbatch` for your site’s submission command (e.g. `qsub`, `bsub`), or
  - replace the submission command with a direct `uv run ...` call to run locally.

### 1. Download Data

```bash
make download
```

Downloads the COLD Cases dataset from HuggingFace into `data/raw/`.

### 2. Train Word2Vec

```bash
make train
```

Runs the Word2Vec training stage on your cluster. In the default setup this is submitted as a batch job that:

- Filters the COLD Cases corpus to state supreme court opinions
- Preprocesses text using spaCy
- Trains the Word2Vec model (`dissent/modeling/train_word2vec.py`)

Wait for this stage to complete before moving on.

### 3. Build Dataset

```bash
make dataset
```

Runs the dataset construction stage (typically as a batch job on your cluster). This step merges:

- Opinion shards from COLD Cases
- CF-scores from DIME

and writes a processed panel dataset to:

- `data/processed/dataset.parquet`

### 4. Generate Wordscores Seed Vocabulary

```bash
make wordscores
```

Runs `dissent/modeling/wordscores_create_seed_words.py` (via `uv run`) to:

- Apply Wordscores anchored by CF-scores
- Produce a ranked vocabulary at `data/interim/wordscores_vocabulary.csv`

Manually review this file and edit:

- `data/interim/discrepant_seed_words.txt`
- `data/interim/concordant_seed_words.txt`

to finalize the discrepant vs. concordant seed dictionaries.

### 5. Expand Dictionaries with Word2Vec

```bash
make expand
```

Runs `dissent/modeling/expand_dictionaries.py` to expand the seed dictionaries using Word2Vec cosine similarity. Final dictionaries are written back into `data/interim/`.

### 6. Calculate Rhetoric Scores

```bash
make rhetoric
```

Runs the rhetoric‑scoring stage (again, typically as a batch job), which invokes `dissent/modeling/calculate_rhetoric_scores.py` to:

- Score each opinion along discrepant vs. concordant rhetoric dimensions
- Save results to `data/processed/processed_rhetoric_scores.parquet`

### 7. End‑to‑End Pipeline Helper

You can see the intended full sequence via:

```bash
make pipeline
```

This target prints the ordered steps and the points at which you need to:

- Wait for your HPC jobs to finish
- Manually edit the seed word files

It does **not** automatically block on batch‑job completion; you still need to monitor your jobs with your site’s usual tools (e.g. `squeue`, `qstat`, `bjobs`).

## Reproducing Plots

- Analysis scripts live in `dissent/analysis/` (e.g. `rhetoric_event_study.py`, `rhetoric_trend_plot.py`, `rhetoric_by_mechanism.py`). Run them with:

  ```bash
  uv run python dissent/analysis/<script_name>.py
  ```
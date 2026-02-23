# Getting Started

## System Dependencies

- `uv`

## Installation

1. Clone the repository: `git clone github.com/aerithnetzer/dissention.git`
2. `cd` into the repository
3. Run `make create_environment`
4. Run `make requirements`

## Pipeline

### 1. Download Data

Run `make download`

This downloads the COLD Cases dataset from HuggingFace to `data/raw/`.

### 2. Train Word2Vec

Run `make train`

Submits a SLURM job that filters the COLD Cases corpus to state supreme court opinions, preprocesses text using spaCy, and trains a Word2Vec model. Wait for this job to complete before proceeding.

### 3. Build Dataset

Run `make dataset`

Submits a SLURM job that merges opinion shards with CF-scores from DIME and saves the processed dataset to `data/processed/dataset.parquet`.

### 4. Generate Wordscores

Run `make wordscores`

Applies the Wordscores method anchored by CF-scores to produce a ranked vocabulary. Results are saved to `data/interim/wordscores_vocabulary.csv`.

Manually review `wordscores_vocabulary.csv` and edit `data/interim/ideological_seed_words.txt` and `data/interim/nonideological_seed_words.txt` to finalize seed dictionaries before proceeding.

### 5. Expand Dictionaries

Run `make expand`

Expands seed dictionaries using Word2Vec cosine similarity and saves final dictionaries to `data/interim/`.

### 6. Calculate Rhetoric Scores

Run `make rhetoric`

Submits a SLURM job that calculates rhetoric scores across the full corpus and saves results to `data/processed/processed_rhetoric_scores.parquet`.
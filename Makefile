#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_NAME = dissention
PYTHON_VERSION = 3.12
PYTHON_INTERPRETER = python

#################################################################################
# COMMANDS                                                                      #
#################################################################################

## Install Python dependencies
.PHONY: requirements
requirements:
	uv sync

## Delete all compiled Python files
.PHONY: clean
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

## Lint using ruff (use `make format` to do formatting)
.PHONY: lint
lint:
	ruff format --check
	ruff check

## Format source code with ruff
.PHONY: format
format:
	ruff check --fix
	ruff format

## Set up Python interpreter environment
.PHONY: create_environment
create_environment:
	uv venv --python $(PYTHON_VERSION)
	@echo ">>> New uv virtual environment created. Activate with:"
	@echo ">>> Windows: .\\\\.venv\\\\Scripts\\\\activate"
	@echo ">>> Unix/macOS: source ./.venv/bin/activate"

## Download COLD Cases dataset from HuggingFace
.PHONY: download
download:
	uv run huggingface-cli download harvard-lil/cold-cases --repo-type dataset --local-dir data/raw/

## Train Word2Vec model on COLD Cases corpus (submit as SLURM job)
.PHONY: train
train:
	sbatch scripts/w2v_train.sh

## Build processed dataset with CF-scores (submit as SLURM job)
.PHONY: dataset
dataset:
	sbatch scripts/make_dataset.sh

## Generate Wordscores seed word candidates
.PHONY: wordscores
wordscores:
	uv run dissent/modeling/create_seed_words.py

## Expand seed dictionaries using Word2Vec
.PHONY: expand
expand:
	uv run dissent/modeling/expand_dictionaries.py

## Calculate rhetoric scores across full corpus (submit as SLURM job)
.PHONY: rhetoric
rhetoric:
	sbatch scripts/calculate_rhetoric_scores.sh

## Run full pipeline in order (requires SLURM jobs to complete between steps)
.PHONY: pipeline
pipeline:
	@echo "Step 1: Download data"
	$(MAKE) download
	@echo "Step 2: Train Word2Vec"
	$(MAKE) train
	@echo "Step 3: Build dataset"
	$(MAKE) dataset
	@echo "Step 4: Generate Wordscores seed words"
	$(MAKE) wordscores
	@echo "Step 5: Manually review data/interim/wordscores_vocabulary.csv"
	@echo "        Edit data/interim/discrepant_seed_words.txt and data/interim/concordant_seed_words.txt"
	@echo "        Then run: make expand"
	@echo "Step 6: Calculate rhetoric scores"
	@echo "        Run: make rhetoric"

#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys; \
lines = '\n'.join([line for line in sys.stdin]); \
matches = re.findall(r'\n## (.*)\n[\s\S]+?\n([a-zA-Z_-]+):', lines); \
print('Available rules:\n'); \
print('\n'.join(['{:25}{}'.format(*reversed(match)) for match in matches]))
endef
export PRINT_HELP_PYSCRIPT

help:
	@$(PYTHON_INTERPRETER) -c "${PRINT_HELP_PYSCRIPT}" < $(MAKEFILE_LIST)
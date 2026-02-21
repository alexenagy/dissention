#!/bin/bash
#SBATCH -A p32234              # Allocation
#SBATCH -p normal
#SBATCH -t 24:00:00             # Walltime/duration of the job
#SBATCH -N 1                    # Number of Nodes
#SBATCH --mem=256G               # Memory per node in GB needed for a job. Also see --mem-per-cpu
#SBATCH --ntasks-per-node=24     # Number of Cores (Processors)
#SBATCH --mail-user=alexandrianagy2026@u.northwestern.edu

#uv run dissent/modeling/calculate_rhetoric_scores.py
uv run dissent/modeling/w2v_train.py
#!/bin/bash
#SBATCH --job-name=PostProcess
#SBATCH --time=00:05:00
#SBATCH --ntasks=22

scontrol show jobid -dd ${SLURM_JOBID} 

time python UTILS/analysis_batch.py $SLURM_NTASKS


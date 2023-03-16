#!/bin/bash
#SBATCH --job-name=ArrayJobTest
#SBATCH --output=array_job_out_%A_%a.txt
#SBATCH --error=array_job_err_%A_%a.txt
#SBATCH --account=project_2004306
#SBATCH --time=00:05:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=4G
#SBATCH --partition=small
#SBATCH --array=1-3

module load geoconda

# For looping through all the files:

# Make a list of input files
readlink -f /appl/data/geo/sentinel/s2_example_data/L2A/S2* > image_path_list.txt

# Select the inputfile from row n to the array job n.
image_path=$(sed -n ${SLURM_ARRAY_TASK_ID}p image_path_list.txt)

# Feed the filename to the Python script
srun python array_job_example.py $image_path

#!/bin/sh
# ****************************************************************************
# Wrapper script for submitting jobs on ACRC HPC
# docs: https://www.acrc.bris.ac.uk/protected/hpc-docs/index.html
# ****************************************************************************
#SBATCH --job-name=rhime_eg
#SBATCH --output=inversions_eg.out
#SBATCH --error=inversions_eg.err
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=4
#SBATCH --time=08:00:00
#SBATCH --mem=50gb
#SBATCH --account=chem007981


# Set up Python environment
module load lang/python/anaconda
source /sw/lang/anaconda.3.10.4-2021-11-fencis/bin/activate  rhime_openghg

#conda info

cd /user/home/wz22079/my_openghg/openghg
echo $PWD
echo "Begin Inversion"

python ~/rhime_with_openghg/rhime_with_openghg/rhime/run_rhime.py -c ~/rhime_with_openghg/rhime_with_openghg/rhime/config/rhime_input_template_example.ini

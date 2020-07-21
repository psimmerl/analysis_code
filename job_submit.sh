#!/bin/bash

#commented out SBATCH --mem-per-cpu=2000

run-groovy wvq2.groovy /cache/clas12/rg-a/production/recon/fall2018/torus-1/pass1/v0/dst/train/skim4/skim4_005038.hipo

python simple_run_wvq2.py
#python run_wvq2.py



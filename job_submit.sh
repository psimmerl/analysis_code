#!/bin/bash

#SBATCH --mem-per-cpu=1500

dir=/cache/clas12/rg-a/production/recon/fall2018/torus-1/pass1/v0/dst/train/skim4

run-groovy gen_hist.groovy $dir/skim4_005038.hipo $dir/skim4_005249.hipo $dir/skim4_005248.hipo #$dir/skim4_005232.hipo $dir/skim4_005231.hipo 
#$dir/skim4_005222.hipo $dir/skim4_005221.hipo $dir/skim4_005234.hipo $dir/skim4_005233.hipo $dir/skim4_005219.hipo $dir/skim4_005124.hipo $dir/skim4_005230.hipo $dir/skim4_005191.hipo $dir/skim4_005197.hipo $dir/skim4_005203.hipo $dir/skim4_005196.hipo $dir/skim4_005261.hipo $dir/skim4_005125.hipo $dir/skim4_005128.hipo $dir/skim4_005198.hipo

#python run_q2w.py
python run_phase.py


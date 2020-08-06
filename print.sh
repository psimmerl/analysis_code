#!/bin/bash
while [ True ]
do 
  clear 
  squeue -u psimmerl 
  tail -n 50 slurm-18624424.out
  sleep 5
done



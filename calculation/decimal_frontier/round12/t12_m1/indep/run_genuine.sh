#!/bin/bash
cd ~/p196_run/r12a
for spec in "0 12 12 1" "7 20 12 2" "22 13 6 3" "13 10 3 4"; do set -- $spec
 /usr/bin/time -l ~/p196_run/venv/bin/python ~/p196_run/r12a/indep_defect.py genuine --V $1 --Lj $2 --R $3 --seed $4 > indep/genuine_V$1_L$2_R$3_s$4.log 2>&1
done

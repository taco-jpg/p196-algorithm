#!/bin/bash
cd ~/p196_run/r12a
for spec in "5 12 4 11" "8 7 6 12" "21 15 8 13"; do set -- $spec
 /usr/bin/time -l ~/p196_run/venv/bin/python ~/p196_run/r12a/indep_defect.py cgenuine --V $1 --Lj $2 --R $3 --seed $4 --solver cadical195 > indep/cgenuine_V$1_L$2_R$3_s$4.log 2>&1
done

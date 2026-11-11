#!/bin/bash
cd ~/p196_run/r13a
for spec in "cadical195 1" "kissat404 2"; do set -- $spec
  nice -n 10 ~/p196_run/venv/bin/python bandjob.py L --clock 1000 --V 9,18,9,0 --T 32 --Tprime 16 --R 12 --all --timeout 600 --solver $1 --enc $2 2>&1 | grep BANDRESULT | cut -c1-170 | tee -a logs/xchk_lr.log
done

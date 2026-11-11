#!/bin/bash
# r12e: deep pass on the T=53 survivors (4 workers, in the slots of the finished T=53 census)
cd ~/p196_run/r12e
until grep -q CENSUS_DONE logs/census_53.log 2>/dev/null; do sleep 60; done
python3 py/census_sum.py 53 > logs/census_sum_53b.txt 2>&1
bash run_deep.sh out/census/surv_T53.txt out/deep53 4 120000000 900 > logs/deep53.log 2>&1

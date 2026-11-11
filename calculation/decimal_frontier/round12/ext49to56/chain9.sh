#!/bin/bash
# r12e: when all 20 T=54 shards are done: summary, deep pass on the T=54 survivors (4 workers), kh2 sample check
cd ~/p196_run/r12e
until [ $(ls out/census/T54_s*.done 2>/dev/null | wc -l) -ge 20 ]; do sleep 30; done
python3 py/census_sum.py 54 > logs/census_sum_54.txt 2>&1
bash run_deep.sh out/census/surv_T54.txt out/deep54 4 120000000 900 > logs/deep54.log 2>&1
bash ctrl/kh2_sample.sh 54

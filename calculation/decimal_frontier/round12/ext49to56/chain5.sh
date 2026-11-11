#!/bin/bash
# r12e: kh2 sample checks for T=50..53 in the slot of the p47 khx3 confirmation run (after it ends and the summaries exist)
cd ~/p196_run/r12e
until [ -s out/confirm/p47_khx3.out ]; do sleep 30; done
until grep -q CENSUS_DONE logs/census_49_52.log; do sleep 30; done
sleep 60
for T in 50 51 52; do bash ctrl/kh2_sample.sh $T; done
until grep -q CENSUS_DONE logs/census_53.log 2>/dev/null; do sleep 60; done
python3 py/census_sum.py 53 > logs/census_sum_53.txt 2>&1
bash ctrl/kh2_sample.sh 53

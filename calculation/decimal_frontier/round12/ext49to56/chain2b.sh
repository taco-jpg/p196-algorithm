#!/bin/bash
# r12e (replaces chain2.sh): after census pass 1 T=49..52: summaries, census T=53 (5 jobs), deep pass on the T=49..52 survivors
# (3 workers).  Families queue later.  Worker count <= 12 (3 Task A/confirm + 1 ancestry + 5 + 3).
cd ~/p196_run/r12e
until grep -q CENSUS_DONE logs/census_49_52.log; do sleep 20; done
python3 py/census_sum.py 49 50 51 52 > logs/census_sum_49_52.txt 2>&1
cat out/census/surv_T49.txt out/census/surv_T50.txt out/census/surv_T51.txt out/census/surv_T52.txt > out/census/surv_49_52.txt
echo "$(date -u +%FT%TZ) chain2b: starting census 53 (5 jobs) and deep pass (3 workers)" >> logs/chain2.log
( nohup bash run_census.sh "53" 12 5 > logs/census_53.log 2>&1 < /dev/null & )
( nohup bash run_deep.sh out/census/surv_49_52.txt out/deep1 3 120000000 900 > logs/deep1.log 2>&1 < /dev/null & )

#!/bin/bash
# r12e: after the deep1 driver ends, rerun run_deep.sh on the same list (it only computes words without an output file)
cd ~/p196_run/r12e
while pgrep -f "run_deep.sh out/census/surv_49_52.txt" > /dev/null; do sleep 15; done
bash run_deep.sh out/census/surv_49_52.txt out/deep1 3 120000000 900 > logs/deep1b.log 2>&1

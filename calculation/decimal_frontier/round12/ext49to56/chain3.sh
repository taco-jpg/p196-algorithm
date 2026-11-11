#!/bin/bash
# r12e: wait for the p34_K2000 ancestry job, stop the old queue (its p21sq/p47 jobs are superseded), start run_anc2.sh
cd ~/p196_run/r12e
until grep -q "p34_K2000 done" out/anc/done.log 2>/dev/null; do sleep 10; done
pkill -f "bash chain1.sh"; pkill -f "bash run_anc.sh"; sleep 1; pkill -f "khxt_a 10 -g 001001010101001010101"
bash run_anc2.sh

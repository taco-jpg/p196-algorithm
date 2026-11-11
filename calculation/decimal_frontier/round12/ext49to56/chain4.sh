#!/bin/bash
# r12e: (01)^20, (01)^24 family runs in the slot freed by the T=53 census (after it finishes)
cd ~/p196_run/r12e
until grep -q CENSUS_DONE logs/census_53.log 2>/dev/null; do sleep 60; done
bash run_fam.sh 1500 1500 > logs/fam.log 2>&1

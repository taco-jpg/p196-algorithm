#!/bin/bash
# r12e: when census T=53 is done, a second T=54 driver joins with 2 jobs (claim locks prevent duplicate shards)
cd ~/p196_run/r12e
until grep -q CENSUS_DONE logs/census_53.log 2>/dev/null; do sleep 30; done
bash run_census2.sh "54" 20 2 > logs/census_54b.log 2>&1

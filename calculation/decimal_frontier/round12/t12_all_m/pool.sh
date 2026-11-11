#!/bin/bash
# r12f pool: JOBS file lines "enc mode U R m solver outdir" (see run1.sh); P parallel workers.
P=${P:-3}; JOBS=$1
cd ~/p196_run/r12f
echo "pool start $(date) P=$P $JOBS" >> logs/pools.log
cat $JOBS | xargs -P $P -L 1 ~/p196_run/r12f/run1.sh
echo "pool done $(date) $JOBS" >> logs/pools.log

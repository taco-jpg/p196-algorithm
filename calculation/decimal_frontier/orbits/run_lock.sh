#!/bin/bash
# run_lock.sh OUT T "bases" "seeds"
OUT=$1; T=$2
: > $OUT
for b in $3; do for s in $4; do ./cpp/lock $b 20 $s $T 8 12 >> $OUT; done; done

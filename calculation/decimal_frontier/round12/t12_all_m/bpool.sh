#!/bin/bash
# r12f2: run a job list (one "mode U R n flag solver" per line) with P parallel workers
P=${P:-6}; L=$1
echo "$(date -u +%FT%TZ) bpool start P=$P $L" >> ~/p196_run/r12f/bres/bpool.log
grep -v '^#' $L | xargs -P $P -L 1 ~/p196_run/r12f/brun.sh
echo "$(date -u +%FT%TZ) bpool done $L" >> ~/p196_run/r12f/bres/bpool.log

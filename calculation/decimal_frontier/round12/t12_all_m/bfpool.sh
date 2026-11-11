#!/bin/bash
P=${P:-6}; L=$1
echo "$(date -u +%FT%TZ) bfpool start P=$P $L" >> ~/p196_run/r12f/bres/bpool.log
grep -v '^#' $L | xargs -P $P -L 1 ~/p196_run/r12f/bfrun.sh
echo "$(date -u +%FT%TZ) bfpool done $L" >> ~/p196_run/r12f/bres/bpool.log

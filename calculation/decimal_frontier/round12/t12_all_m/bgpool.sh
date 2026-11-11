#!/bin/bash
P=${P:-5}; L=$1
echo "$(date -u +%FT%TZ) bgpool start P=$P $L" >> ~/p196_run/r12f/bres/bpool.log
grep -v '^#' $L | xargs -P $P -L 1 ~/p196_run/r12f/bgrun.sh
echo "$(date -u +%FT%TZ) bgpool done $L" >> ~/p196_run/r12f/bres/bpool.log

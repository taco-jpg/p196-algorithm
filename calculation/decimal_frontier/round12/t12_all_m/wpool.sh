#!/bin/bash
P=${P:-4}; L=$1
echo "$(date -u +%FT%TZ) wpool start P=$P $L" >> ~/p196_run/r12f/bres/bpool.log
grep -v '^#' $L | xargs -P $P -L 1 ~/p196_run/r12f/wrun.sh
echo "$(date -u +%FT%TZ) wpool done $L" >> ~/p196_run/r12f/bres/bpool.log

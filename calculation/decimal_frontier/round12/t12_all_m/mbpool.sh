#!/bin/bash
P=${P:-6}; L=$1
echo "$(date -u +%FT%TZ) mbpool start P=$P $L" >> ~/p196_run/r12f/bres/bpool.log
grep -v '^#' $L | xargs -P $P -L 1 ~/p196_run/r12f/mbrun.sh
echo "$(date -u +%FT%TZ) mbpool done $L" >> ~/p196_run/r12f/bres/bpool.log

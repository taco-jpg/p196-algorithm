#!/bin/bash
# usage: censusU.sh b pmin pmax out per_p_timeout [extra args to bwdcensus]
cd /home/claude/research/w3_formats/code
B=$1; PMIN=$2; PMAX=$3; OUT=$4; TO=$5; shift 5
echo "start $(date -u)" > $OUT
for p in $(seq $PMIN $PMAX); do
  echo "### b=$B p=$p $(date -u)" >> $OUT
  timeout $TO ./bwdcensus $B $p $p "$@" 2>>$OUT.err | cut -c1-1500 >> $OUT
  echo "rc=${PIPESTATUS[0]} $(date -u)" >> $OUT
done
echo "end $(date -u)" >> $OUT

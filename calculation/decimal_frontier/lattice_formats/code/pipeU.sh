#!/bin/bash
# usage: pipeU.sh out pmin pmax per_p_timeout [bwdcensus args...]   (base 10, stage 1: small caps)
cd /home/claude/research/w3_formats/code
OUT=$1; PMIN=$2; PMAX=$3; TO=$4; shift 4
echo "start $(date -u)" > $OUT
for p in $(seq $PMIN $PMAX); do
  echo "### p=$p $(date -u)" >> $OUT
  timeout $TO ./bwdcensus 10 $p $p -und ../out/und_b10_hi.txt "$@" 2>>$OUT.err | cut -c1-1800 >> $OUT
  echo "rc=${PIPESTATUS[0]} $(date -u)" >> $OUT
done
echo "end $(date -u)" >> $OUT

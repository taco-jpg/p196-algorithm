#!/bin/bash
# usage: census5.sh b pmin pmax out cap per_p_timeout
cd /home/claude/research/w3_formats/code
OUT=$4
echo "start $(date -u)" > $OUT
for p in $(seq $2 $3); do
  echo "### b=$1 p=$p $(date -u)" >> $OUT
  timeout $6 ./bauto5 $1 $p $p -cap $5 -maxscc 4 2>>$OUT.err | cut -c1-1800 >> $OUT
  echo "rc=${PIPESTATUS[0]} $(date -u)" >> $OUT
done
echo "end $(date -u)" >> $OUT

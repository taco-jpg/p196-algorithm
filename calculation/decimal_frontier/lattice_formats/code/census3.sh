#!/bin/bash
# usage: census3.sh pmin pmax outfile
cd /home/claude/research/w3_formats/code
OUT=$3
echo "start $(date -u)" > $OUT
for p in $(seq $1 $2); do
  echo "### p=$p $(date -u)" >> $OUT
  timeout 270 ./bauto3 10 $p $p -cap 3000000 -maxscc 3 2>>$OUT.err | grep -v "nontrivial_sccs=0" | cut -c1-300 >> $OUT
  echo "rc=${PIPESTATUS[0]} $(date -u)" >> $OUT
done

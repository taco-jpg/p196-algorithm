#!/bin/bash
cd /home/claude/research/w3_formats/code
OUT=../out/census2_b10.txt
echo "start $(date -u)" > $OUT
for p in 9 10 11 12; do
  echo "### p=$p" >> $OUT
  timeout 380 ./bauto3 10 $p $p -cap 3000000 -maxscc 4 2>/dev/null | grep -v "nontrivial_sccs=0" | cut -c1-400 >> $OUT
  echo "rc=$? $(date -u)" >> $OUT
done

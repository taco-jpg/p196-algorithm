#!/bin/bash
cd /home/claude/research/w3_formats/code
OUT=../out/uSD2_diff_sym_b10.txt
echo "start $(date -u)" > $OUT
for p in 18 20 22 24; do
  timeout 420 /tmp/claude-0/bddenv/bin/python diff_sym.py 10 $p $p 30 >> $OUT 2>&1
done
echo "end $(date -u)" >> $OUT

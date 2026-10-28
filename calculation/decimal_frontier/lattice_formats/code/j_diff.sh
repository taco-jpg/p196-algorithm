#!/bin/bash
cd /home/claude/research/w3_formats/code
OUT=../out/uSD_diff_sym.txt
echo "start $(date -u)" > $OUT
for spec in "4 2 12" "13 2 10" "9 2 10" "5 2 10" "6 2 10" "7 2 10" "8 2 10" "10 2 12" "11 2 9" "12 2 9" "3 2 12"; do
  timeout 400 /tmp/claude-0/bddenv/bin/python diff_sym.py $spec >> $OUT 2>&1
done
echo "end $(date -u)" >> $OUT

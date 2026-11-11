#!/bin/bash
cd ~/p196_run/mchk14
PY=~/p196_run/venv/bin/python
L=~/p196_run/mchk13b/lat/rec0.txt
clang++ -O2 -std=c++17 -o mc14p mc14p.cpp -lpthread 2>&1 | head -n 5
echo "== accepting phases, rec0 orbit 0"
ACCPH=1 perl -e 'alarm 900; exec @ARGV' ./mc14p runscc $L 0 17 4 0 2>&1 | grep -E "ACCPH|^K (12|14|16|17) |FATAL" | cut -c1-300
echo "== forbidden values, plain python, rec0 orbit 0 (expected K(v) = 11,12,7,7,8,5,4,5,5,7,5,5,3,5,8,7,7,11,10 for v = 0..18)"
for v in 12 6 5 7 8 10 11 13 9; do
  r=$(FORB=$v perl -e 'alarm 800; exec @ARGV' $PY pyforb.py $L 8 0 2>&1 | grep -E "^EMPTY|Traceback" | head -n 1)
  echo "v=$v: $r"
done
echo "== band closures, plain python (r14b: 1,1,17,17 -> 3,3,2,1; 0,9,18,9 -> 1,3,3,2; 5,5,13,13 -> 3,3,2,1; 6,9,12,9 -> 1,3,3,2; 1,7,17,11 -> 2,2,2,2; 1,11,17,7 live)"
perl -e 'alarm 1500; exec @ARGV' $PY bandchk.py 3 1,1,17,17 0,9,18,9 5,5,13,13 6,9,12,9 1,7,17,11 1,11,17,7 2>&1 | cut -c1-220
echo done

#!/bin/bash
# round 9: chain 1 backward cones, Agent6 period-8 port streams (all alignments; window filter drops the dead ones), clock (0001)^(P/4), w=12 bitset windows
cd ~/p196_run/r9; BD=./backdisk9
run() { name=$1; shift; rm -rf wd_$name; ( time WIN=12 WINFILE=win/w12 ROT=1 THREADS=16 nice -n 10 $BD "$@" ) > logs/$name.log 2>&1; grep -E "RESULT|of .* target keys|real" logs/$name.log | sed "s/^/$name: /" >> logs/cones.log; rm -rf wd_$name; }
echo "== cones $(date -u)" >> logs/cones.log
run C1_P88 10 88 0001 wd_C1_P88 2000000000 0.20 $(python3 specs.py 88)
run C1_P72 10 72 0001 wd_C1_P72 2000000000 0.20 $(python3 specs.py 72)
echo "== cones done $(date -u)" >> logs/cones.log

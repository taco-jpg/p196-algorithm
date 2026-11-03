#!/bin/bash
cd ~/p196_run/r9; BD=./backdisk9
while pgrep -f cones.sh >/dev/null; do sleep 30; done
run() { name=$1; shift; rm -rf wd_$name; ( time WIN=12 WINFILE=win/w12 ROT=1 THREADS=16 nice -n 10 $BD "$@" ) > logs/$name.log 2>&1; grep -E "RESULT|of .* target keys|real" logs/$name.log | sed "s/^/$name: /" >> logs/cones.log; rm -rf wd_$name; }
echo "== cones2 $(date -u)" >> logs/cones.log
run C1_P96 10 96 0001 wd_C1_P96 1000000000 0.20 $(python3 specs.py 96)
echo "== cones2 done $(date -u)" >> logs/cones.log

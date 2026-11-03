#!/bin/bash
cd ~/p196_run/r9; BD=./backdisk9; n12=101101010010
run() { w=$1; name=$2; shift 2; rm -rf wd_$name; ( time WIN=$w WINFILE=win/w$w ROT=1 THREADS=16 nice -n 10 $BD "$@" ) > logs/ctrl_$name.log 2>&1; grep -E "RESULT|of .* target keys|real" logs/ctrl_$name.log | sed "s/^/$name: /" >> logs/ctrl.log; rm -rf wd_$name; }
echo "== ctrl2 $(date -u)" >> logs/ctrl.log
run 12 n12_T48_w12 10 48 0001 wd_n12_T48_w12 3000000000 0.20 stream:$(printf "$n12%.0s" 1 2 3 4)
run 10 p8_T40_w10 10 40 0001 wd_p8_T40_w10 5000000000 0.20 $(python3 specs.py 40)
run 12 p8_T40_w12 10 40 0001 wd_p8_T40_w12 5000000000 0.20 $(python3 specs.py 40)
run 12 p8_T48_w12 10 48 0001 wd_p8_T48_w12 5000000000 0.20 $(python3 specs.py 48)
echo "== ctrl2 done $(date -u)" >> logs/ctrl.log

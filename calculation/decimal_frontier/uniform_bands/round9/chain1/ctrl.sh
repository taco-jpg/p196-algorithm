#!/bin/bash
# round 9 controls for backdisk9 (128-bit streams, bitset windows): N12 positive control (expected height 53) and regressions vs round 7
# (M1 P=24 cone 7,142 states, P=40 cone 11,320,224 states, both w=10)
cd ~/p196_run/r9; BD=./backdisk9; n12=101101010010
run() { w=$1; name=$2; shift 2; rm -rf wd_$name; ( time WIN=$w WINFILE=win/w$w ROT=1 THREADS=16 nice -n 10 $BD "$@" ) > logs/ctrl_$name.log 2>&1; grep -E "RESULT|of .* target keys|real" logs/ctrl_$name.log | sed "s/^/$name: /" >> logs/ctrl.log; rm -rf wd_$name; }
echo "== ctrl (bitset windows) $(date -u)" >> logs/ctrl.log
run 10 n12_T24_w10 10 24 0001 wd_n12_T24_w10 5000000000 0.20 stream:${n12}${n12}
run 10 p8_T24_w10 10 24 0001 wd_p8_T24_w10 5000000000 0.20 $(python3 specs.py 24)
run 12 n12_T24_w12 10 24 0001 wd_n12_T24_w12 5000000000 0.20 stream:${n12}${n12}
run 12 n12_T72_w12 10 72 0001 wd_n12_T72_w12 5000000000 0.20 stream:$(printf "$n12%.0s" 1 2 3 4 5 6)
run 12 n12_T96_w12 10 96 0001 wd_n12_T96_w12 5000000000 0.20 stream:$(printf "$n12%.0s" 1 2 3 4 5 6 7 8)
run 10 p8_T40_w10 10 40 0001 wd_p8_T40_w10 5000000000 0.20 $(python3 specs.py 40)
run 12 p8_T40_w12 10 40 0001 wd_p8_T40_w12 5000000000 0.20 $(python3 specs.py 40)
run 12 p8_T48_w12 10 48 0001 wd_p8_T48_w12 5000000000 0.20 $(python3 specs.py 48)
echo "== ctrl done $(date -u)" >> logs/ctrl.log

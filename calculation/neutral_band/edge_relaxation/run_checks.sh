#!/bin/sh
# Neutral band, all known decimal exteriors: no centre and no converter can absorb their carry streams (all widths, all periods).
# About 15 minutes, < 1 GB. Needs g++ and python-sat. Expected key lines are in README.md.
set -e
cd "$(dirname "$0")"
K6SRC=../../decimal_frontier/lattice_kinks/edge_relaxation/kink6.cpp
g++ -O2 -o up4 up4.cpp; g++ -O2 -o kink6 $K6SRC; g++ -O2 -o wirebudget wirebudget.cpp
echo "== 1. exteriors and their streams (upward transfer construction, complete when the interface set repeats)"
./up4 10 11 00001110001 ANY 200 | grep -E "NEW STREAM|RESULT"
./up4 10 12 0001 ANY 200 | grep -E "NEW STREAM|RESULT"
python3 wiretbl.py
echo "== 2. positive control: the known clock-0001 centre loop is found as an exact centre cycle (K>=4)"
./kink6 wire_ctrl.tbl 3 full c3.bin 2>/dev/null
for K in 4 5; do ./kink6 wire_ctrl.tbl $K incr c$((K-1)).bin c$K.bin 2>/dev/null; done
echo "== 3. centres moving with h (all periods): accepting states die at K=6, no exact centre of depth <= 6"
for W in wire_p11 wire_p12_0 wire_p12_1 wire_p12_2; do
  ./kink6 $W.tbl 3 full ${W}_3.bin 2>/dev/null
  for K in 4 5 6; do ./kink6 $W.tbl $K incr ${W}_$((K-1)).bin ${W}_$K.bin 2>/dev/null; done
done
echo "== 4. independent Python reference (klib rule, own SCC and exact check)"
python3 wirelat.py 00001110001 00111010011 wire_p11_3.bin 3 6
python3 wirelat.py 000100010001 101101010010 wire_p12_0_3.bin 3 6
python3 wirelat.py 1000100010001000 1000100001110111 c3.bin 3 5
echo "== 5. any drift in [0, centre speed] (centres and converters), all periods: shift budget frame"
./wirebudget 1000100010001000 1000100001110111 1 8 3 full bc3.bin
for K in 4 5 6; do ./wirebudget 1000100010001000 1000100001110111 1 8 $K incr bc$((K-1)).bin bc$K.bin; done
./wirebudget 00001110001 00111010011 2 11 3 full b11_3.bin
for K in 4 5 6 7; do ./wirebudget 00001110001 00111010011 2 11 $K incr b11_$((K-1)).bin b11_$K.bin; done
i=0; for S in 101101010010 001010110101 010100101011; do
  ./wirebudget 000100010001 $S 1 8 3 full b12_${i}_3.bin
  for K in 4 5 6 7; do ./wirebudget 000100010001 $S 1 8 $K incr b12_${i}_$((K-1)).bin b12_${i}_$K.bin; done; i=$((i+1)); done
echo "== 6. separate SAT encoding, fixed period: drift needed to cap the p11 stream (centre drift 2 per 11 steps)"
python3 edgesatg.py 00001110001 00111010011 11 8 0 5 | grep SUMMARY
python3 edgesatg.py 00001110001 00111010011 22 12 0 8 | grep SUMMARY

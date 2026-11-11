#!/bin/bash
cd ~/p196_run/mchk13b || exit 1
mkdir -p logs
clang++ -O2 -std=c++17 -pthread mc13b.cpp -o mc13b 2> build.log; echo "build rc=$?"; cat build.log | head -30
~/p196_run/venv/bin/python mklat13.py lat 2>&1
for L in rec0 rec1 rec2; do ./mc13b selftest lat/$L.txt 13 300000 2>&1; done
for L in b9r0 b9r1; do for o in 0 1 2 3; do echo "== $L orbit $o"; ./mc13b run lat/$L.txt $o 12 4 1 2>&1 | grep -E "exact orbit|^# base|^K (1|2|3|4|5|6) |EMPTY" ; done; done
./mc13b orbits lat/rec0.txt
./mc13b orbits lat/rec2.txt

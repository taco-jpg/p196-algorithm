#!/bin/bash
cd ~/p196_run/mchk13b || exit 1
clang++ -O2 -std=c++17 -pthread mc13d.cpp -o mc13d2 2> build_d2.log; echo "build rc=$?"; head -20 build_d2.log
for L in p12m9 rec0 rec2 ; do ./mc13d2 lat/$L.txt 8 selftest 23 400000 2>&1 | cut -c1-150; done
~/p196_run/venv/bin/python pybudget.py lat/p12m9.txt 8 7 > logs/py_budget8_p12m9.log 2>&1 &
~/p196_run/venv/bin/python pybudget.py lat/p12m9.txt 8 7 zero > logs/py_zero_p12m9.log 2>&1 &
wait

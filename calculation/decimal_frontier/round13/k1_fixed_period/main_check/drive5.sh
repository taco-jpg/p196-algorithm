#!/bin/bash
cd ~/p196_run/mchk13b || exit 1
clang++ -O2 -std=c++17 -pthread mc13d.cpp -o mc13d 2> build_d.log; echo "build rc=$?"; head -20 build_d.log
echo "control: base 9 (centres exist, budget 5): must NOT die"
./mc13d lat/b9r0.txt 5 8 4 2>&1 | cut -c1-110
echo "p12m9, budget 8, drift in [0,1/8]"
./mc13d lat/p12m9.txt 8 30 8 2>&1 | tee logs/p12m9_budget8.log | cut -c1-110
echo "p12m9, drift 0 only"
./mc13d lat/p12m9.txt 8 30 8 zero 2>&1 | tee logs/p12m9_zero.log | cut -c1-110

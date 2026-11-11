#!/bin/bash
cd ~/p196_run/mchk13a || exit 1
mkdir -p logs
clang++ -O2 -std=c++17 -pthread bandcount.cpp -o bandcount 2> build.log; echo "build rc=$?"; head -20 build.log
for G in 1000 10 00001110001; do
  for s in 1 2 3 4 5 6 7; do
    ./bandcount $G $s 8 list > logs/bc_${G}_s$s.txt 2>&1; head -1 logs/bc_${G}_s$s.txt
  done
done
./bandcount 1000 8 8 list > logs/bc_1000_s8.txt 2>&1; head -1 logs/bc_1000_s8.txt
./bandcount 10 8 8 list > logs/bc_10_s8.txt 2>&1; head -1 logs/bc_10_s8.txt
./bandcount 00001110001 8 8 list > logs/bc_00001110001_s8.txt 2>&1; head -1 logs/bc_00001110001_s8.txt

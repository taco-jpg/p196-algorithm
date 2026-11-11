#!/bin/bash
cd ~/p196_run/mchk13c || exit 1
mkdir -p logs
clang++ -O2 -std=c++17 -pthread mc13e.cpp -o mc13e 2> build.log; echo "build rc=$?"; head -30 build.log
./mc13e selftest 7 200000
for pair in "0001 4" "01 8" "0001 12" "00001110001 11" "00010010111 11" "00100101010101 14" "001010101 9"; do set -- $pair; ./mc13e if $1 $2; done
./mc13e root 00010010111 11 60 | tail -3
./mc13e root 001010101 9 40 | tail -1
./mc13e root 00100101010101 14 40 | tail -1
echo "-- control: N12 at d=4, L=12"
./mc13e towers 0001 4 12 8 3000000 30 400 | tail -6 | cut -c1-200
echo "-- control: p11 L=22"
./mc13e towers 00001110001 11 22 8 30000000 120 2000 | tail -5 | cut -c1-200
echo "-- control: (01), d=8, L=16"
./mc13e towers 01 8 16 8 30000000 300 2000 > logs/L16.out 2>&1; tail -5 logs/L16.out | cut -c1-300
echo "-- word (00010010111)^5, L=55"
./mc13e towers 00010010111 11 55 8 40000000 600 3000 > logs/T55.out 2>&1; tail -6 logs/T55.out | cut -c1-400

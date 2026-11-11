#!/bin/bash
cd ~/p196_run/mchk13c || exit 1
clang++ -O2 -std=c++17 -pthread mc13e.cpp -o mc13e2 2> build2.log; echo "build rc=$?"; head build2.log
./mc13e2 towers 00010010111 11 55 1 900000000 86400 3000 0 665992 > logs/T55_tower665992.out 2>&1
tail -3 logs/T55_tower665992.out | cut -c1-200

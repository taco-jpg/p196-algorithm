#!/bin/bash
cd ~/p196_run/mchk13b || exit 1
clang++ -O2 -std=c++17 -pthread mc13c.cpp -o mc13c 2> build_c.log; echo "build rc=$?"; head -20 build_c.log
# control: base 9 must keep its genuine centres, all periods
for L in b9r0 b9r1; do for o in 0 2; do echo "== $L orbit $o"; ./mc13c runscc lat/$L.txt $o 9 4 1 2>&1 | grep -E "PERIODIC|^K " | cut -c1-120; done; done
for o in 0 1 2; do
  echo "== p12m9 orbit $o (all periods)"
  ./mc13c runscc lat/p12m9.txt $o 40 8 1 2>&1 | tee logs/p12m9_scc_o$o.log | cut -c1-120
done

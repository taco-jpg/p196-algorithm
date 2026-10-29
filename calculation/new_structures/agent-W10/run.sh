#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python3 cyclic_clock.py
CXX=g++
"$CXX" -O3 -std=c++17 -Wall -Wextra period4_replay.cpp -o /tmp/w10_period4_replay
"$CXX" -O3 -std=c++17 -Wall -Wextra gmp_replay.cpp -lgmpxx -lgmp -o /tmp/w10_gmp_replay
/tmp/w10_period4_replay 8000 20000 64 > /tmp/w10_digit.tsv
/tmp/w10_gmp_replay 8000 20000 > /tmp/w10_gmp.tsv
awk -F'\t' 'NR>1{print $1,$2,$3,$7}' /tmp/w10_digit.tsv > /tmp/w10_digit.columns
awk -F'\t' 'NR>1{print $1,$2,$3,$4}' /tmp/w10_gmp.tsv > /tmp/w10_gmp.columns
diff -u /tmp/w10_digit.columns /tmp/w10_gmp.columns
diff -u checkpoints.tsv /tmp/w10_digit.tsv
echo 'ALL W10 CHECKS PASSED'

#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
work=$(mktemp -d); trap 'rm -rf "$work"' EXIT
g++ -O3 -std=c++17 bulk20k_digits.cpp -o "$work/base"
g++ -O3 -std=c++17 bulk20k_pump_q.cpp -o "$work/pump"
"$work/base" 15000 20000 100 > "$work/full.csv" 2> "$work/base.log"
python3 allq_matrix.py "$work/full.csv"
"$work/pump" 15000 20000 1 > "$work/pump.log"
grep 'PUMP_ALL_STEPS_PASS k=15000 T=20000 q=1 min_odd=2' "$work/pump.log"
"$work/pump" 15000 500 2 > "$work/pump2.log"
grep 'PUMP_ALL_STEPS_PASS k=15000 T=500 q=2 min_odd=2' "$work/pump2.log"
echo 'N19_UNIVERSAL_FINITE_HORIZON_FAMILY_CHECKS_PASSED'

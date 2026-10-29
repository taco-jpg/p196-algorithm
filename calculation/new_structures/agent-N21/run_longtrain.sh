#!/bin/sh
# Reproduce N21 mixed-phase 20,000-step coefficient and independent GMP arithmetic.
set -eu
cd "$(dirname "$0")"
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT HUP INT TERM
c++ -O3 -std=c++17 longtrain.cpp -lgmpxx -lgmp -o "$tmp/longtrain"
"$tmp/longtrain" 10000 100 1000 3500 1 > "$tmp/positive"
grep -q '^LONG_TRAIN_PASS 100 steps' "$tmp/positive"
if "$tmp/longtrain" 10000 1 1000 3500 1 1 > "$tmp/negative" 2>&1; then
    echo 'Negative corrupted-GMP-seed control failed' >&2; exit 1
fi
grep -q '^PAIR_MISMATCH step=0 seed=3' "$tmp/negative"
python3 check_longtrain.py
if [ "$#" -gt 0 ] && [ "$1" = '--quick' ]; then
    echo 'QUICK_CONTROLS_PASS'; exit 0
fi
"$tmp/longtrain" 70000 20000 8000 22000 1 > "$tmp/full"
diff -u trace_longtrain.txt "$tmp/full"
echo 'REPRODUCTION_20000_PASS'

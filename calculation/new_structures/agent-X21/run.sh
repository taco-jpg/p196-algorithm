#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
c++ -std=c++17 -O3 "$HERE/gap_fast.cpp" -o "$TMP/gap_fast"
c++ -std=c++17 -O3 "$HERE/check_gmp.cpp" -lgmpxx -lgmp -o "$TMP/check_gmp"
for seed in 196 879 1997; do
    "$TMP/gap_fast" "$seed" 20000 128 "$TMP/seed.csv" 2>"$TMP/fast.stats"
    python3 "$HERE/verify_radius.py" "$seed" "$TMP/seed.csv" "$TMP/checkpoints.tsv"
    "$TMP/check_gmp" "$seed" > "$TMP/gmp.stats"
    case "$seed" in
      196) expected='max_def=21 max_def_time=12877 min_half_length_growth=21 min_gap_exp_growth=8' ;;
      879) expected='max_def=22 max_def_time=6353 min_half_length_growth=22 min_gap_exp_growth=5' ;;
      1997) expected='max_def=21 max_def_time=3100 min_half_length_growth=21 min_gap_exp_growth=10' ;;
    esac
    grep -F "SUMMARY palindrome=0 bad_stride=0 $expected" "$TMP/gmp.stats"
done
echo "INDEPENDENT-GMP PASS; ALL X21 CHECKS PASSED"
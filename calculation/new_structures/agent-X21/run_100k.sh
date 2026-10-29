#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
c++ -O3 -std=c++17 "$HERE/gap_fast.cpp" -o "$TMP/fast"
c++ -O3 -std=c++17 "$HERE/independent_string_100k.cpp" -lgmpxx -lgmp -o "$TMP/independent"
"$TMP/fast" 196 100000 128 "$TMP/orbit.csv" 2> "$TMP/fast.log"
python3 "$HERE/adaptive_radius_100k.py" "$TMP/orbit.csv"
"$TMP/independent" "$TMP/orbit.csv"
echo 'ALL X21 ADAPTIVE 100K CHECKS PASSED'
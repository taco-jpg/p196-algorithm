#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
"${CXX:-g++}" -O3 -std=c++17 "$HERE/master_gap_sweep.cpp" -o "$TMP/master"
"${CXX:-g++}" -O3 -std=c++17 "$HERE/master_pair_emission.cpp" -o "$TMP/emission"
"$TMP/master" 256 52000 100 > "$TMP/masters.csv"
"$TMP/emission" > "$TMP/pairs.csv"
python3 "$HERE/verify_pair_emission.py" "$TMP/pairs.csv" "$TMP/masters.csv"

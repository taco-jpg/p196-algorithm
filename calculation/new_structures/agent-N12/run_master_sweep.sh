#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
"${CXX:-g++}" -O3 -std=c++17 "$HERE/master_gap_sweep.cpp" -o "$TMP/master"
"$TMP/master" 256 52000 100 > "$TMP/sweep.csv"
python3 "$HERE/independent_master_check.py" "$TMP/sweep.csv"

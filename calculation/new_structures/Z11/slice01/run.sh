#!/usr/bin/env bash
set -euo pipefail
HERE="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
BIN="/tmp/z11_slice01_bitparallel"
g++ -O3 -march=native -mavx2 -std=c++17 -fopenmp "$HERE/bitparallel_census.cpp" -o "$BIN"
"$BIN" --selftest
OMP_NUM_THREADS=5 "$BIN"

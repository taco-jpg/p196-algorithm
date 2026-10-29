#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
BIN="/tmp/z07-j5-search"
g++ -O3 -march=native -std=c++17 -Wall -Wextra -pedantic "$ROOT/calculation/new_structures/Z07/search.cpp" -o "$BIN"
"$BIN" 0 2476099 7
"$BIN" 0 2476099 19
python3 "$ROOT/calculation/new_structures/Z07/independent_bigint.py"
for U in 6,9,12 9,16,2; do
  for J in 0,0,0,0,0 18,18,18,18,18 1,2,3,4,5 5,18,4,8,1 18,0,9,12,3; do
    python3 "$ROOT/tools/parametric_verify_r30.py" --lattice "$ROOT/calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt" --J "$J" --U "$U" --C 0,0,0 --qmin 256 --kmin 256 --only-symbolic
  done
done

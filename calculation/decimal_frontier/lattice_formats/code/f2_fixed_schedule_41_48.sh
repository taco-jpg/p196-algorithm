#!/usr/bin/env bash
# Exact fixed-schedule exterior check used by Agent335F2FixedSchedule4148.
# Usage: ./f2_fixed_schedule_41_48.sh [output-directory]
set -euo pipefail

root=$(cd "$(dirname "$0")/../../../.." && pwd)
out=${1:-"$root/../agent335-f2-41-48"}
mkdir -p "$out"
cxx=${CXX:-g++}
"$cxx" -O3 -std=c++17 "$root/calculation/decimal_frontier/lattice_formats/code/bauto3.cpp" -o "$out/bauto3"

# Positive controls for the same p=10 engine and state cap.
"$out/bauto3" 9 10 10 -g 1100011000 -cap 3000000 -maxscc 8 > "$out/control-b9.txt"
"$out/bauto3" 13 10 10 -g 1010010000 -cap 3000000 -maxscc 8 > "$out/control-b13.txt"

for b in $(seq 41 48); do
  for g in 1100011000 1010010000; do
    "$out/bauto3" "$b" 10 10 -g "$g" -cap 3000000 -maxscc 8
  done
done | tee "$out/results.txt"

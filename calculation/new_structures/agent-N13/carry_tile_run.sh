#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
D="$(mktemp -d)"
trap 'rm -rf "$D"' EXIT
c++ -std=c++17 -O3 -Wall -Wextra carry_tile.cpp -o "$D/carry_tile"
"$D/carry_tile" 20000 "$D/cpp.csv" | tee "$D/out.txt"
grep -Fqx 'CARRY_EIGHT_GATES_88_PHASES high_A_B_differ_phases=49 comparisons=19001 mismatch_counts=0,0,0,0,0,0,0,0,' "$D/out.txt"
python3 carry_tile_independent.py "$D/python.csv"
diff -u "$D/cpp.csv" "$D/python.csv"
diff -u carry88.csv "$D/cpp.csv"
echo 'AGENT_N13_88_PHASE_CARRY_TILE_REPLAY_PASS'

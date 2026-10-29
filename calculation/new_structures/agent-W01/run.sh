#!/usr/bin/env bash
# Reproduce four 20,000-step true decimal orbits with two independent engines.
set -euo pipefail
cd "$(dirname "$0")"
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT
cxx=${CXX:-g++}
"$cxx" -std=c++17 -O3 -Wall -Wextra w01_collision.cpp -o "$work/collision"
"$cxx" -std=c++17 -O3 -Wall -Wextra w01_independent.cpp -lgmpxx -lgmp -o "$work/independent"
"$work/collision" 20000 > "$work/keyframes.csv" 2> "$work/digits.log"
for k in 0 1 2 3; do "$work/independent" 20000 "$k" > "$work/gmp${k}.log"; done
if "$work/independent" 100 3 wrong_phase > "$work/wrong.log" 2>&1; then
  echo 'ERROR: corrupted temporal phase was not rejected' >&2; exit 2
fi
python3 verify_results.py "$work"
echo 'AGENT_W01_TWO_PULSE_20K_PASS'

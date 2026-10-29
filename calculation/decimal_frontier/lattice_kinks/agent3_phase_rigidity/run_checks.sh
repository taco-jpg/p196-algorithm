#!/bin/sh
# From repository root: sh calculation/decimal_frontier/lattice_kinks/agent3_phase_rigidity/run_checks.sh
set -eu
cd "$(dirname "$0")"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT HUP INT TERM
c++ -std=c++17 -O2 -Wall -Wextra -pedantic primary.cpp -o "$TMP/phase_rigidity"
"$TMP/phase_rigidity"
python3 independent_check.py

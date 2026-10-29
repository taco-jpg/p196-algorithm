#!/usr/bin/env bash
# Independent signed two-ended residual-particle checks of all four decimal orbits.
set -euo pipefail
cd "$(dirname "$0")"
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT
cxx=${CXX:-g++}
"$cxx" -std=c++17 -O3 w01_residual_onset.cpp -o "$work/primary"
"$cxx" -std=c++17 -O3 w01_scatter_gmp.cpp -lgmpxx -lgmp -o "$work/gmp"
"$work/primary" 20000 > "$work/residual.csv" 2> "$work/primary.log"
"$work/gmp" 6000 > "$work/gmp.log"
if "$work/gmp" 3000 19 > "$work/negative.log" 2>&1; then
  echo 'Incorrect -19 spatial displacement unexpectedly accepted' >&2;exit 3
fi
python3 residual_verify.py "$work"
echo 'AGENT_W01_NONLINEAR_DAUGHTER_20K_PASS'

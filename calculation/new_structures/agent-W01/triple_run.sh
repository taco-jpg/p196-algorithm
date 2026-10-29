#!/usr/bin/env bash
# Complete W01 eight-orbit decimal three-body scattering and independent GMP controls.
set -euo pipefail
root=$(cd "$(dirname "$0")" && pwd)
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
c++ -std=c++17 -O3 "$root/w01_screened_corridor.cpp" -o "$tmp/corridor"
c++ -std=c++17 -O3 "$root/w01_scatter_phase.cpp" -o "$tmp/pair"
"$tmp/corridor" 20000 > "$tmp/triple.csv"
"$tmp/pair" 8000 20000 > "$tmp/pair.csv"
python3 "$root/triple_verify.py" "$tmp/triple.csv" "$tmp/pair.csv"
c++ -std=c++17 -O3 "$root/w01_triple_gmp.cpp" -o "$tmp/gmp" -lgmpxx -lgmp
"$tmp/gmp" 6000
printf '%s\n' AGENT_W01_TRIPLE_SCREENING_PASS

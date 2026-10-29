#!/usr/bin/env bash
# Full 32-orbit finite triple-packet emission-port and independent GMP controls.
set -euo pipefail
root=$(cd "$(dirname "$0")" && pwd)
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
c++ -std=c++17 -O3 "$root/w01_screened_corridor_z.cpp" -o "$tmp/triple"
c++ -std=c++17 -O3 "$root/w01_scatter_phase.cpp" -o "$tmp/pair"
for z in 9920 10000 10080 10160; do
  "$tmp/triple" 20000 12000 "$z" > "$tmp/triple_$z.csv"
done
"$tmp/pair" 8000 20000 > "$tmp/pair.csv"
python3 "$root/param_verify.py" \
  "$tmp/triple_9920.csv" "$tmp/triple_10000.csv" \
  "$tmp/triple_10080.csv" "$tmp/triple_10160.csv" "$tmp/pair.csv"
c++ -std=c++17 -O3 "$root/w01_triple_param_gmp.cpp" -o "$tmp/triple_gmp" -lgmpxx -lgmp
"$tmp/triple_gmp" 5600 10080
printf '%s\n' AGENT_W01_PARAMETERIZED_TRIPLE_PORT_PASS

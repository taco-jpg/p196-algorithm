#!/usr/bin/env bash
# Atomic self-contained control: 36 real decimal digit-vector orbits, plus 8 GMP controls.
set -euo pipefail
root=$(cd "$(dirname "$0")" && pwd)
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
c++ -std=c++17 -O3 "$root/w01_scatter_phase.cpp" -o "$tmp/phase"
for y in 7760 7840 7920 8000 8080 8160 8240 8320 8400; do
  "$tmp/phase" "$y" 20000 > "$tmp/phase_${y}.csv"
done
python3 "$root/phase_verify.py" \
  "$tmp/phase_7760.csv" "$tmp/phase_7840.csv" "$tmp/phase_7920.csv" \
  "$tmp/phase_8000.csv" "$tmp/phase_8080.csv" "$tmp/phase_8160.csv" \
  "$tmp/phase_8240.csv" "$tmp/phase_8320.csv" "$tmp/phase_8400.csv"
c++ -std=c++17 -O3 "$root/w01_phase_gmp.cpp" -o "$tmp/phase_gmp" -lgmpxx -lgmp
"$tmp/phase_gmp" 4500
printf '%s\n' 'AGENT_W01_PHASE_COVARIANCE_PASS'

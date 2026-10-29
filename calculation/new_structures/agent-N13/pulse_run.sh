#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
D="$(mktemp -d)"
trap 'rm -rf "$D"' EXIT
c++ -std=c++17 -O3 -Wall -Wextra pulse_collision.cpp -o "$D/pulse"
"$D/pulse" 5200 2000 100 6000 > "$D/dense.tsv" 2> "$D/cpp.log"
grep -Fqx 'FIRST_COLLISION t=3426 pulse_inner=4434 center_outer=4433' "$D/cpp.log"
grep -Fqx 'COLLISION=3426' "$D/cpp.log"
python3 pulse_check.py "$D/dense.tsv" "$D/keyframes.csv"
diff -u pulse_keyframes.csv "$D/keyframes.csv"
python3 pulse_independent.py "$D/dense.tsv"
echo 'AGENT_N13_BIPOLAR_PULSE_COLLISION_PASS'

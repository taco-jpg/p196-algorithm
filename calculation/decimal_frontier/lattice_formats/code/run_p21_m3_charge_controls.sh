#!/usr/bin/env bash
# Full optional external-engine controls, alongside mandatory self-contained ones.
set -euo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"
python3 "$DIR/p21_m3_charge_proof.py"
python3 "$DIR/check_p21_m3_charge.py"
tmp="$(mktemp -d)"; trap 'rm -rf "$tmp"' EXIT
g++ -std=c++17 -O3 "$DIR/bauto5.cpp" -o "$tmp/bauto5"
nice -n 10 "$tmp/bauto5" 9 10 10 -g 1100011000 -cap 3000000 -maxscc 8 >"$tmp/b9"
nice -n 10 "$tmp/bauto5" 13 10 10 -g 1010010000 -cap 3000000 -maxscc 8 >"$tmp/b13"
grep -q 'states=956310.*nontrivial_sccs=7' "$tmp/b9"
grep -q 'minc=4 depth=61' "$tmp/b9"
grep -q 'states=250302.*nontrivial_sccs=5' "$tmp/b13"
grep -q 'cyclen=1 depth=55' "$tmp/b13"
grep -q 'cyclen=1 depth=75' "$tmp/b13"
printf 'PASS mandatory base-9 and base-13 exterior controls\n'

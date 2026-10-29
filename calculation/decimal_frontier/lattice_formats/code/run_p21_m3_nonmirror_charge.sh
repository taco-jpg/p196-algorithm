#!/usr/bin/env bash
# Full reproducibility, two independent programs, exact data/controls, no external Python packages.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
ulimit -v 8388608
tmp="$(mktemp -d)"; trap 'rm -rf "$tmp"' EXIT
python3 "$ROOT/p21_m3_nonmirror_charge.py" "$tmp/new.txt"
diff -u "$ROOT/p21_m3_nonmirror_cycles.txt" "$tmp/new.txt"
python3 "$ROOT/check_p21_m3_nonmirror_charge.py" "$tmp/new.txt"
g++ -std=c++17 -O3 "$ROOT/bauto5.cpp" -o "$tmp/bauto5"
nice -n 10 "$tmp/bauto5" 9 10 10 -cap 3000000 -maxscc 8 -g 1100011000 >"$tmp/b9"
nice -n 10 "$tmp/bauto5" 13 10 10 -cap 3000000 -maxscc 8 -g 1010010000 >"$tmp/b13"
grep -q 'states=956310.*nontrivial_sccs=7' "$tmp/b9"
grep -q 'minc=4 depth=61' "$tmp/b9"
grep -q 'states=250302.*nontrivial_sccs=5' "$tmp/b13"
grep -q 'cyclen=1 depth=55' "$tmp/b13"
grep -q 'cyclen=1 depth=75' "$tmp/b13"
echo 'PASS all p21/m3 nonmirror cycles, independent checker and mandatory b9/b13 controls'

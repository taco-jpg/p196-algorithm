#!/usr/bin/env bash
# Exact full repro incl. control runs; one nice process at a time and <=8GB virtual memory.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
ulimit -v 8388608
tmp="$(mktemp -d)";trap 'rm -rf "$tmp"' EXIT
g++ -std=c++17 -O3 -Wall -Wextra "$ROOT/p21_m9_charge.cpp" -o "$tmp/m9charge"
nice -n 10 "$tmp/m9charge" "$tmp/reps.txt"
diff -u "$ROOT/p21_m9_charge_reps.txt" "$tmp/reps.txt"
python3 "$ROOT/check_p21_m9_charge.py" "$tmp/reps.txt"
g++ -std=c++17 -O3 "$ROOT/bauto5.cpp" -o "$tmp/bauto5"
nice -n 10 "$tmp/bauto5" 9 10 10 -cap 3000000 -maxscc 8 -g 1100011000 >"$tmp/b9.txt"
nice -n 10 "$tmp/bauto5" 13 10 10 -cap 3000000 -maxscc 8 -g 1010010000 >"$tmp/b13.txt"
grep -q 'states=956310.*nontrivial_sccs=7' "$tmp/b9.txt"
grep -q 'minc=4 depth=61' "$tmp/b9.txt"
grep -q 'states=250302.*nontrivial_sccs=5' "$tmp/b13.txt"
grep -q 'cyclen=1 depth=55' "$tmp/b13.txt"
grep -q 'cyclen=1 depth=75' "$tmp/b13.txt"
echo "PASS complete p21/m9 root-charge classification, independent checker, base9/base13 controls"

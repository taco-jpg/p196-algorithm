#!/usr/bin/env bash
# Complete reproducibility from the repo; no downloads or external Python packages.
set -euo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"
ulimit -v 8388608
python3 "$DIR/p21_f1_allbase.py"
python3 "$DIR/check_p21_f1_allbase.py"
tmp="$(mktemp -d)"; trap 'rm -rf "$tmp"' EXIT
g++ -std=c++17 -O3 "$DIR/bauto5.cpp" -o "$tmp/bauto5"
nice -n 10 "$tmp/bauto5" 9 10 10 -cap 3000000 -maxscc 8 -g 1100011000 >"$tmp/b9"
nice -n 10 "$tmp/bauto5" 13 10 10 -cap 3000000 -maxscc 8 -g 1010010000 >"$tmp/b13"
grep -q 'states=956310.*nontrivial_sccs=7' "$tmp/b9"
grep -q 'minc=4 depth=61' "$tmp/b9"
grep -q 'states=250302.*nontrivial_sccs=5' "$tmp/b13"
grep -q 'cyclen=1 depth=55' "$tmp/b13"
grep -q 'cyclen=1 depth=75' "$tmp/b13"
printf 'PASS p21 all-base first-column theorem + independent DP + b9/b13 controls\n'

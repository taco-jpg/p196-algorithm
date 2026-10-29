#!/usr/bin/env bash
# Complete independent reproduction from repository alone.
set -euo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"
ulimit -v 8388608
DATA="$DIR/p21_b110_two_column_witness.json"
python3 "$DIR/verify_p21_b110_affine.py" "$DATA"
python3 "$DIR/check_p21_b110_affine.py" "$DATA"
tmp="$(mktemp -d)"; trap 'rm -rf "$tmp"' EXIT
g++ -std=c++17 -O3 "$DIR/bauto5.cpp" -o "$tmp/bauto5"
nice -n 10 "$tmp/bauto5" 9 10 10 -cap 3000000 -maxscc 8 -g 1100011000 >"$tmp/b9"
nice -n 10 "$tmp/bauto5" 13 10 10 -cap 3000000 -maxscc 8 -g 1010010000 >"$tmp/b13"
grep -q 'states=956310.*nontrivial_sccs=7' "$tmp/b9"
grep -q 'minc=4 depth=61' "$tmp/b9"
grep -q 'states=250302.*nontrivial_sccs=5' "$tmp/b13"
grep -q 'cyclen=1 depth=55' "$tmp/b13"
grep -q 'cyclen=1 depth=75' "$tmp/b13"
echo 'PASS all-n two-column proof, independent divmod replay, b9/b13 positive controls'

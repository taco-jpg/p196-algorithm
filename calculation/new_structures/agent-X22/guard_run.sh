#!/bin/sh
# Independent ordinary-digit and GMP arithmetic, all 20,001 states.
set -eu
HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT HUP INT TERM
python3 "$HERE/seed.py" --tiles 600 --random-seed 20261028 > "$TMP/seed.txt"
python3 "$HERE/build_bphases.py" > "$TMP/bphases.txt"
g++ -O3 -std=c++17 "$HERE/guard_check.cpp" -o "$TMP/guard_array"
g++ -O3 -std=c++17 "$HERE/guard_gmp.cpp" -lgmpxx -lgmp -o "$TMP/guard_gmp"
"$TMP/guard_array" "$TMP/seed.txt" "$TMP/bphases.txt" > "$TMP/array.txt"
"$TMP/guard_gmp" "$TMP/seed.txt" "$TMP/bphases.txt" > "$TMP/gmp.txt"
cmp "$TMP/array.txt" "$TMP/gmp.txt"
cat "$TMP/array.txt"
sha256sum "$TMP/seed.txt"

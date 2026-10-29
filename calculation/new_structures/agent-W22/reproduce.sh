#!/bin/sh
set -eu
HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
python3 "$HERE/unit.py"
g++ -std=c++17 -O3 "$HERE/hinge_fast.cpp" -o "$TMP/digit"
g++ -std=c++17 -O3 "$HERE/hinge_gmp_fast.cpp" -lgmpxx -lgmp -o "$TMP/gmp"
(cd "$TMP" && ./digit 14000 8000 16000 20000 > digits.log && ./gmp 14000 8000 16000 20000 > gmp.log && cmp w22_final_digits.txt w22_gmp_final_digits.txt && sha256sum w22_final_digits.txt && tail -1 gmp.log && grep '^PASS ' digits.log)

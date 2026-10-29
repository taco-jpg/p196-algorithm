#!/bin/sh
set -eu
D=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
OUT=${1:-/tmp/agent3_six_witness}
mkdir -p "$OUT"
"${CXX:-c++}" -O3 -std=c++17 "$D/primary.cpp" -o "$OUT/primary"
"$OUT/primary" "$OUT" "$D"
"${CXX:-c++}" -O3 -std=c++17 "$D/independent_check.cpp" -o "$OUT/independent"
"$OUT/independent" "$OUT" "$D"

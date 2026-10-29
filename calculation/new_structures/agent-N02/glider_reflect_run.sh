#!/bin/sh
set -eu
HERE="$(CDPATH='' cd -- "$(dirname -- "$0")" && pwd)"
ROOT="$(CDPATH='' cd -- "$HERE/../../.." && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
python3 "$HERE/glider_reflect_independent.py" "$ROOT"
g++ -std=c++17 -O3 -Wall -Wextra "$HERE/glider_reflect_replay.cpp" -lgmpxx -lgmp -o "$TMP/reflect"
"$TMP/reflect" 1 512 > "$TMP/small.log"
grep -q 'REFLECT_PREFIX_BREAK step=500 index=38' "$TMP/small.log"
"$TMP/reflect" 224 20140 > "$TMP/big.log"
for step in 5000 10000 15000 20000; do grep "REFLECT_CHECKPOINT step=$step " "$TMP/big.log"; done
grep -q 'REFLECT_PREFIX_BREAK step=20124 index=38' "$TMP/big.log"
echo N02_REFLECTING_CENTRE_20000_GMP_STEPS_PASS

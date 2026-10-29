#!/bin/sh
set -eu
HERE="$(CDPATH='' cd -- "$(dirname -- "$0")" && pwd)"
ROOT="$(CDPATH='' cd -- "$HERE/../../.." && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
python3 "$HERE/glider_independent.py" "$ROOT"
g++ -std=c++17 -O3 -Wall -Wextra "$HERE/glider_replay.cpp" -lgmpxx -lgmp -o "$TMP/replay"
"$TMP/replay" 1 100 > "$TMP/small.log"
grep -q 'PREFIX_BREAK step=92 index=38' "$TMP/small.log"
"$TMP/replay" 228 20090 > "$TMP/big.log"
for step in 5000 10000 15000 20000; do grep "CHECKPOINT step=$step " "$TMP/big.log"; done
grep -q 'PREFIX_BREAK step=20068 index=38' "$TMP/big.log"
grep -q 'N02_GMP_AND_DIGIT_REPLAY_PASS q=228 steps=20090 first_bad=20068' "$TMP/big.log"
echo N02_GMP_20000_STEPS_AND_20068_FRONT_BREAK_PASS

#!/usr/bin/env bash
set -euo pipefail
DIR=calculation/new_structures/agent-W18
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
c++ -O3 -std=c++17 "$DIR/wall.cpp" -o "$TMP/wall"
c++ -O3 -std=c++17 "$DIR/bigint.cpp" -o "$TMP/bigint"
"$TMP/wall" 4138 20000 > "$TMP/wall.log"
"$TMP/bigint" 4138 20000 > "$TMP/big.log"
grep -q 'final_digits=16552 final_band=2 trims=11726 overflow=8274 final_hash=425518744' "$TMP/wall.log"
grep -q 'final_digits=16552 final_band=2 final_hash=425518744' "$TMP/big.log"
if "$TMP/wall" 4137 20000 >"$TMP/negative.log" 2>&1; then echo 'negative guard control failed'; exit 1; fi
grep -q 'BAND EXHAUSTED at t=19998 L=1' "$TMP/negative.log"
echo 'PASS: two independent arithmetic engines; 20,000 steps; exact finite-horizon padding threshold'

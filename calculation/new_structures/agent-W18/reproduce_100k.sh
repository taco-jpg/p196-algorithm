#!/usr/bin/env bash
set -euo pipefail
DIR=calculation/new_structures/agent-W18
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
c++ -O3 -std=c++17 "$DIR/wall.cpp" -o "$TMP/wall"
c++ -O3 -std=c++17 "$DIR/full_digits.cpp" -o "$TMP/full"
"$TMP/wall" 20702 100000 > "$TMP/wall.txt"
"$TMP/full" 20702 100000 > "$TMP/full.txt"
grep -q 'final_digits=82808 final_band=2 trims=58598 overflow=41402 final_hash=132839273' "$TMP/wall.txt"
grep -q 'final_digits=82808 final_hash=132839273' "$TMP/full.txt"
for t in 1 100 1000 5000 10000 100000; do
  grep -q "checkpoint t=$t " "$TMP/wall.txt"
  grep -q "checkpoint t=$t " "$TMP/full.txt"
done
if "$TMP/wall" 20701 100000 > "$TMP/guard.txt" 2>&1; then echo 'expected guard loss';exit 1;fi
grep -q 'BAND EXHAUSTED at t=99995 L=1' "$TMP/guard.txt"
echo 'PASS W18 100,000 full-digit and symbolic wall arithmetic checks'

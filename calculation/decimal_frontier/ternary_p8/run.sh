#!/bin/sh
# Full eight-step ternary centre classification; restartable, one C++ process.
set -eu
HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
OUT=${1:-/tmp/agent13-ternary-p8}
mkdir -p "$OUT"
c++ -O3 -std=c++17 "$HERE/p8_nfa.cpp" -o "$OUT/p8_nfa"
FILE="$OUT/n24.tsv"
START=0
if [ -s "$FILE" ]; then
  LAST=$(tail -n 1 "$FILE" | cut -f 1)
  START=$((LAST+1))
fi
while [ "$START" -lt 5814 ]; do
  END=$((START+800))
  if [ "$END" -gt 5814 ]; then END=5814; fi
  "$OUT/p8_nfa" "$START" "$END" 50000 "$FILE" 24
  START=$END
done
python3 "$HERE/verify.py" "$FILE"
python3 "$HERE/controls.py"

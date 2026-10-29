#!/bin/sh
# Exact single-core, nice-priority, resumable decimal 01010101 ternary F1 census.
set -eu
HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
OUT=${1:-/tmp/agent13-ternary-p8-rotation}
mkdir -p "$OUT"
c++ -O3 -std=c++17 "$HERE/p8_nfa_rotated.cpp" -o "$OUT/p8_rotated"
FILE="$OUT/all_n24.tsv"
START=0
if [ -s "$FILE" ]; then
  LAST=$(tail -n 1 "$FILE" | cut -f 1)
  START=$((LAST+1))
fi
while [ "$START" -lt 5814 ]; do
  END=$((START+500))
  if [ "$END" -gt 5814 ]; then END=5814; fi
  nice -n 10 "$OUT/p8_rotated" "$START" "$END" 50000 "$FILE" 24
  START=$END
done
python3 "$HERE/verify_rotation.py" "$FILE"
python3 "$HERE/controls.py"

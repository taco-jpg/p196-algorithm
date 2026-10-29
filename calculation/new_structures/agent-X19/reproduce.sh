#!/usr/bin/env bash
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
work="$(mktemp -d)"; trap 'rm -rf "$work"' EXIT
g++ -std=c++17 -O3 "$here/dual_replay.cpp" -o "$work/replay"
g++ -std=c++17 -O3 "$here/first_break.cpp" -o "$work/breaks"
"$work/breaks" > "$work/breaks.csv"
diff -u "$here/first_break.csv" "$work/breaks.csv"
python3 "$here/independent.py"
"$work/replay" 100 100 300
"$work/replay" 5500 6300 20000

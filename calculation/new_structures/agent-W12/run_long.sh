#!/bin/sh
set -eu
here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT HUP INT TERM
c++ -O3 -std=c++17 "$here/long.cpp" -o "$work/long"
"$work/long" 0 25000 "$work" 16000 428571 > "$work/result.txt"
"$work/long" 25000 50000 "$work" 16000 428571 >> "$work/result.txt"
"$work/long" 50000 75000 "$work" 16000 428571 >> "$work/result.txt"
"$work/long" 75000 100000 "$work" 16000 428571 >> "$work/result.txt"
diff -u "$here/long_expected.txt" "$work/result.txt"
cat "$work/result.txt"
echo 'PASS W12 all-q>=16000, 100000 decimal steps'

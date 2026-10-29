#!/bin/sh
set -eu
HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
TEMP=$(mktemp -d)
trap 'rm -rf "$TEMP"' EXIT HUP INT TERM
python3 "$HERE/sft.py" > "$TEMP/transfer.json"
PYTHONPATH="$HERE" python3 "$HERE/validate.py" > "$TEMP/validate.json"
python3 "$HERE/seed.py" --tiles 600 --random-seed 20261028 > "$TEMP/seed.txt"
g++ -O3 -std=c++17 "$HERE/replay_digits.cpp" -o "$TEMP/digits"
g++ -O3 -std=c++17 "$HERE/replay_gmp.cpp" -lgmpxx -lgmp -o "$TEMP/gmp"
"$TEMP/digits" "$TEMP/seed.txt" 20000 > "$TEMP/digit.log"
"$TEMP/gmp" "$TEMP/seed.txt" 20000 > "$TEMP/gmp.log"
grep '^CHECK' "$TEMP/digit.log" > "$TEMP/dcheck"
grep '^CHECK' "$TEMP/gmp.log" > "$TEMP/gcheck"
cmp "$TEMP/dcheck" "$TEMP/gcheck"
grep '^PASSED' "$TEMP/digit.log"
grep '^PASSED' "$TEMP/gmp.log"
sha256sum "$TEMP/seed.txt"
cat "$TEMP/dcheck"

#!/bin/sh
# From repository root: sh calculation/new_structures/agent-W09/renew60/reproduce.sh
set -eu
cd "$(dirname "$0")/../../../.."
D=calculation/new_structures/agent-W09
R=$D/renew60
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
c++ -std=c++17 -O3 "$D/replay_digits.cpp" -o "$TMP/digits"
c++ -std=c++17 -O3 "$D/replay_limbs.cpp" -o "$TMP/limbs"
python3 "$R/check60.py"
CAP=$(cat "$R/cap.csv")
"$TMP/digits" 22000 20000 "$CAP" > "$TMP/a"
"$TMP/limbs" 22000 20000 "$CAP" > "$TMP/b"
diff -u "$TMP/a" "$TMP/b"
diff -u "$TMP/a" "$R/checkpoints.txt"
echo "ALL W09-60 LOCAL CHECKS PASSED"

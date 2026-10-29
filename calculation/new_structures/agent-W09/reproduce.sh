#!/bin/sh
# Run from repository root: sh calculation/new_structures/agent-W09/reproduce.sh
set -eu
cd "$(dirname "$0")/../../.."
D=calculation/new_structures/agent-W09
TEMP=$(mktemp -d)
trap 'rm -rf "$TEMP"' EXIT
c++ -O3 -std=c++17 "$D/replay_digits.cpp" -o "$TEMP/digits"
c++ -O3 -std=c++17 "$D/replay_limbs.cpp" -o "$TEMP/limbs"
python3 "$D/pump_check.py"
"$TEMP/digits" 22000 20000 > "$TEMP/trace1"
"$TEMP/limbs" 22000 20000 > "$TEMP/trace2"
diff -u "$TEMP/trace1" "$TEMP/trace2"
diff -u "$D/checkpoints.txt" "$TEMP/trace1"
echo "ALL W09 LOCAL CHECKS PASSED"

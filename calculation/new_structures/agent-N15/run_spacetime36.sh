#!/bin/sh
set -eu
DIR=$(CDPATH= cd -- "$(dirname "$0")" && pwd)
python3 "$DIR/spacetime36.py" --check
TMP=$(mktemp "${TMPDIR:-/tmp}/agentN15-spacetime36.XXXXXXXX")
trap 'rm -f "$TMP"' EXIT HUP INT TERM
${CXX:-c++} -std=c++17 -O3 "$DIR/spacetime36_independent.cpp" -o "$TMP"
"$TMP" "$DIR/spacetime36_states.tsv"
printf '%s\n' 'AGENT_N15_36_STATE_SPACETIME_ALL_HEIGHT_PASS'

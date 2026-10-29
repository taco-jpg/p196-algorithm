#!/bin/sh
set -eu
DIR=$(CDPATH= cd -- "$(dirname "$0")" && pwd)
# Check the all-height arithmetic premise, then the new finite 240->32 grammar.
python3 "$DIR/ca_bounded.py" >/dev/null
python3 "$DIR/renorm32.py" --check
TMP=$(mktemp "${TMPDIR:-/tmp}/agentN15-renorm32.XXXXXXXX")
trap 'rm -f "$TMP"' EXIT HUP INT TERM
${CXX:-c++} -std=c++17 -O3 "$DIR/renorm32_independent.cpp" -o "$TMP"
"$TMP" "$DIR/renorm32_states.tsv"
printf '%s\n' 'AGENT_N15_32_STATE_SPATIAL_RENORM_PASS'

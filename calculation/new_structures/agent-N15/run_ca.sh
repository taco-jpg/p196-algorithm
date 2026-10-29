#!/bin/sh
# Both checkers are self-contained and use no optional packages.
set -eu
DIR=$(CDPATH= cd -- "$(dirname "$0")" && pwd)
python3 "$DIR/ca_proof.py"
TMP=$(mktemp "${TMPDIR:-/tmp}/agentN15-ca.XXXXXXXX")
trap 'rm -f "$TMP"' EXIT HUP INT TERM
${CXX:-c++} -std=c++17 -O2 "$DIR/ca_independent.cpp" -o "$TMP"
"$TMP"
printf '%s\n' 'AGENT_N15_SEVEN_EDGE_ALL_LEVEL_CHECK_PASS'

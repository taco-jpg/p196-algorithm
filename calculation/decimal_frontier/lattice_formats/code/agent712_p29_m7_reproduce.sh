#!/usr/bin/env bash
# Agent-712: reproducible full p29/m7 unrooted absorbing-bulk classification.
# All artifacts are generated in a temporary directory, never committed.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/../../../.." && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
CXX="${CXX:-g++}"
"$CXX" -std=c++17 -O2 "$ROOT/calculation/decimal_frontier/triple_ones_root/full_scc_controls.cpp" -o "$TMP/scc_controls"
(ulimit -v 8000000; nice -n 19 "$TMP/scc_controls") > "$TMP/controls.txt"
grep -q 'base=9 g=1100011000 nodes=956310 edges=1005301 nontriv_scc=7' "$TMP/controls.txt"
grep -q 'base=13 g=1010010000 nodes=250302 edges=254201 nontriv_scc=5' "$TMP/controls.txt"
grep -q 'SCC depth=61 size=4' "$TMP/controls.txt"
grep -q 'SCC depth=55 size=1' "$TMP/controls.txt"
grep -q 'SCC depth=75 size=1' "$TMP/controls.txt"
echo 'PASS mandatory base-9/base-13 full graph controls'
"$CXX" -std=c++17 -O3 "$HERE/agent712_p29_m7.cpp" -o "$TMP/census"
(ulimit -v 8000000; nice -n 19 "$TMP/census" --dump-map "$TMP/map.txt") > "$TMP/summary.txt"
python3 "$HERE/agent712_p29_m7_check.py" "$TMP/summary.txt" "$TMP/map.txt"
echo 'ALL AGENT-712 NON-LEAN CHECKS PASSED'

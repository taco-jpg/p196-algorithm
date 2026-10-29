#!/usr/bin/env bash
# Fully self-contained reproduction of the base-1286 neutral-band certificate.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
cd "$ROOT"
P=calculation/neutral_band/agent10_base1286
PY="${PYTHON:-python3}"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
"$PY" "$P/generate.py" --output "$TMP/cert_b1286.json"
cmp "$TMP/cert_b1286.json" "$P/cert_b1286.json"
"$PY" "$P/check.py" "$P/cert_b1286.json" 1000
c++ -std=c++17 -O3 "$P/replay.cpp" -o "$TMP/replay1286"
nice -n 10 "$TMP/replay1286" "$P/cert_b1286.json" 20000
c++ -std=c++17 -O3 calculation/decimal_frontier/lattice_formats/code/bauto3.cpp -o "$TMP/bauto3"
nice -n 10 "$TMP/bauto3" 9 10 10 -g 1100011000 -cap 3000000 -maxscc 10 > "$TMP/b9.txt"
grep -q 'cyclen=4' "$TMP/b9.txt"
grep -q 'depth=61' "$TMP/b9.txt"
echo 'CONTROL PASS: base 9 g=1100011000, period-4 SCC depth 61'
nice -n 10 "$TMP/bauto3" 13 10 10 -g 1010010000 -cap 3000000 -maxscc 10 > "$TMP/b13.txt"
grep -q 'depth=55' "$TMP/b13.txt"
grep -q 'depth=75' "$TMP/b13.txt"
echo 'CONTROL PASS: base 13 g=1010010000, singleton SCCs depths 55 and 75'
echo 'ALL BASE-1286 CERTIFICATE CONTROLS PASSED'

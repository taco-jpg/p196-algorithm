#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
python3 "$HERE/regenerate.py" | tee "$TMP/regen.log"
grep -F 'REGENERATION ALL CONTROLS PASSED' "$TMP/regen.log"
c++ -O3 -std=c++17 "$HERE/outage196.cpp" -o "$TMP/outage196"
"$TMP/outage196" 100000 | tee "$TMP/outage.log"
grep -F 'OUTAGE t=8 digits=7 firstHigh=0 successorOddIndex=0 successorPal=0' "$TMP/outage.log"
grep -F 'OUTAGE t=13 digits=9 firstHigh=3 successorOddIndex=2 successorPal=0' "$TMP/outage.log"
grep -F 'OUTAGE t=19 digits=11 firstHigh=1 successorOddIndex=0 successorPal=0' "$TMP/outage.log"
grep -F 'SUMMARY T=100000 finalDigits=41490 allEven=3 regenerated=3 noHigh=0' "$TMP/outage.log"
echo 'X27 REGENERATION ALL CHECKS PASSED'

#!/usr/bin/env bash
# Complete reproducibility control, run from any directory in a real checkout.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
SRC="$ROOT/calculation/decimal_frontier/exterior_census/src/Agent732P22History.cpp"
ORACLE="$ROOT/calculation/decimal_frontier/exterior_census/py/Agent732P22Oracle.py"
CONTROL="$ROOT/calculation/decimal_frontier/exterior_census/py/Agent732P22PositiveControls.py"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
ulimit -v 8388608  # 8 GiB virtual memory per process
c++ -O3 -std=c++17 -Wall -Wextra -Werror "$SRC" -o "$TMP/history"
python3 "$CONTROL"
python3 "$ORACLE" 0000111000100001110001 3 "$TMP/oracle.csv" > "$TMP/oracle.out"
nice -n 10 "$TMP/history" 0000111000100001110001 3 3 "$TMP/hist.csv" > "$TMP/dump.out"
diff -q "$TMP/oracle.csv" "$TMP/hist.csv"
nice -n 10 "$TMP/history" 00001110001 70 > "$TMP/p11.out"
grep -Fx 'WEIGHTED_FIXED_POINT at transition depth 59 -> 60 states=17' "$TMP/p11.out"
grep -Fx 'SUMMARY p=11 G=4 maxfront=828 fixed=59' "$TMP/p11.out"
# The p12 positive control does not reach a weighted fixed point by width 55.
set +e
nice -n 10 "$TMP/history" 000100010001 55 > "$TMP/p12.out"
RC=$?
set -e
[[ "$RC" -eq 1 ]]
grep -Fx 'depth=53 states=5622 accepted=3' "$TMP/p12.out"
nice -n 10 "$TMP/history" 0000111000100001110001 90 > "$TMP/p22.out"
python3 - "$TMP/p22.out" <<'PY'
import sys, re
s = open(sys.argv[1]).read().splitlines()
counts = {}
for line in s:
    m = re.match(r'depth=(\d+) states=(\d+) accepted=(\d+)$', line)
    if m:
        counts[int(m[1])] = int(m[3])
assert all(counts[d] == 1 for d in range(29, 89))
assert all(v == 0 for d, v in counts.items() if d < 29)
assert [l for l in s if l.startswith('  ACCEPT_E=')] == [
    '  ACCEPT_E=0011101001100111010011 MULT=1'] * 60
assert 'WEIGHTED_FIXED_POINT at transition depth 88 -> 89 states=257' in s
assert 'SUMMARY p=22 G=8 maxfront=651921 fixed=88' in s
print('P22 ALL-WIDTH UNIQUE B-HISTORY VERIFIED FROM EXACT WEIGHTED VECTOR')
PY

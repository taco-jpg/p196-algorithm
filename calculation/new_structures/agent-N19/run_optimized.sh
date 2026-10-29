#!/usr/bin/env bash
# New sharp k=13314 two-block witness, both independent engines and universal pump.
set -euo pipefail
cd "$(dirname "$0")"
w=$(mktemp -d);trap 'rm -rf "$w"' EXIT
g++ -O3 -std=c++17 bulk20k_digits.cpp -o "$w/digits"
g++ -O3 -std=c++17 bulk20k_gmp.cpp -o "$w/gmp" -lgmpxx -lgmp
g++ -O3 -std=c++17 bulk20k_pump_q.cpp -o "$w/pump"
"$w/digits" 13314 20000 100 > "$w/digits.csv" 2> "$w/digitlog"
"$w/gmp" 13314 10000 100 0 - "$w/mid.txt" > "$w/first.csv" 2> "$w/gmplog1"
"$w/gmp" 13314 20000 100 10000 "$w/mid.txt" - > "$w/second.csv" 2> "$w/gmplog2"
{ cat "$w/first.csv"; tail -n+3 "$w/second.csv"; } > "$w/gmp.csv"
diff -u "$w/digits.csv" "$w/gmp.csv"
printf '%s  %s\n' '0992a0a6c9922c58ef7ce696b8496227974ac01eec066289ca41d8019c5a40fe' "$w/gmp.csv" | sha256sum -c -
python3 allq_matrix.py "$w/digits.csv"
"$w/pump" 13314 20000 1 > "$w/pumplog"
grep 'PUMP_ALL_STEPS_PASS k=13314 T=20000 q=1 min_odd=2' "$w/pumplog"
python3 - "$w/digits.csv" optimized_checkpoints.csv <<'PY'
import csv,sys
with open(sys.argv[1]) as f: rows=list(csv.DictReader(f))
with open(sys.argv[2]) as f: cp=list(csv.DictReader(f))
assert len(rows)==20001
for r in cp:
 t=int(r['step']);assert all(rows[t][key]==value for key,value in r.items())
assert int(rows[-1]['digits'])==61497
assert int(rows[-1]['left_count'])==134
assert int(rows[-1]['right_count'])==100
assert int(rows[-1]['junction'])==13183
PY
set +e
"$w/digits" 13313 20000 100 > /dev/null 2> "$w/negative"
code=$?
set -e
test "$code" -eq 3
grep 'BLOCK_SHAPE_FAILURE t=19999' "$w/negative"
echo N19_OPTIMIZED_13314_ALL_CHECKS_PASSED
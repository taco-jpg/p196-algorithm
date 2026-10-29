#!/usr/bin/env bash
# Full 20k two-block decimal replay. Requires C++17, GMP, Python3, sha256sum.
set -euo pipefail
cd "$(dirname "$0")"
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
g++ -O3 -std=c++17 bulk20k_digits.cpp -o "$tmp/digits"
g++ -O3 -std=c++17 bulk20k_gmp.cpp -o "$tmp/gmp" -lgmpxx -lgmp
"$tmp/digits" 15000 20000 100 > "$tmp/digits.csv" 2> "$tmp/digits.err"
"$tmp/gmp" 15000 10000 100 0 - "$tmp/midpoint.txt" > "$tmp/gmp_first.csv" 2> "$tmp/gmp_first.err"
"$tmp/gmp" 15000 20000 100 10000 "$tmp/midpoint.txt" - > "$tmp/gmp_second.csv" 2> "$tmp/gmp_second.err"
{ cat "$tmp/gmp_first.csv"; tail -n +3 "$tmp/gmp_second.csv"; } > "$tmp/gmp.csv"
diff -u "$tmp/digits.csv" "$tmp/gmp.csv"
printf '%s  %s\n' 0ac6f1d97ed2da30430bd1d8f393918691de847abcf4b678738b27187b297851 "$tmp/gmp.csv" | sha256sum -c -
python3 - "$tmp/digits.csv" bulk20k_checkpoints.csv <<'PY'
import csv,sys
with open(sys.argv[1]) as f: rows=list(csv.DictReader(f))
assert len(rows)==20001
with open(sys.argv[2]) as f: cp=list(csv.DictReader(f))
for r in cp:
    t=int(r['step']);assert all(rows[t][k]==v for k,v in r.items()),(t,r,rows[t])
assert int(rows[-1]['digits'])==68241
assert int(rows[-1]['left_count'])==1820 and int(rows[-1]['right_count'])==1786
assert int(rows[-1]['junction'])==13183
print('N19_TWO_BLOCK_20000_ALL_CHECKS_PASSED')
PY
cat "$tmp/digits.err" "$tmp/gmp_first.err" "$tmp/gmp_second.err"
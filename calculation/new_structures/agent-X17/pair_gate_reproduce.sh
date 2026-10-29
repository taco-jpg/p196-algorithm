#!/usr/bin/env bash
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
python3 "$here/pair_gate.py" "$tmp/pair.csv"
python3 - "$here/pair_gate.csv" "$tmp/pair.csv" <<'PY'
import csv,sys
with open(sys.argv[1],newline='') as a, open(sys.argv[2],newline='') as b:
 assert list(csv.reader(a)) == list(csv.reader(b))
print('PASS: 18 independently recomputed Python bigint neutral-charge gate rows')
PY
cxx="${CXX:-g++}"
"$cxx" -std=c++17 -O3 -Wall -Wextra -Werror "$here/shadow.cpp" -o "$tmp/single"
"$cxx" -std=c++17 -O3 -Wall -Wextra -Werror "$here/shadow_pair.cpp" -o "$tmp/pair"
"$cxx" -std=c++17 -O3 -Wall -Wextra -Werror "$here/independent_pair_gmp.cpp" -lgmpxx -lgmp -o "$tmp/gmp"
"$tmp/single" 10001 110 88283583 "$tmp/single7.csv" 7 2> "$tmp/single7.log"
"$tmp/single" 10001 110 88283583 "$tmp/single8.csv" 8 2> "$tmp/single8.log"
"$tmp/pair" 10001 20000 88283583 "$tmp/pair78.csv" 7 8 2> "$tmp/pair78.log"
"$tmp/gmp" 10001 20000 88283583 7 8 "$tmp/gmp78.csv" 2> "$tmp/gmp78.log"
"$tmp/pair" 10001 600 88283583 "$tmp/pair12.csv" 1 2 2> "$tmp/pair12.log"
python3 - "$tmp/single7.csv" "$tmp/single8.csv" "$tmp/pair78.csv" "$tmp/gmp78.csv" "$tmp/pair12.log" "$here/pair78_checkpoints.csv" <<'PY'
import csv,sys
singles=[list(csv.DictReader(open(p))) for p in sys.argv[1:3]]
for rows in singles:
 r=next(r for r in rows if r['t']=='108')
 assert r['shadow_right']=='60'
pair={r['t']:r for r in csv.DictReader(open(sys.argv[3]))}
assert pair['108']['shadow_right']=='4971'
gmp=list(csv.DictReader(open(sys.argv[4])))
assert len(gmp)==211
with open(sys.argv[6],newline='') as a: assert list(csv.reader(a)) == list(csv.reader(open(sys.argv[4])))
for r in gmp:
 a=pair[r['t']]
 assert a['length']==r['length']
 assert min(int(a['shadow_left']),int(a['shadow_right']))==int(r['matched'])
 assert a['outer_witness']==r['min_witness']
 assert a['base_hash']==r['base_hash'] and a['pert_hash']==r['pert_hash']
assert gmp[-1]['t']=='20000' and gmp[-1]['length']=='18316' and gmp[-1]['matched']=='2154'
assert 'first_length_split=520' in open(sys.argv[5]).read()
print('PASS: two individually destructive offsets combine into 20k-safe pair (7,8)')
print('PASS: 20,001 full-word GMP/digit comparisons, 211 matching checkpoints, 0 palindromes')
print('PASS: distinct bad-control pair (1,2) collides at step 520, no infinity claim')
PY

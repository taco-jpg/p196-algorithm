#!/usr/bin/env bash
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
python3 "$here/charge_gate.py" "$tmp/charge.csv"
python3 - "$here/charge_gate.csv" "$tmp/charge.csv" <<'PY'
import csv,sys
with open(sys.argv[1],newline='') as a, open(sys.argv[2],newline='') as b:
    assert list(csv.reader(a))==list(csv.reader(b))
print('PASS: all 15 exact incoming-carry states')
PY
cxx="${CXX:-g++}"
"$cxx" -std=c++17 -O3 -Wall -Wextra -Werror "$here/shadow.cpp" -o "$tmp/digits"
"$cxx" -std=c++17 -O3 -Wall -Wextra -Werror "$here/independent_offset_gmp.cpp" -lgmpxx -lgmp -o "$tmp/gmp"
"$tmp/digits" 10001 20000 88283583 "$tmp/digits.csv" 3
"$tmp/gmp" 10001 20000 88283583 3 "$tmp/gmp.csv"
python3 - "$tmp/digits.csv" "$tmp/gmp.csv" <<'PY'
import csv,sys
rows={r['t']:r for r in csv.DictReader(open(sys.argv[1]))}
gmp=list(csv.DictReader(open(sys.argv[2])))
assert len(gmp)==211
for r in gmp:
    a=rows[r['t']]
    assert a['length']==r['length']
    assert min(int(a['shadow_left']),int(a['shadow_right']))==int(r['matched'])
    assert a['outer_witness']==r['min_witness']
    assert a['base_hash']==r['base_hash'] and a['pert_hash']==r['pert_hash']
assert gmp[-1]['t']=='20000' and gmp[-1]['length']=='18316' and gmp[-1]['matched']=='2151'
print('PASS: 20,001 full-word GMP/digit comparisons, 211 matching checkpoints, offset-3 gate protection')
PY
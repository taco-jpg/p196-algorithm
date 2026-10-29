#!/usr/bin/env bash
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
cxx="${CXX:-g++}"
python3 "$here/phase_gate.py" "$tmp/phase_gate.csv"
python3 - "$here/phase_gate.csv" "$tmp/phase_gate.csv" <<'PYROWS'
import csv,sys
with open(sys.argv[1], newline='') as a, open(sys.argv[2], newline='') as b:
    assert list(csv.reader(a)) == list(csv.reader(b))
print('PASS: 32 stored neutral-carry phase checkpoints')
PYROWS
"$cxx" -std=c++17 -O3 -Wall -Wextra -Werror "$here/shadow.cpp" -o "$tmp/digits"
"$cxx" -std=c++17 -O3 -Wall -Wextra -Werror "$here/independent_gmp.cpp" -lgmpxx -lgmp -o "$tmp/gmp"
"$tmp/digits" 10009 20000 88283583 "$tmp/digits.csv" 1
"$tmp/gmp" 10009 20000 88283583 "$tmp/gmp.csv"
python3 - "$tmp/digits.csv" "$tmp/gmp.csv" <<'PY'
import csv,sys
x={r['t']:r for r in csv.DictReader(open(sys.argv[1]))}
y=list(csv.DictReader(open(sys.argv[2])))
assert len(y)==211
for r in y:
    a=x[r['t']]
    assert (a['length']==r['length'] and
            min(int(a['shadow_left']), int(a['shadow_right']))==int(r['matched']) and
            a['outer_witness']==r['min_witness'] and
            a['base_hash']==r['base_hash'] and a['pert_hash']==r['pert_hash'])
assert y[-1]['t']=='20000' and y[-1]['length']=='18324'
print('PASS: 20,001 complete-word GMP-vs-digit comparisons; 211 matching checkpoints; phase-nine motif')
PY
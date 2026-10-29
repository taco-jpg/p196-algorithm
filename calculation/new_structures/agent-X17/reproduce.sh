#!/usr/bin/env bash
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
cxx="${CXX:-g++}"
"$cxx" -std=c++17 -O3 -Wall -Wextra -Werror "$here/shadow.cpp" -o "$tmp/shadow"
"$cxx" -std=c++17 -O3 -Wall -Wextra -Werror "$here/independent_gmp.cpp" -lgmpxx -lgmp -o "$tmp/oracle"
"$tmp/shadow" 10001 20000 83271645 "$tmp/shadow.csv" 1
"$tmp/oracle" 10001 20000 83271645 "$tmp/gmp.csv"
python3 - "$tmp/shadow.csv" "$tmp/gmp.csv" "$here/checkpoints.csv" <<'PY'
import csv,sys
traces=[list(csv.DictReader(open(z))) for z in sys.argv[1:]]
a,b,stored=traces
assert len(a)==len(b)==len(stored)==211
for x,y,z in zip(a,b,stored):
    assert x['t']==y['t']==z['t']
    assert x['length']==y['length']==z['length']
    assert min(int(x['shadow_left']),int(x['shadow_right']))==int(y['matched'])==int(z['matched'])
    assert x['outer_witness']==y['min_witness']==z['min_witness']
    assert x['base_hash']==y['base_hash']==z['base_hash']
    assert x['pert_hash']==y['pert_hash']==z['pert_hash']
assert b[-1]['t']=='20000' and b[-1]['matched']=='2202'
print('PASS 211 persisted checkpoints and complete-word GMP/digit agreement at all 20,001 steps')
PY
# Recheck the precise first departure from the shadow format past the valid horizon.
"$tmp/shadow" 10001 55000 83271645 "$tmp/extended.csv" 1
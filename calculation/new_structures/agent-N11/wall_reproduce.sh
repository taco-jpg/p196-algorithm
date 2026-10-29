#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
g++ -O3 -std=c++17 -Wall -Wextra "$HERE/bubble_lifetime.cpp" -o "$TMP/bubble_lifetime"
g++ -O3 -std=c++17 -Wall -Wextra "$HERE/wall_independent.cpp" -o "$TMP/wall_independent"
"$TMP/bubble_lifetime" 45000 110000 10000 >"$TMP/forward.txt"
"$TMP/wall_independent" 45000 110000 10000 >"$TMP/independent.txt"
python3 - "$HERE/expected_wall.json" "$TMP/forward.txt" "$TMP/independent.txt" <<'PY'
import json,sys,re,pathlib
e=json.loads(pathlib.Path(sys.argv[1]).read_text())
a=pathlib.Path(sys.argv[2]).read_text()
b=pathlib.Path(sys.argv[3]).read_text()
assert ('ZERO DOMAIN ENDED t='+str(e['tracked_domain_lost_step'])) in a
assert ('INDEPENDENT WALL ENDED t='+str(e['tracked_domain_lost_step'])) in b
assert ('final_digits='+str(e['final_length_at_loss'])) in a
assert ('final_digits='+str(e['final_length_at_loss'])) in b
assert ('hash='+e['final_fnv_hash_at_loss']) in b
assert 'grow=0' in a
for r in e['sample']:
    t=r['t'];key='t='+str(t)
    row=next(x for x in a.splitlines() if x.startswith(key+' '))
    assert ('len='+str(r['length'])) in row
    assert ('a='+str(r['left'])) in row and ('b='+str(r['right'])) in row
    assert ('width='+str(r['width'])) in row
    ind=next(x for x in b.splitlines() if x.startswith('INDEPENDENT '+key+' '))
    for k,v in [('len',r['length']),('left',r['left']),('right',r['right']),('width',r['width'])]:
        assert (k+'='+str(v)) in ind,(t,k,ind)
    assert ('hash='+r['hash']) in ind
for r in e['table']:
    suffix='left+='+str(r['left_inc'])+' right-='+str(r['right_dec'])+' count='+str(r['count'])
    assert 'wall_transition gam='+str(r['gamma'])+' '+suffix in a
    assert 'INDEPENDENT transition g='+str(r['gamma'])+' '+suffix in b
assert sum(r['count'] for r in e['table'])==e['wall_step_counts']
print('ALL WALL CHECKS PASSED: 74,927 nonpalindrome checks in BOTH literal engines;')
print('moving domain survives t=1..74925, lost t=74926; 74,924 exact wall transitions;')
print('independent matching checkpoints and boundary-state counts')
PY

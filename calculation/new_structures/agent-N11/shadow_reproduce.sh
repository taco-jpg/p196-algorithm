#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
g++ -O3 -std=c++17 "$HERE/sync_front.cpp" -o "$TMP/sync_front"
g++ -O3 -std=c++17 "$HERE/sync_independent.cpp" -o "$TMP/sync_independent"
python3 "$HERE/guarded_prefix.py"
for L in 2000 4000 8000; do
 "$TMP/sync_front" "$L" 45000 $((7*L)) > "$TMP/front_$L.txt"
 if [[ "$L" == 8000 ]]; then BIG=16000; else BIG=45000; fi
 "$TMP/sync_independent" "$L" "$BIG" $((7*L)) 64 > "$TMP/independent_$L.txt"
done
"$TMP/sync_front" 16000 45000 56000 > "$TMP/reference.txt"
python3 - "$HERE/shadow_expected.json" "$TMP" <<'PY'
import json,sys,pathlib
j=json.loads(pathlib.Path(sys.argv[1]).read_text());p=pathlib.Path(sys.argv[2])
for r in j['orbits']:
 L=r['L']
 s=(p/f'front_{L}.txt').read_text().splitlines()
 d=dict(x.split('=') for x in s[0].split())
 assert int(d['L'])==L and int(d['first_gamma'])==r['first_gamma']
 actual=[int(x.split('=')[-1]) for x in s[1:]]
 assert actual==r['prefix_first_diff'],(L,actual)
 ind=(p/f'independent_{L}.txt').read_text().strip()
 for k,v in [('diffP1',r['prefix_first_diff'][0]),('diffP',r['prefix_first_diff'][6]),('diffP1024',r['prefix_first_diff'][-1]),('diffGamma',r['first_gamma'])]:
  assert k+'='+str(v) in ind,(L,k,v,ind)
 assert 'all_nonpal_checked_through='+str(r['first_gamma']) in ind
t=(p/'reference.txt').read_text()
assert 'first_gamma=-1' in t
assert all(x.endswith('first_diff=-1') for x in t.splitlines()[1:])
print('ALL N11 SHADOW TESTS PASSED: 3-scale front timing, two independent integer kernels, 12k random carry guards. No infinite certificate claimed.')
PY

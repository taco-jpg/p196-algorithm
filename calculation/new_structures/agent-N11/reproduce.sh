#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
for module in bubble_family bubble_independent orbit_mine adaptive_rule neutral_switch trace_defect; do
  g++ -O3 -std=c++17 -Wall -Wextra "$HERE/$module.cpp" -o "$TMP/$module"
done
"$TMP/bubble_family" 45000 20000 1000 >"$TMP/forward.txt"
"$TMP/bubble_independent" 45000 20000 1000 >"$TMP/independent.txt"
"$TMP/adaptive_rule" 100000 100 >"$TMP/adaptive.txt"
(cd "$TMP" && "$TMP/neutral_switch" 100000 100 >neutral.txt)
"$TMP/trace_defect" 96400 10 10 >"$TMP/trace.txt"
"$TMP/orbit_mine" 5000 1000 128 1000 "$TMP/short" 2>"$TMP/short.err"
python3 "$HERE/independent_check.py" --steps 5000 --sample-file "$TMP/short_samples.tsv"
python3 - "$TMP" "$HERE/expected.json" <<'PY'
import sys,json,pathlib
p=pathlib.Path(sys.argv[1])
e=json.loads(pathlib.Path(sys.argv[2]).read_text())
def records(path):
    out={}
    for line in path.read_text().splitlines():
        if line.startswith('t='):
            r=dict(x.split('=',1) for x in line.split() if '=' in x)
            out[int(r['t'])]=(int(r['length']),r['hash'])
    return out
a=records(p/'forward.txt');b=records(p/'independent.txt')
assert len(a)==21 and a==b,('independent checkpoint mismatch',a,b)
for x in e['decimal_zero_shield']['checkpoints']:
    assert a[x['t']]==(x['length'],x['fnv'])
assert 'PASS L=45000 steps=20000 no_pal=20001 shield_checks=20000 final_digits=98491' in (p/'forward.txt').read_text()
assert 'INDEPENDENT PASS L=45000 steps=20000 no_pal=20001 all_shields=PASS final_digits=98491' in (p/'independent.txt').read_text()
s=(p/'adaptive.txt').read_text()
assert 'tested_cells 10340000' in s and 'max_run9_on_samples 7' in s
for k,v in enumerate(e['carry_shadow']['eligible_by_K']):
    assert 'K '+str(k)+' eligible '+str(v)+' ' in s
assert all('errors 0' in x for x in s.splitlines() if x.startswith('K '))
z=(p/'neutral.txt').read_text()
assert 'total=390 errors=0' in z
assert 'symbol0 39 neutral9 107 symbol18 26' in z
assert 'symbol0 52 neutral9 110 symbol18 56' in z
assert 'source_t=96400 chain_start_i=5745' in (p/'trace.txt').read_text()
print('QUICK CONTROLS PASSED: two independent 20k replays, every zero site, 21 matching hashes, 100k carry profile, transient trace')
PY
if [[ "$#" -gt 0 && "$1" == "--quick" ]]; then
  exit 0
fi
"$TMP/orbit_mine" 1000000 1000 128 10 "$TMP/million" 2>"$TMP/million.err"
python3 - "$TMP" "$HERE/expected.json" <<'PY'
import sys,json,csv,pathlib
p=pathlib.Path(sys.argv[1])
e=json.loads(pathlib.Path(sys.argv[2]).read_text())['orbit196']
with (p/'million_samples.tsv').open() as f:
    rows=list(csv.DictReader(f,delimiter='\t'))
r=rows[-1]
assert int(r['step'])==e['steps']
assert int(r['length'])==e['final_digits']
assert r['fnv_hash']==e['final_fnv_hash']
assert int(r['pal'])==0
s=(p/'million_overflow.txt').read_text().strip()
assert len(s)==e['steps'] and s.count('1')==e['overflow_ones']
print('FULL CONTROLS PASSED: 1,000,000 literal 196 steps, all nonpalindromic; length',r['length'],'overflow',s.count('1'))
PY

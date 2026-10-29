#!/usr/bin/env bash
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
"${CXX:-g++}" -std=c++17 -O3 -Wall -Wextra -Werror "$here/pump_partitions.cpp" -o "$tmp/pump"
"$tmp/pump" 1001 850 "$tmp/pump_1001.csv" 2> "$tmp/pump_1001.log"
"$tmp/pump" 2001 1700 "$tmp/pump_2001.csv" 2> "$tmp/pump_2001.log"
python3 "$here/pump_fold.py" 1001 108 "$tmp/fold_1001.csv"
python3 "$here/pump_gate.py" "$tmp/pump_gate.csv" "$here/charge_logic_2001.csv" 2001
python3 - "$here" "$tmp" <<'PY'
import sys,csv
from pathlib import Path
here,tmp=map(Path,sys.argv[1:])
def rows(path):
 with open(path,newline='') as f:return list(csv.DictReader(f))
# Independent per-mask folded insertion (C++) and bigint exact uniform 108 phases (Python).
stored=rows(here/'pump_partition_checkpoints.csv')
for r in stored:
 n=int(r['n']);test={int(x['t']):x for x in rows(tmp/f'pump_{n}.csv')}
 x=test[int(r['t'])]
 assert all(x[k]==r[k] for k in x), (n,r['t'])
for n,first,last in [(1001,776,813),(2001,1602,1667)]:
 rr=rows(tmp/f'pump_{n}.csv')
 assert next(int(x['t']) for x in rr if int(x['valid_masks'])<256)==first
 assert next(int(x['t']) for x in rr if int(x['valid_masks'])==0)==last
 assert max(int(x['unique_cut_blocks']) for x in rr)==(4 if n==1001 else 5)
with open(here/'pump_gate_2001.csv',newline='') as a,open(tmp/'pump_gate.csv',newline='') as b:
 assert list(csv.reader(a))==list(csv.reader(b))
fold=rows(tmp/'fold_1001.csv')
assert len(fold)==108 and all(int(x['common_choices'])>=1 for x in fold)
assert int(fold[-1]['valid_min'])==61
sys.path.insert(0,str(here))
from pump_fold import initial,fold as folding,st
v=initial(1017,0); saved=rows(here/'pump_left_108.csv')
assert len(saved)==108
for t,(a,b) in enumerate(zip(fold,saved)):
 assert int(a['t'])==int(b['t'])==t
 j=int(a['valid_min']);assert j==int(b['cut_j'])
 pairs,_=folding(v)
 word=''.join(''.join(z) for z in pairs[j:j+8])
 assert word==b['common_8_folded_pairs']
 v=st(v)
print('PASS: 256-mask exact folded pump through 107, 108 uniform eight-pair words')
print('PASS: two-branch t108 charge-controlled 09^8 / 00^8 pump across 256 masks')
print('PASS: C++ full 256-mask fold relation to collision, recorded failure bounds')
PY
if [ "${DEEP:-0}" = 1 ]; then python3 "$here/pump_fold.py" 2001 108 "$tmp/fold_2001.csv"; fi

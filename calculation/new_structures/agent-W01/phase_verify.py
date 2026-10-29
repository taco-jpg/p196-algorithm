#!/usr/bin/env python3
"""Independent exact CSV checker for W01 four-orbit nine-geometry phase covariance.

Regenerates no input by itself; call phase_run.sh to replay real decimal digit vectors.
"""
import csv
import sys
from pathlib import Path

YS = [8000+80*k for k in range(-3,6)]
T=20000
if len(sys.argv)!=len(YS)+1:
    raise SystemExit('usage: phase_verify.py '+ ' '.join(f'phase_{y}.csv' for y in YS))
D={}
for y,filename in zip(YS,sys.argv[1:]):
    with open(filename,newline='') as f:
        rows=list(csv.DictReader(f))
    D[y]={int(r['t']):r for r in rows}
    assert len(rows)==T-1750+1,(y,len(rows))
    assert all(len(r['low'])==len(r['high'])==61 for r in rows),y
    assert all((r['low'].count('?') in (0,61)) and (r['high'].count('?') in (0,61)) for r in rows),y
    assert min(D[y])==1750 and max(D[y])==20000

expected={}
with (Path(__file__).resolve().parent/'phase_expected.csv').open(newline='') as f:
    for r in csv.DictReader(f):
        expected[int(r['k'])]=r
assert set(expected)==set(range(-3,6))
for k,y in enumerate(YS,start=-3):
    first=next((t,int(r['front'])) for t,r in D[y].items() if int(r['front'])>=0)
    assert first==(2154+88*k,7514+60*k), (k,first)
    assert int(expected[k]['y'])==y
    assert first==(int(expected[k]['birth_t']),int(expected[k]['birth_front']))

# All valid aligned t intervals, not interpolated or extrapolated.
lastbad={-3:2747,-2:2831,-1:2761,1:2747,2:3019,3:2747,4:2747,5:2747}
rows=0;equalities=0
for k in [z for z in range(-3,6) if z]:
    y=8000+80*k
    failed=[]
    for t in range(2300,T+1):
        if t+88*k not in D[y]:continue
        a,b=D[8000][t],D[y][t+88*k]
        correct=(int(b['front'])==int(a['front'])+60*k and a['low']==b['low'] and a['high']==b['high'])
        if not correct:failed.append(t)
        if t>=3020:
            assert correct,(k,t)
            rows+=1
            equalities+=2*61
    assert lastbad[k]==int(expected[k]['last_bad_reference'])
    assert failed and failed[-1]==lastbad[k],(k,failed[-1] if failed else None)
    # Deliberately corrupted spatial displacements, all must fail.
    assert int(D[y][3100+88*k]['front'])!=int(D[8000][3100]['front'])+60*k+1,k
    # At least this reference phase must fail when shifted by a wrong time step.
    a=D[8000][3100]
    bad=D[y][3100+88*k-1]
    assert (a['low'],a['high'])!=(bad['low'],bad['high']),k

assert rows==134528, rows
assert equalities==16412416,equalities
print('W01_NINE_GEOMETRY_PASS cases=9 actual_orbits=36 steps=20000 aligned_rows='
      +str(rows)+' signed_digit_checks='+str(equalities)+' last_failures='+str(lastbad))

#!/usr/bin/env python3
"""Reproduce K1 p8 rec0 centre-window SAT results using repository CaDiCaL.

Run from the repository root (python-sat, CaDiCaL153 required):
python3 calculation/decimal_frontier/lattice_kinks/code/agent1_width14_reproduce.py --controls
python3 calculation/decimal_frontier/lattice_kinks/code/agent1_width14_reproduce.py --width 14 --offset 0 --horizon 80

Uses the exact published `sat_kink.build` CNF and the p8_scc record already
tracked under calculation/decimal_frontier/lattice_formats/p8_scc.txt.
Independent positive-witness check uses actual Python big integers, not SAT
carry formulas. Every UNSAT proof is solver-based (not a Lean kernel theorem).
"""
import argparse
import json
import tempfile
from pathlib import Path
from agent303_w8_exclusion import write_lat0
from sat_kink import build, load_lat, solve
from lib7 import Lattice, parse_scc, digits_from_pair

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
REGRESSION_UNSAT = {0:33, 1:35, 2:30, 3:39}
REGRESSION_SAT = {0:32, 1:34, 2:28, 3:38}


def decode_layer(row, model_positive):
    result=[]
    for x in row:
        if isinstance(x,int): result.append(x)
        else:
            vals=[j for j,literal in enumerate(x) if literal in model_positive]
            assert len(vals)==1, ('not one hot',vals)
            result.append(vals[0])
    return result


def independent_bigint_check(w, offset, steps, layers, model):
    """Independently replay all SAT layers by decimal string + big-int RAA.

    We reconstruct a genuine 400+offset digit seed whose pair sums agree with
    the SAT initial free centre and prescribed exterior. This does not certify
    infinitely many palindrome-free steps; it checks finite model soundness.
    """
    rec=parse_scc(str(ROOT/'calculation/decimal_frontier/lattice_formats/p8_scc.txt'))[0]
    lat=Lattice(rec)
    assert (lat.p,lat.nB,lat.m)==(8,39,20)
    n0=400+offset
    K=w+6
    half=(n0+1)//2
    pos={lit for lit in model if lit>0}
    first=decode_layer(layers[0],pos)
    low=[lat.cell(0,x) for x in range(half)]
    assert first[:6]==low[half-K:half-K+6]
    low[half-K:half]=first
    P=low+low[:n0//2][::-1] if n0%2 else low+low[::-1]
    digits=digits_from_pair(P)
    assert digits[-1]>0
    N=int(''.join(str(d) for d in digits[::-1]))
    for t in range(steps+1):
        s=str(N)
        assert s != s[::-1], ('palindrome in finite positive control',t)
        actual=[int(c) for c in s[::-1]]
        n=len(actual)
        h=(n+1)//2
        word=[actual[j]+actual[n-1-j] for j in range(n)]
        assert n==n0+sum(lat.g[j%8] for j in range(t)), ('length',t,n)
        actual_layer=word[h-K:h]
        expected=decode_layer(layers[t],pos)
        assert actual_layer==expected, ('model mismatch',t,actual_layer,expected)
        for j in range(lat.nB,h-K+6):
            assert word[j]==lat.cell(t,j),('bulk mismatch',t,j,word[j],lat.cell(t,j))
        if t<steps:
            N+=int(s[::-1])
    return True


def check(lat,w,o,H,expected=None,independent=True):
    encoding,layers,K,ns=build(lat,w,o,'hor',H)
    sat,model,seconds=solve(encoding)
    label='SAT' if sat else 'UNSAT'
    print(f'K1 width={w} class={o} horizon={H}: {label} '
          f'vars={encoding.nv} clauses={len(encoding.cl)} seconds={seconds:.3f}',flush=True)
    if expected is not None and bool(sat)!=bool(expected):
        raise AssertionError(f'expected {expected}, observed {label}')
    if sat and independent:
        independent_bigint_check(w,o,H,layers,model)
        print(f'INDEPENDENT BIG-INT REPLAY PASS width={w} class={o} steps={H}',flush=True)
    return sat


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--controls',action='store_true')
    ap.add_argument('--all',action='store_true',help='run controls and all completed cases from case JSON')
    ap.add_argument('--cases',type=Path,default=HERE.parent/'data'/'agent1_width14_cases.json')
    ap.add_argument('--width',type=int)
    ap.add_argument('--offset',type=int,choices=range(4))
    ap.add_argument('--horizon',type=int)
    args=ap.parse_args()
    with tempfile.TemporaryDirectory() as temp:
        path=Path(temp)/'lat0.txt'
        write_lat0(path)
        lat=load_lat(str(path))
        assert (lat['p'],lat['nB'],lat['m'],lat['gam'])==(8,39,20,[1,0,1,0,1,0,1,0])
        if args.controls or args.all:
            for offset in range(4):
                check(lat,8,offset,REGRESSION_UNSAT[offset],False)
                check(lat,8,offset,REGRESSION_SAT[offset],True)
            print('EIGHT PUBLISHED CONTROL CASES PASS',flush=True)
            check(lat,14,3,30,True)
            print('WIDTH14 POSITIVE FINITE SURVIVOR CONTROL PASS',flush=True)
        if args.all:
            data=json.loads(args.cases.read_text())
            if data.get('status')!='COMPUTED':
                raise RuntimeError('Case file has not recorded a completed result; no exclusion claim')
            assert data['base']==10 and data['overflow']=='10101010' and data['free_half_width']==14
            bounds=data['confirmed_unsat_by_phase']
            assert set(bounds)==set(map(str,range(4)))
            for offset in range(4):
                check(lat,14,offset,int(bounds[str(offset)]),False)
            print('ALL WIDTH14 PHASE CLASSES UNSAT, no state cap',flush=True)
        if args.width is not None:
            if args.offset is None or args.horizon is None:
                ap.error('--width requires --offset and --horizon')
            check(lat,args.width,args.offset,args.horizon)

if __name__=='__main__':main()

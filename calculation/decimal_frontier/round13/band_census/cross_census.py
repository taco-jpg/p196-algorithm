#!/usr/bin/env python3
import os
"""Cross-check the bitset census against the SAT enumeration: for (s, T): the set of necklaces of phase-0 rows V with V_T=V.
usage: cross_census.py CLOCK s T [b]"""
import sys, re
sys.path.insert(0,os.path.expanduser('~/p196_run/r13a'))
import bandsat as BS, mkjobs as MK
import bandenum_sat as ES
clock=sys.argv[1]; s=int(sys.argv[2]); T=int(sys.argv[3]); b=int(sys.argv[4]) if len(sys.argv)>4 else 10
cl=[int(c) for c in clock]; p=len(cl)
def canon(V):
    return min(tuple(V[r:]+V[:r]) for r in range(len(V)))
# census rows: walk each band's F-cycle (phase-0 rows)
scensus=set()
for B in MK.parse(clock,8):
    if B['s']!=s or T%B['T']: continue
    V=[int(x) for x in B['V'].split(',')]
    x=list(V)
    for _ in range(B['T']//p):
        scensus.add(canon(x))
        for t in range(p):
            x,*_=BS.rowstep(x,cl[t],b)
# SAT
found,complete,tt=ES.enum_bands(b,cl,s,T,200000)
ssat=set(found.keys())
# primitive only in census; SAT includes non-primitive words -> filter
def primitive(c):
    n=len(c)
    return not any(n%d==0 and all(c[i]==c[(i+d)%n] for i in range(n)) for d in range(1,n))
ssat_p={c for c in ssat if primitive(c)}
print(f'clock={clock} s={s} T={T}: census necklaces {len(scensus)}, SAT necklaces {len(ssat)} (primitive {len(ssat_p)}), complete={complete}, time {tt:.1f}s')
print('in census not SAT:',sorted(scensus-ssat_p)[:5])
print('in SAT not census:',sorted(ssat_p-scensus)[:5])
print('CROSS', 'PASS' if scensus==ssat_p else 'FAIL', flush=True)

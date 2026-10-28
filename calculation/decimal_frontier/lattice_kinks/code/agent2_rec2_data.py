#!/usr/bin/env python3
"""Emit column-major rec2 rows for agent-2's exact stationary transfer.
Run from repository root; redirect stdout to a temporary data file.
"""
from pathlib import Path
src = Path(__file__).resolve().parents[4] / 'calculation/decimal_frontier/lattice_kinks/data/lat2.txt'
z = list(map(int,src.read_text().split()))
p,nb,m,b=z[:4]
assert (p,nb,m,b)==(8,11,48,10)
gam=z[4:4+p];assert gam==[1,0,1,0,1,0,1,0]
o=4+p
W=[z[o+t*m:o+(t+1)*m] for t in range(p)];o+=p*m
cup=[z[o+t*m:o+(t+1)*m] for t in range(p)];o+=p*m
B=[z[o+t*nb:o+(t+1)*nb] for t in range(p)]
assert len(z)==o+p*nb
for t in range(p):
    a=[0]*m;d=[0]*m
    for _ in range(5):
        for j in range(m):a[(j+1)%m]=int(W[t][j]+a[j]>=b)
    for _ in range(5):
        for j in range(m-1,-1,-1):d[j]=int(W[t][(j+1)%m]+d[(j+1)%m]>=b)
    assert a==cup[t]
    for j in range(m):
        ip=(j-1)%m
        v=(W[t][j]+a[j])%b+((W[t][ip]+d[ip])%b if gam[t] else (W[t][j]+d[j])%b)
        assert v==W[(t+1)%p][j]
for j in range(m):print(*(W[t][j] for t in range(p)))
for j in range(nb):print(*(B[t][j] for t in range(p)))
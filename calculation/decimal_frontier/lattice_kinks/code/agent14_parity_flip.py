#!/usr/bin/env python3
"""Exact parity-changing coefficient-complement alignment for four known decimal lattices.
Run from repo root: python3 calculation/decimal_frontier/lattice_kinks/code/agent14_parity_flip.py
"""
import re
from math import gcd
from pathlib import Path
ROOT=Path.cwd()
def cols(s):
    return [tuple(map(int, x.split(','))) for x in re.findall(r'\[([0-9,]+)\]',s)]
def load():
    rows=[]
    f=ROOT/'calculation/decimal_frontier/lattice_formats/p8_scc.txt'
    for k,line in enumerate(x for x in f.read_text().splitlines() if x.startswith('SCC p=')):
        z=re.fullmatch(r'SCC p=(\d+) g=([01]+) size=(\d+) cyclen=(\d+) depth=(\d+) path=(.*?) cyc=(.*)',line)
        assert z
        p,g,_,m,_,path,cyc=z.groups();p=int(p);m=int(m)
        v=cols(cyc)
        assert len(v)==m and all(len(col)==p for col in v)
        rows.append((f'p8-rec{k}',tuple(map(int,g)),tuple(tuple(c[t] for c in v) for t in range(p))))
    assert len(rows)==3
    s=(ROOT/'calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt').read_text().splitlines()
    p,nb,m,b=map(int,s[0].split());assert b==10
    rows.append(('p12-m9',tuple(map(int,s[1].split())),tuple(tuple(map(int,x.split())) for x in s[2:2+p])))
    for name,g,W in rows:
        assert len(W)==len(g) and all(len(w)==len(W[0]) for w in W)
        assert all(0<=x<=18 for w in W for x in w)
    return rows
def classify(g,W):
    p,m=len(g),len(W[0])
    L=p*(2*m//gcd(2*m,sum(g)))
    C=[]
    for w in W:
        c=0
        for x in w:c=int(x+c>=10)
        start=c;v=[]
        for x in w:
            v.append(c);c=int(x+c>=10)
        assert c==start
        C.append(v)
    eligible=[0,0];minimum=[m+1,m+1];matches=[]
    for t in range(p):
        growth=0
        for d in range(1,L+1):
            growth+=g[(t+d-1)%p]
            if growth%2==0:continue
            for parity in (0,1):
                delta=(growth+1-parity)//2
                misses=sum(W[(t+d)%p][(j+delta)%m]!=18-W[t][j] for j in range(m))
                eligible[parity]+=1
                minimum[parity]=min(minimum[parity],misses)
                if misses==0:
                    assert all(C[t][j]+C[(t+d)%p][(j+delta)%m]==1 for j in range(m))
                    assert all(g[i]==g[(i+d)%p] for i in range(p))
                    matches.append((t,parity,d,growth,delta%m))
    return L,eligible,minimum,matches
expected={
 'p8-rec0':{(t,0,18,9,5) for t in range(8)}|{(t,1,62,31,15) for t in range(8)},
 'p8-rec1':{(t,0,18,9,5) for t in range(8)}|{(t,1,62,31,15) for t in range(8)},
 'p8-rec2':set(),'p12-m9':set()
}
for name,g,W in load():
    L,eligible,minimum,matches=classify(g,W)
    assert set(matches)==expected[name] and len(matches)==len(expected[name])
    print(name,'L=',L,'eligible_by_parity=',eligible,'least_mismatches=',minimum,'alignments=',sorted(matches))
print('ALL PARITY-FLIP CLASSIFICATION CHECKS PASSED')

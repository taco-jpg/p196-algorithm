#!/usr/bin/env python3
"""Constructive all-width modulo-3/9/11 charge saturation for decimal rec0/rec1.
Run from repo root: python3 calculation/decimal_frontier/lattice_kinks/code/agent14_charge_saturation.py
"""
import re
from pathlib import Path
def witness(a,b,c):
    r=(b-a)%3
    s=18+(4*(b+3*r))%9
    assert 18<=s<=26
    for u in range(s-18,19):
        v=s-u
        if (2*u-2*v+2*r)%11==c:
            assert (u+v+2*r)%3==a
            assert (-2*u-2*v-3*r)%9==b
            return u,v,r
    raise AssertionError((a,b,c))
def load():
    raw=Path('calculation/decimal_frontier/lattice_formats/p8_scc.txt').read_text()
    for idx,line in enumerate(x for x in raw.splitlines() if x.startswith('SCC p=8')):
        z=re.fullmatch(r'SCC p=8 g=([01]+) size=(\d+) cyclen=(\d+) depth=(\d+) path=(.*?) cyc=(.*)',line)
        assert z
        g,size,m,depth,path,cyc=z.groups()
        if idx>=2:break
        def groups(s):return [[int(y) for y in x.split(',')] for x in re.findall(r'\[([0-9,]+)\]',s)]
        P=groups(path);W=groups(cyc)
        assert len(P)==39 and len(W)==20
        B=[[P[j][t] for j in range(39)] for t in range(8)]
        Q=[[W[j][t] for j in range(20)] for t in range(8)]
        yield idx,B,Q
def full_pair(left,n):
    assert len(left)==(n+1)//2
    return left+list(reversed(left[:-1] if n%2 else left))
def physical_controls():
    count=0
    for idx,B,W in load():
        def coeff(t,j):return B[t%8][j] if j<39 else W[t%8][(j-39)%20]
        for t in range(8):
            for n0 in (400,402,404,406):
                h0=n0//2;n1=n0+9;h1=(n1+1)//2
                for w in range(3,23):
                    x0=[coeff(t,j) for j in range(h0-w)]
                    x1=[coeff(t+18,j) for j in range(h1-w)]
                    sign=1 if (h1-1)%2==0 else -1
                    baseline=full_pair(x1+[18]*w,n1)
                    alt=sum((1 if j%2==0 else -1)*p for j,p in enumerate(baseline))
                    a=(-sum(x0))%3
                    b=(sum(x0)-sum(x1))%9
                    c=(sign*alt)%11
                    u,v,r=witness(a,b,c)
                    C=[0]*(w-3)+[u,v,2*r]
                    P0=full_pair(x0+C,n0)
                    P18=full_pair(x1+[18-q for q in C],n1)
                    assert P0==P0[::-1] and P18==P18[::-1] and P18[n1//2]%2==0
                    s0=sum(P0)//2;s18=sum(P18)//2
                    assert s0%3==0 and (s18-s0)%9==0
                    assert sum((1 if i%2==0 else -1)*x for i,x in enumerate(P18))%11==0
                    count+=1
    assert count==1280,count
    return count
if __name__=='__main__':
    seen=set()
    for a in range(3):
        for b in range(9):
            for c in range(11):
                u,v,r=witness(a,b,c)
                seen.add(((u+v+2*r)%3,(-2*u-2*v-3*r)%9,(2*u-2*v+2*r)%11))
    assert len(seen)==297
    print('SURJECTIVE MODULAR MAP: 297/297 residues (constructive proof)')
    print('DIRECT REAL-LATTICE PAIRWORD CONTROLS:',physical_controls(),'successful phase/length/width cases')
    print('ALL THREE-COEFFICIENT CHARGE CHECKS PASSED')

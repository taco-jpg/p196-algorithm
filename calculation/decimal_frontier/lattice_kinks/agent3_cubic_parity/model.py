#!/usr/bin/env python3
"""Cyclic decimal rec2 pair-word model; square-free degree <=3 local features."""
from itertools import combinations
from pathlib import Path
ROOT=Path(__file__).resolve().parent
raw=[int(x) for x in (ROOT/'lat2.txt').read_text().split()]
assert raw[:12]==[8,11,48,10,1,0,1,0,1,0,1,0]
raw=raw[12:]
W=[raw[48*t:48*(t+1)] for t in range(8)]
MONOMS=[()]+[(i,) for i in range(6)]+list(combinations(range(6),2))+list(combinations(range(6),3))
assert len(MONOMS)==42
NUM=len(MONOMS)

def carries(P):
    n=len(P);asc=[];desc=[]
    assert n>0 and all(0<=x<=18 for x in P) and any(x!=9 for x in P)
    for seed in (0,1):
        a=[seed]
        for x in P:a.append(int(x+a[-1]>=10))
        if a[-1]==seed:asc.append(a[:-1])
        d=[0]*n;d[-1]=seed
        for j in range(n-1,0,-1):d[j-1]=int(P[j]+d[j]>=10)
        if seed==int(P[0]+d[0]>=10):desc.append(d)
    assert len(asc)==len(desc)==1
    return asc[0],desc[0]

def step(P,g):
    a,d=carries(P);n=len(P)
    if g==0:
        out=[2*P[j]+a[j]+d[j]-10*(a[(j+1)%n]+d[(j-1)%n]) for j in range(n)]
    else:
        out=[P[j]+P[(j-1)%n]+a[j]+d[(j-1)%n]-10*(a[(j+1)%n]+d[(j-2)%n]) for j in range(n)]
    assert all(0<=x<=18 for x in out)
    return out

def local_feature(bits):
    return sum((1<<k) for k,mon in enumerate(MONOMS) if all(bits[i] for i in mon))

def features(P):
    a,d=carries(P);n=len(P);total=0
    for j in range(n):
        k=(j+1)%n
        total^=local_feature((P[j]&1,P[k]&1,a[j],d[j],a[k],d[k]))
    return total

def covariance(t,P):
    out=features(step(P,1-t%2))<<(NUM*((t+1)%8))
    if t%2==0:out^=features(P)<<(NUM*t)
    return out

def tags():
    for t in range(8):
        yield (t,-1,0,0)
        for j in range(48):
            for s in (-1,1):
                if 0<=W[t][j]+s<=18:yield (t,j,s,0)
        for j in range(48):
            for s in (-1,1):
                for u in (-1,1):
                    if 0<=W[t][j]+s<=18 and 0<=W[t][(j+1)%48]+u<=18:
                        yield (t,j,s,u)

def test_row(tag):
    t,j,s,u=tag;P=W[t].copy()
    if j>=0:
        P[j]+=s
        if u:P[(j+1)%48]+=u
    return covariance(t,P)

def rank(vectors):
    piv={}
    for v in vectors:
        while v:
            k=v.bit_length()-1
            if k not in piv:piv[k]=v;break
            v^=piv[k]
    return len(piv)

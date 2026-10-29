#!/usr/bin/env python3
"""Exact six-bit cubic rec2 cyclic-bulk parity feature model. Standard library."""
from itertools import combinations
from pathlib import Path
RAW=list(map(int,Path(__file__).with_name('lat2.txt').read_text().split()))
assert RAW[:4]==[8,11,48,10] and RAW[4:12]==[1,0]*4
Z=RAW[12:]; assert len(Z)==8*(48+48+11)
W=[Z[t*48:(t+1)*48] for t in range(8)]
MON=[()] + [(i,) for i in range(6)] + list(combinations(range(6),2)) + list(combinations(range(6),3))
assert len(MON)==42
N=42

def carries(P):
    n=len(P);u=[];d=[]
    for seed in (0,1):
        a=[seed]
        for p in P:a.append(int(p+a[-1]>=10))
        if a[-1]==seed:u.append(a[:-1])
        z=[0]*n;z[-1]=seed
        for j in range(n-1,0,-1):z[j-1]=int(P[j]+z[j]>=10)
        if seed==int(P[0]+z[0]>=10):d.append(z)
    assert len(u)==len(d)==1
    return u[0],d[0]

def step(P,g):
    a,d=carries(P);n=len(P)
    if g==0:return [2*P[j]+a[j]+d[j]-10*(a[(j+1)%n]+d[(j-1)%n]) for j in range(n)]
    return [P[j]+P[(j-1)%n]+a[j]+d[(j-1)%n]-10*(a[(j+1)%n]+d[(j-2)%n]) for j in range(n)]

def edge_feature(x):
    return sum(1<<i for i,inds in enumerate(MON) if all(x[k] for k in inds))

def features(P):
    a,d=carries(P);f=0;n=len(P)
    for j in range(n):
        k=(j+1)%n
        f^=edge_feature((P[j]&1,P[k]&1,a[j],d[j],a[k],d[k]))
    return f

def covariance(t,P):
    r=features(step(P,1-t%2))<<(N*((t+1)%8))
    if t%2==0:r^=features(P)<<(N*t)
    return r

def tags():
    for t in range(8):
        yield (t,-1,0,0)
        for j in range(48):
            for s in (-1,1):
                if 0<=W[t][j]+s<=18:yield (t,j,s,0)
        for j in range(48):
            for s in (-1,1):
                for u in (-1,1):
                    if 0<=W[t][j]+s<=18 and 0<=W[t][(j+1)%48]+u<=18:yield (t,j,s,u)

def test_row(tag):
    t,j,s,u=tag;P=W[t].copy()
    if j>=0:
        P[j]+=s
        if u:P[(j+1)%48]+=u
    return covariance(t,P)

def add(piv,v):
    while v:
        k=v.bit_length()-1
        if k in piv:v^=piv[k]
        else:piv[k]=v;return True
    return False

def rank(vectors):
    p={}
    for v in vectors:add(p,v)
    return len(p)

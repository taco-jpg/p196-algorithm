#!/usr/bin/env python3
"""Independent cyclic modulo-normalization, with random positive control checks."""
from pathlib import Path
from random import Random
from math import gcd
import sys
def check(path):
    raw=[int(x) for x in Path(path).read_text().split()]
    assert tuple(raw[:4])==(8,11,48,10)
    rest=raw[12:];W=[rest[i*48:(i+1)*48] for i in range(8)]
    def cyclic_carries(P):
        m=len(P);upward=[];downward=[]
        for start in (0,1):
            c=start;v=[]
            for p in P:v.append(c);c=(p+c)//10
            if c==start:upward.append(v)
        for final in (0,1):
            c=final;v=[0]*m
            for i in range(m-1,-1,-1):
                v[i]=c;c=(P[i]+c)//10
            if c==final:downward.append(v)
        assert len(upward)==len(downward)==1
        return upward[0],downward[0]
    def iterate(P,g):
        a,d=cyclic_carries(P);m=len(P)
        low=[(P[i]+a[i])%10 for i in range(m)]
        high=[(P[i]+d[i])%10 for i in range(m)]
        return [low[i]+high[i] if not g else low[i]+high[(i-1)%m] for i in range(m)]
    def E(P,g):
        T=iterate(P,g);_,d=cyclic_carries(P);_,dn=cyclic_carries(T)
        z=11 if g else 2
        return sum(10**i*(T[i]-z*P[i]) for i in range(48)),[10**i*(dn[i]-z*d[i]) for i in range(48)]
    for t in range(8):assert iterate(W[t],1-t%2)==W[(t+1)%8]
    def delta(t,i):
        C,K=E(W[t],1-t%2);new=W[t].copy();new[i]+=1
        Y,V=E(new,1-t%2)
        return Y-C,[x-y for x,y in zip(V,K)]
    x,dx=delta(0,47);y,dy=delta(0,2);z,dz=delta(1,2)
    assert x==1-10**48 and dx==[0]*48
    assert y==0 and dy[1]==10 and all(v==0 for j,v in enumerate(dy) if j!=1)
    assert z==-990 and dz[1]==-30 and all(v==0 for j,v in enumerate(dz) if j!=1)
    assert gcd(10**48-1,990)==99
    rng=Random(19637)
    for _ in range(1200):
        P=[rng.randrange(19) for _ in range(48)]
        for g in (0,1):
            new=iterate(P,g)
            q=lambda row,M:sum(pow(10,i,M)*x for i,x in enumerate(row))%M
            for M in (3,9,11,33,99):
                assert q(new,M)==(11 if g else 2)*q(P,M)%M
    print("INDEPENDENT PASS: modulo-normalized row-map witness, gcd 99, 2400 random cyclic control steps in M=3,9,11,33,99")
if __name__=="__main__":
    check(sys.argv[1] if len(sys.argv)>1 else str(Path(__file__).with_name("lat2.txt")))

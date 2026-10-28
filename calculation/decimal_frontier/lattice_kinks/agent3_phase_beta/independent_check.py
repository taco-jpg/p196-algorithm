#!/usr/bin/env python3
"""Independent digit-normalization replay and modular finite-control tester."""
from pathlib import Path
from math import gcd
from random import Random
import sys

def run(path):
    data=[int(x) for x in Path(path).read_text().split()]
    assert data[:4]==[8,11,48,10] and data[4:12]==[1,0]*4
    z=data[12:]
    W=[z[t*48:(t+1)*48] for t in range(8)]
    def carry(P):
        n=len(P);A=[];D=[]
        for s in (0,1):
            a=s;lst=[]
            for p in P:lst.append(a);a=(p+a)//10
            if a==s:A.append(lst)
            d=s;lst=[0]*n
            for j in range(n-1,-1,-1):lst[j]=d;d=(P[j]+d)//10
            if d==s:D.append(lst)
        assert len(A)==len(D)==1
        return A[0],D[0]
    def evolve(P,g):
        U,D=carry(P);n=len(P)
        a=[(P[i]+U[i])%10 for i in range(n)]
        d=[(P[i]+D[i])%10 for i in range(n)]
        return [a[j]+d[(j-g)%n] for j in range(n)]
    def variations(t,j,s):
        A=11 if t%2==0 else 2
        P=W[t].copy();T=evolve(P,1-t%2);_,dp=carry(P);_,dt=carry(T)
        P[j]+=s;S=evolve(P,1-t%2);_,ep=carry(P);_,et=carry(S)
        expr={}
        def add(k,v):expr[k]=expr.get(k,0)+v
        add(('b',(t+1)%8),sum(10**k*(S[k]-T[k]) for k in range(48)))
        add(('b',t),-A*s*10**j)
        for k in range(48):
            if et[k]!=dt[k]:add(('a',(t+1)%8,k),10**k*(et[k]-dt[k]))
            if ep[k]!=dp[k]:add(('a',t,k),-A*10**k*(ep[k]-dp[k]))
        return {k:v for k,v in expr.items() if v}
    for t in range(8):assert evolve(W[t],1-t%2)==W[(t+1)%8]
    for t in range(4):
        e=variations(t,0,-1);A=11 if t%2==0 else 2
        assert e=={('b',t):A,('b',(t+1)%8):-A}
    assert variations(0,47,1)=={('b',0):-11*10**47,('b',1):10**47+1}
    assert variations(2,5,1)=={('b',2):-11*10**5,('b',3):11*10**5,('a',3,4):10**4}
    assert variations(3,5,1)=={('b',3):-2*10**5,('b',4):-79*10**4,('a',3,4):-2*10**4}
    assert gcd(10**48-1,99*10**4)==99
    rng=Random(319648)
    for _ in range(1200):
        P=[rng.randrange(19) for _ in range(48)]
        for g in (0,1):
            N=evolve(P,g)
            for mod in (3,9,11,33,99):
                q=lambda row:sum(pow(10,j,mod)*row[j] for j in range(48))%mod
                assert q(N)==(11 if g else 2)*q(P)%mod
    print('INDEPENDENT PASS: digit-normalized 7 perturbation witnesses and 2400 random cyclic bulk updates')
if __name__=='__main__':run(sys.argv[1] if len(sys.argv)>1 else str(Path(__file__).with_name('lat2.txt')))

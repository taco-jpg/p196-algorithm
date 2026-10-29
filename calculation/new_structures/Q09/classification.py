#!/usr/bin/env python3
"""Q09 independent exact checks of the column-normalizer centralizer.
Run: python3 calculation/new_structures/Q09/classification.py
Only local algebraic checks, not a decimal Lychrel certificate.
"""
from random import Random

def T(b,p,c): return (p+c)%b,(p+c)//b
def norm(b,P,c):
    out=[]
    for p in P:
        d,c=T(b,p,c);out.append(d)
    return out,c
def test(b):
    for flip in (0,1):
        a=lambda p:2*b-2-p if flip else p
        d=lambda r:b-1-r if flip else r
        k=lambda c:1-c if flip else c
        assert sorted(a(p) for p in range(2*b-1))==list(range(2*b-1))
        for p in range(2*b-1):
            for c in (0,1):
                y,co=T(b,p,c)
                assert T(b,a(p),k(c))==(d(y),k(co))
    print("COLUMN",b,"two automorphisms PASS")
r=Random(909474)
for b in (2,9,10,50):test(b)
for b in (9,10,50):
    for m in (20,40,80,160):
        for _ in range(100):
            P=[r.randrange(2*b-1) for i in range(m)]
            c=r.randrange(2)
            ds,co=norm(b,P,c)
            dual,co2=norm(b,[2*b-2-p for p in P],1-c)
            assert dual==[b-1-d for d in ds] and co2==1-co
        print("WORD",b,m,"100 cases PASS")

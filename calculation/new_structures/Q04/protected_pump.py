#!/usr/bin/env python3
"""Exact all-length protected-prefix pumping. Run from repository root."""
from pathlib import Path
from random import Random

FIXTURE=Path("calculation/decimal_frontier/lattice_kinks/data/lat2.txt")

def rec2():
    r=[list(map(int,s.split())) for s in FIXTURE.read_text().splitlines()]
    assert len(r)==26 and r[0]==[8,11,48,10]
    assert len(r[1])==8 and all(len(x)==48 for x in r[2:18])
    assert all(len(x)==11 for x in r[18:])
    return r[1],r[2:10],r[18:26]

def protected(b,B,W,m,u):
    """Folded prefix of B W^m C reverse(W)^m reverse(B), conditional on
    the real carry u leaving C towards the upper reflected band."""
    assert b>=2 and m>=1 and u in (0,1) and B and W
    assert all(0<=x<=2*b-2 for x in B+W)
    H=B+W*m
    low=[0]
    for x in H: low.append((x+low[-1])//b)
    high=[0]*(len(H)+1); high[-1]=u
    for i in range(len(H)-1,-1,-1):
        high[i]=(H[i]+high[i+1])//b
    gamma=high[0]
    a=[(x+low[i])%b for i,x in enumerate(H)]
    d=[(x+high[i+1])%b for i,x in enumerate(H)]
    return gamma,[a[i]+(d[i] if gamma==0 else (1 if i==0 else d[i-1]))
                  for i in range(len(H))]

def pump(b,B,W,u):
    """Proof of all-m decomposition in reports/Q04BandPortPumping.md."""
    v=len(B);w=len(W)
    g2,p2=protected(b,B,W,2,u)
    g3,p3=protected(b,B,W,3,u)
    assert g2==g3
    A=p2[:v]; X=p2[v:v+w]; Z=p2[v+w:]
    Y=p3[v+w:v+2*w]
    assert p2==A+X+Z and p3==A+X+Y+Z
    return g2,A,X,Y,Z

def tests():
    rng=Random(20261028)
    for b in (3,4,9,10,13,50):
        for _ in range(4000):
            B=[rng.randrange(1,2*b-1)]+[rng.randrange(2*b-1) for _ in range(rng.randrange(5))]
            W=[rng.randrange(2*b-1) for _ in range(rng.randrange(1,8))]
            u=rng.randrange(2)
            gamma,A,X,Y,Z=pump(b,B,W,u)
            for m in range(1,13):
                g,p=protected(b,B,W,m,u)
                assert g==gamma
                if m>=2:assert p==A+X+Y*(m-2)+Z
    print("PASS 24,000 random all-m decompositions, 12 sampled widths")
    g,W,B=rec2()
    gates=((0,1),(0,),(0,1),(1,),(0,1),(1,),(0,1),(1,))
    for t in range(8):
        admissible=[]
        for u in (0,1):
            gamma,A,X,Y,Z=pump(10,B[t],W[t],u)
            assert gamma==g[t]
            nb=B[(t+1)%8];nw=W[(t+1)%8]
            v1=protected(10,B[t],W[t],1,u)[1]==nb+nw
            v2=A+X+Z==nb+nw*2
            v3=A+X+Y+Z==nb+nw*3
            assert v1==v2==v3,(t,u)
            for m in (4,5,20,40,80,160):
                gm,out=protected(10,B[t],W[t],m,u)
                assert gm==gamma and out==A+X+Y*(m-2)+Z
                assert (out==nb+nw*m)==v2
            if v1:admissible.append(u)
        assert tuple(admissible)==gates[t]
    print("PASS rec2 all-exponent gates:",gates)
    print("Necessary odd-phase carries:",(0,1,1,1))

if __name__=="__main__":tests()

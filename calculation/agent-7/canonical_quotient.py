#!/usr/bin/env python3
"""Independent exact all-trim versus deterministic quotient audit (Agent 7).

This is a finite test, not a Lean theorem or a decimal certificate.
Run: python3 calculation/agent-7/canonical_quotient.py
"""
from itertools import product
from collections import Counter

def norm(b, w, carry):
    out = []
    for z in w:
        out.append((z+carry)%b)
        carry = (z+carry)//b
    return out, carry

def raw(b, B, C):
    h = b-1
    db,e = norm(b,B,0)
    dc,f = norm(b,C,e)
    dr,g = norm(b,B[::-1],f)
    x,y = h*(1-e), h*(1-f)
    nB = ([a+c for a,c in zip(db+[x],[1]+dr[::-1])]
          if g else [a+c for a,c in zip(db,dr[::-1])])
    w = dc+[y] if g else dc
    nC = [a+c for a,c in zip(w,w[::-1])]
    return e,f,g,nB,nC

def canonical_center(b,c):
    h=b-1
    while len(c)>=2 and c[0]==h and c[-1]==h:
        c=c[1:-1]
    return c

def canonical(b,B,C):
    h=b-1
    while B and B[-1]==h:
        B=B[:-1]
    return B, canonical_center(b,C)

def legal(b,B,C):
    if B and B[0]==0:return False
    if any(not 0<=z<=2*(b-1) for z in B+C):return False
    e,f,_,_,_=raw(b,B,C)
    return e!=f

def successors_all(b,B,C):
    h=b-1
    _,_,_,nB,nC=raw(b,B,C)
    for u in range(len(nB)+1):
        if u and nB[-u:] != [h]*u:continue
        TB=nB[:-u] if u else nB
        for v in range(len(nC)//2+1):
            if v and (nC[:v]!=[h]*v or nC[-v:]!=[h]*v):continue
            TC=nC[v:len(nC)-v] if v else nC
            if legal(b,TB,TC):
                yield TB,TC,u,v

def test_small():
    counts=Counter()
    for b in range(2,6):
        h=b-1
        for n in range(3):
            for bp in product(range(2*h+1),repeat=n):
                B=list(bp)
                for m in range(1,5):
                    for half in product(range(2*h+1),repeat=(m+1)//2):
                        C=list(half)+list(half[:m//2][::-1])
                        if not legal(b,B,C):continue
                        cb,cc=canonical(b,B,C)
                        _,_,_,nb,nc=raw(b,cb,cc)
                        expected=canonical(b,nb,nc)
                        for B2,C2,u,v in successors_all(b,B,C):
                            assert canonical(b,B2,C2)==expected,(b,B,C,B2,C2)
                            counts['edges']+=1
                            if u+v:counts['nonzero_trims']+=1
                        counts['sources']+=1
    assert counts=={'sources':10564,'edges':11222,'nonzero_trims':2830},counts
    print('All-trim quotient: PASSED sources=10564 edges=11222 nonzero_trims=2830')

def test_cert26():
    # Coefficients from previously Lean-checked Agent213.KnownBases.cert26.
    b=26
    B0=[24,28,19,36,30,15,19,12]
    B1=[49,4,40,21,9,31,38,25]
    C0=[32,20,20,32]
    C1=[12,41,41,12]
    C2=[38,28,32,28,38]
    C3=[25,6,14,6,25]
    states=[(B0,C0),(B1,C1),(B0,C2),(B1,C3)]
    phases=[]
    for i,(B,C) in enumerate(states):
        E,D=canonical(b,B,C)
        _,_,g,nb,nc=raw(b,E,D)
        nxt=canonical(b,nb,nc)
        assert nxt==canonical(b,*states[(i+1)%4])
        u=len(nb)-len(nxt[0])
        v=(len(nc)-len(nxt[1]))//2
        assert g==0 or (u==0 and v==0)
        phases.append((g,u,v))
    assert phases==[(0,1,0),(1,0,0),(0,1,1),(1,0,0)]
    print('Base26 published Lean-source positive control: PASSED',phases)

if __name__=='__main__':
    test_small()
    test_cert26()

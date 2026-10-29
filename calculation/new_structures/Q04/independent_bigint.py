#!/usr/bin/env python3
"""Independent genuine big-integer reverse-and-add; no port-model imports."""
from pathlib import Path
from random import Random
import json,re,sys
sys.set_int_max_str_digits(0)

def digits(n,b):
    a=[]
    while n:a.append(n%b);n//=b
    return a

def pairs(n,b):
    d=digits(n,b)
    return [d[i]+d[-i-1] for i in range(len(d))]

def step(n,b):
    d=digits(n,b)
    return n+sum(x*b**i for i,x in enumerate(d[::-1]))

def from_pairs(P,b):
    assert P==P[::-1] and P[0]>0
    h=len(P)//2
    upper=[min(b-1,x) for x in P[:h]]
    lower=[P[i]-upper[i] for i in range(h)]
    mid=[] if len(P)%2==0 else [P[h]//2]
    assert len(P)%2==0 or P[h]%2==0
    assert all(0<=x<b for x in upper+lower+mid)
    n=0
    for x in upper+mid+lower[::-1]:n=b*n+x
    return n

def controls():
    src=Path("lean/P196/LatticeBand/Base9.lean").read_text()
    def datum(k):
        m=re.search(r"def "+k+r" : List Nat := \[([^]]+)\]",src)
        assert m,k
        return [int(x.strip()) for x in m.group(1).split(",")]
    B=datum("B0");W=datum("W0")
    for L in (10,22,42,82,162,322):
        P=B+(W*((L+len(W)-1)//len(W)))[:L]+B[::-1]
        n=from_pairs(P,9)
        for _ in range(10):
            d=digits(n,9);assert d!=d[::-1]
            n=step(n,9)
        Q=B+(W*((L+4+len(W)-1)//len(W)))[:L+4]+B[::-1]
        assert pairs(n,9)==Q
    info=json.loads(Path("calculation/neutral_band/agent10_base50/cert_b50.json").read_text())
    B=info["edges"][0]["B"];C=info["edges"][0]["C"]
    for L in (12,20,40,80,160):
        n=from_pairs(B+[49]*L+C+[49]*L+B[::-1],50)
        for _ in range(4):
            d=digits(n,50);assert d!=d[::-1]
            n=step(n,50)
        assert pairs(n,50)==B+[49]*(L+1)+C+[49]*(L+1)+B[::-1]
    print("PASS independent base-9 Lean-certified +4 and base-50 +1 controls")

def decimal():
    r=[list(map(int,s.split())) for s in Path("calculation/decimal_frontier/lattice_kinks/data/lat2.txt").read_text().splitlines()]
    g,W,B=r[1],r[2:10],r[18:26]
    gate=((0,1),(0,),(0,1),(1,),(0,1),(1,),(0,1),(1,))
    rng=Random(404)
    count={(t,u):0 for t in range(8) for u in (0,1)}
    for t in range(8):
        for m in (1,2,3,5,20,40,80,160):
            for j in range(10):
                H=B[t]+W[t]*m
                a=[rng.randrange(19) for _ in range(j%4)]
                C=a+([2*rng.randrange(10)] if j%2==0 else [])+a[::-1]
                P=H+C+H[::-1]
                n=from_pairs(P,10)
                d=digits(n,10)
                carry=0
                # Genuine carry out of C into the reflected upper band.
                for i in range(len(H)+len(C)):
                    carry=(d[i]+d[-1-i]+carry)//10
                nxt=step(n,10)
                Q=pairs(nxt,10)
                assert len(Q)==len(P)+g[t],("overflow",t,m,j)
                good=Q[:len(H)]==B[(t+1)%8]+W[(t+1)%8]*m
                assert good==(carry in gate[t]),(t,m,j,carry)
                count[(t,carry)]+=1
    assert all(count.values())
    print("PASS 640 genuine decimal integer steps, both seam carries at all phases")
    print(count)

if __name__=="__main__":controls();decimal()

#!/usr/bin/env python3
"""Standalone mod-(base-1) neutral-band center constraint audit (not certificate)."""
import argparse
import random

def norm(b,w,c):
    d=[]
    for a in w:
        z=a+c
        d.append(z%b)
        c=z//b
    return d,c

def one_step(b,B,C):
    D,e=norm(b,B,0)
    T,e2=norm(b,C,e)
    R,g=norm(b,B[::-1],e2)
    if e==e2: return None
    if g:
        NB=[x+y for x,y in zip(D+[(b-1)*(1-e)],[1]+R[::-1])]
        t=(b-1)*(1-e2)
        NC=[x+y for x,y in zip(T+[t],[t]+T[::-1])]
    else:
        NB=[x+y for x,y in zip(D,R[::-1])]
        NC=[x+y for x,y in zip(T,T[::-1])]
    while NB and NB[-1]==b-1: NB.pop()
    while len(NC)>=2 and NC[0]==NC[-1]==b-1: NC=NC[1:-1]
    return NB,NC,e,g

def affine(stream,b=10,k=1):
    assert b>=3 and stream and k>=1 and set(stream)<=set("01")
    a,q=1,0
    for bit in stream*k:
        a,q=(2*a)%(b-1),(2*q+4*int(bit)-2)%(b-1)
    return a,q

def residues(stream,b=10,k=1):
    a,q=affine(stream,b,k)
    return [s for s in range(b-1) if (a*s+q-s)%(b-1)==0]

def census(p,b=10):
    mod=b-1
    dp=[0]*mod
    dp[0]=1
    for t in range(p):
        w=pow(2,p-t-1,mod)
        nxt=[0]*mod
        for q,n in enumerate(dp):
            if n:
                nxt[(q-2*w)%mod]+=n
                nxt[(q+2*w)%mod]+=n
        dp=nxt
    viable={(1-pow(2,p,mod))*s%mod for s in range(mod)}
    return sum(dp[q] for q in viable),2**p

def selftest():
    rng=random.Random(128)
    n=0
    for b in (3,4,7,10,11,17,26):
        for j in range(15000):
            B=[rng.randrange(1,2*b-1)]+[rng.randrange(2*b-1) for _ in range(rng.randrange(6))]
            half=[rng.randrange(2*b-1) for _ in range(rng.randrange(1,5))]
            C=half+half[::-1] if rng.randrange(2) else half+[rng.randrange(2*b-1)]+half[::-1]
            z=one_step(b,B,C)
            if z is None: continue
            B2,C2,e,g=z
            h=b-1
            assert (sum(B2)-2*sum(B)-1+2*e)%h==0
            assert (sum(C2)-2*sum(C)-4*e+2)%h==0
            assert (sum(C2)+2*sum(B2)-2*(sum(C)+2*sum(B)))%h==0
            n+=1
    for p in range(1,13):
        brute=sum(bool(residues(format(x,"0"+str(p)+"b"))) for x in range(1<<p))
        assert brute==census(p)[0]
    assert residues("10100110011")==[3]
    assert residues("10100110011",k=2)==[0,3,6]
    assert residues("10100110011",k=3)==[3]
    assert len(residues("101010010101"))==9
    print("SELFTEST PASSED",n,"eligible among 105000 trials, bitstream p<=12")

if __name__=="__main__":
    ap=argparse.ArgumentParser(description=__doc__)
    sub=ap.add_subparsers(dest="cmd",required=True)
    c=sub.add_parser("check")
    c.add_argument("e")
    c.add_argument("k",nargs="?",type=int,default=1)
    c=sub.add_parser("census")
    c.add_argument("period",type=int,nargs="+")
    sub.add_parser("selftest")
    args=ap.parse_args()
    if args.cmd=="selftest":selftest()
    if args.cmd=="check":print("affine",affine(args.e,k=args.k),"residues",residues(args.e,k=args.k))
    if args.cmd=="census":
        for p in args.period:print("period",p,"raw e streams",*census(p),"NOT B-cycle count")

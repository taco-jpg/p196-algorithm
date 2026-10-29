#!/usr/bin/env python3
"""Independent Python-bigint controls for the W42 phase-0 cell."""
from collections import Counter
from itertools import product
import argparse, sys
sys.set_int_max_str_digits(100000)

B=[10,4,6,6,7,12,9,16,16,13,0,2,10,17,7,0,18,6,5,18,4,18,14,9,14,8,12,17,10,4,6,4,0,5]
W=[5,18,4,8,1,15,4,0,5]
U=[10,8,9]
EXPECTED={-25:150,-24:317,-23:5807,-22:4945,-21:580,-20:576,-19:37,-18:48,-16:13,-15:9}
NONZERO_C={
    3:[1,2,1],
    5:[0,1,2,1,0],
    7:[0,0,1,2,1,0,0],
    9:[0,0,0,1,2,1,0,0,0],
    11:[0,0,0,0,1,2,1,0,0,0,0],
    13:[0,0,0,0,0,1,2,1,0,0,0,0,0],
}

def alt(xs):
    return sum((1 if i%2==0 else -1)*x for i,x in enumerate(xs))

def admissible_j():
    for n in (3,4):
        for J in product(range(19), repeat=n):
            if alt(J)%11==0:
                yield list(J)

def pairword_template(J,U,C,q,k):
    h=B+W*q+J+U*k
    return h+C+h[::-1]

def realize_pairword(p):
    assert p==p[::-1]
    d=[0]*len(p)
    for i in range(len(p)//2):
        hi=min(9,p[i]);lo=p[i]-hi
        assert 0<=lo<=9
        d[i]=lo;d[-1-i]=hi
    if len(p)%2:
        assert p[len(p)//2]%2==0
        d[len(p)//2]=p[len(p)//2]//2
    assert d[-1]!=0
    return int(''.join(str(x) for x in d[::-1]))

def actual_bigint(J,C,q,k,steps=120):
    n=realize_pairword(pairword_template(J,U,C,q,k))
    gamma=[]
    for _ in range(steps):
        s=str(n)
        nn=n+int(s[::-1])
        gamma.append(len(str(nn))-len(s))
        n=nn
    s=str(n)
    got=[int(s[-1-i])+int(s[i]) for i in range(len(s))]
    target=pairword_template(J,U,C,q,k+5)
    first=next((i for i,(x,y) in enumerate(zip(got,target)) if x!=y),None)
    if first is None and len(got)!=len(target):
        first=min(len(got),len(target))
    cut=len(B)+9*q
    return {
        "first_mismatch":first,
        "offset":None if first is None else first-cut,
        "prefix_preserved":got[:cut]==target[:cut],
        "gamma":"".join(map(str,gamma)),
        "sum_gamma":sum(gamma),
    }

def exhaustive_q20():
    hist=Counter();n=0;passes=0;clockfails=0;sumfails=0
    for J in admissible_j():
        r=actual_bigint(J,[0,0,0],20,20)
        n+=1
        if r["prefix_preserved"]:passes+=1
        if r["gamma"]!="1000"*30:clockfails+=1
        if r["sum_gamma"]!=30:sumfails+=1
        if r["offset"] is not None:hist[r["offset"]]+=1
    assert n==12482
    assert passes==clockfails==sumfails==0
    assert dict(sorted(hist.items()))==EXPECTED,dict(hist)
    print("PYTHON_BIGINT_EXHAUSTIVE q=k=20: J=12482; prefix passes=0; clock failures=0; sum-gamma failures=0")
    print("histogram:",dict(sorted(hist.items())))

def centre_controls():
    examples=[
        ([0,0,0],-22),
        ([11,0,0],-21),
        ([0,0,11],-23),
        ([18,18,18,18],-21),
    ]
    count=0
    for J,expected_offset in examples:
        assert alt(J)%11==0
        for clen in (3,5,7,9,11,13):
            centres=([0]*clen,NONZERO_C[clen])
            for C in centres:
                assert C==C[::-1] and C[len(C)//2]%2==0 and alt(C)%11==0
                for q in (20,40,80,160):
                    r=actual_bigint(J,C,q,q)
                    assert r["offset"]==expected_offset,(J,C,q,r)
                    assert not r["prefix_preserved"]
                    assert r["gamma"]=="1000"*30 and r["sum_gamma"]==30
                    count+=1
    assert count==192
    print("PYTHON_BIGINT_CENTRE_CONTROLS: 192/192 pass (4 J x 6 odd lengths x 2 centre representatives x q=k in 20,40,80,160)")

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--controls-only",action="store_true")
    args=p.parse_args()
    if not args.controls_only: exhaustive_q20()
    centre_controls()

if __name__=="__main__":
    main()

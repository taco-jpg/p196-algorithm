#!/usr/bin/env python3
"""Exact all-k binary last-edge inverse gate; NOT a decimal Lychrel proof."""
import re
from pathlib import Path

data=Path(__file__).with_name("p8_rec0_rows.txt").read_text().splitlines()
B,W=[[tuple(map(int,s.split(","))) for s in re.findall(r"\[([^\]]+)\]",line)] for line in data]
assert len(B)==39 and len(W)==20
B0=tuple(r[0] for r in B);B7=tuple(r[7] for r in B)
W0=tuple(r[0] for r in W);W7=tuple(r[7] for r in W)
A=W7[:17]+(9,)+W7[18:19]+(16,)
assert len(A)==20 and [(i,a,b) for i,(a,b) in enumerate(zip(A,W7)) if a!=b]==[(17,9,14),(19,16,6)]

def inverse_block(lo,ho):
    """Exact transfer inverse over a target W0 and all possible binary carries."""
    states={(lo,ho):[()]}
    for y in W0:
        out={}
        for (l,h),words in states.items():
            for x in range(19):
                for eta in (0,1):
                    q,d=divmod(x+l,10)
                    hp,u=divmod(x+eta,10)
                    if hp==h and d+u==y:
                        out.setdefault((q,eta),[]).extend(w+(x,) for w in words)
        states=out
    return states

def check_all_k():
    tables={(l,h):inverse_block(l,h) for l in (0,1) for h in (0,1)}
    assert tables[(0,0)]=={(1,0):[A],(0,0):[W7]}
    assert tables[(1,0)]=={} and tables[(1,1)]=={}
    D=(18,11,0,6,18,15,6,11,18,10,0,10,3,1,17,5,17,14,3,6)
    assert tables[(0,1)]=={(0,1):[D]}
    print("Exact 4-state 20-column inverse transfer:")
    for s,targets in tables.items():
        print(s,"=>",[(target,list(words[0])) for target,words in targets.items()])
    print("For every k>=1, source state (0,0), target W0^k: only W7^k or W7^(k-1) A.")

def pairword_integer(n):
    d=list(map(int,str(n)[::-1]))
    return tuple(a+b for a,b in zip(d,d[::-1]))

def canonical_integer(P):
    assert len(P)%2==0 and P==P[::-1]
    low=[min(9,x) for x in P[:len(P)//2]]
    high=[x-a for x,a in zip(P[:len(P)//2],low)]
    if high[0]==0:
        low[0]-=1;high[0]+=1
    d=low+high[::-1]
    assert d[-1]>0
    return int("".join(map(str,d[::-1])))

def ordinary_integer_oracle():
    count=0
    for q in (1,2,5,20):
        for k in (1,2,4,8):
            for c in (0,1,2,6,8):
                for end in (W7,A):
                    half=B7+W7*q+W7*(k-1)+end+(c,)*12
                    P=half+half[::-1]
                    n=canonical_integer(P)
                    assert pairword_integer(n)==P
                    nxt=n+int(str(n)[::-1])
                    assert len(str(nxt))==len(str(n))
                    Q=pairword_integer(nxt)
                    assert Q[:len(B0)+20*(q+k)]==B0+W0*(q+k)
                    count+=1
    print("PASS",count,"independent ordinary decimal integer one-step controls")

if __name__=="__main__":
    check_all_k()
    ordinary_integer_oracle()

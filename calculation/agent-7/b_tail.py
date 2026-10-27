#!/usr/bin/env python3
"""Base-10 B suffix neutral conjugacy and trim-site audit; standalone.

Agent 7 / T1.B-tail-normal-form. No imports from the neutral-band mirror.
Run: python3 calculation/agent-7/b_tail.py
"""
from itertools import product
from collections import Counter

def norm(w, inc):
    ds=[]
    for a in w:
        ds.append((a+inc)%10)
        inc=(a+inc)//10
    return ds,inc

def exterior(B):
    db,e=norm(B,0)
    dr,g=norm(B[::-1],1-e)
    assert e in (0,1) and g in (0,1)
    if not g:
        out=[a+b for a,b in zip(db,dr[::-1])]
    else:
        out=[a+b for a,b in zip(db+[9*(1-e)], [1]+dr[::-1])]
    return e,g,out

def tail_carry(B):
    assert B
    return norm(B[:-1],0)[1]

def audit():
    padding=Counter()
    for n in range(4):
        for B in product(range(19),repeat=n):
            # Include B=[]; reject only first digit=0 for nonempty B.
            if B and B[0]==0:continue
            e,g,out=exterior(list(B))
            for a in range(5):
                ep,gp,op=exterior(list(B)+[9]*a)
                assert (ep,gp)==(e,g), (B,a,e,g,ep,gp)
                assert op==out+[9]*a, (B,a,g,out,op)
                padding[n]+=1
    counted=Counter()
    examples={}
    for n in range(5):
        for B in product(range(19),repeat=n):
            if B and B[0]==0:continue
            if B and B[-1]==9:continue # strip maximal 9-suffix first
            e,g,out=exterior(list(B))
            if not out or out[-1]!=9:continue
            counted[(n,e,g)]+=1
            examples.setdefault((n,e,g),B)
            assert not g, (B,e,g,out)
            assert len(B)>0
            assert (e,B[-1],tail_carry(B)) in ((0,4,0),(1,14,1)), (B,e,g,out)
            if len(out)>1 and out[-2]==9:
                assert len(B)>1
                assert B[-2:]==((4,4) if e==0 else (14,14)), (B,e,g,out)
    print('ALL CHECKS PASSED')
    print('padding tests by B length (a=0..4):',dict(sorted(padding.items())))
    print('head-neutral raw B outputs by (length,e,g):',dict(sorted(counted.items())))
    print('examples:',{str(k):v for k,v in examples.items()})

if __name__=='__main__':audit()

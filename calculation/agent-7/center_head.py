#!/usr/bin/env python3
"""Independent exact base-10 one-band center boundary audit (Agent 7, T1).

No imported mirror or solver. Outputs are COMPUTED. The proof is in
reports/agent-7-T1.md; this script does not certify a base-10 Lychrel number.
Run: python3 calculation/agent-7/center_head.py
"""
from itertools import product
from collections import Counter

BASE=10
NEUTRAL=9

def palindromes(n):
    for left in product(range(19), repeat=(n+1)//2):
        yield list(left) + list(left[:n//2][::-1])

def norm(C, inc):
    digs=[]
    for z in C:
        digs.append((z+inc)%10)
        inc=(z+inc)//10
    return digs,inc

def next_center(C, e, gam):
    d, e2=norm(C,e)
    if e2==e:
        raise ValueError('flip condition not met')
    y=9*(1-e2)
    d=d+([y] if gam else [])
    return [a+b for a,b in zip(d,reversed(d))]

def stripped(C):
    assert C and C==C[::-1] and any(v!=9 for v in C)
    a=0
    while C[a]==9:
        a+=1
    return a,C[a:len(C)-a]

def first_raw(c,e,g,t):
    # t: carry into C's most-significant coefficient, derived from the
    # unspecified middle; for length-1 C, the actual t is just e.
    if e==0:
        if c<9 or (c==9 and t!=1): return None
    else:
        if c>9 or (c==9 and t!=0): return None
    lo=(c+e)%10
    hi=(c+t)%10
    return lo+hi if g==0 else lo+9*e

def predicted(e,g,c):
    return any(first_raw(c,e,g,t)==9 for t in (0,1))

def audit():
    states=Counter()
    tested=0
    center_trims=Counter()
    two_trim=Counter()
    for length in range(1,6):
        for C in palindromes(length):
            for e in (0,1):
                _,e2=norm(C,e)
                if e2!=1-e:continue
                a,D=stripped(C)
                for g in (0,1):
                    raw=next_center(C,e,g)
                    raw_base=next_center(D,e,g)
                    for padding in range(4):
                        Cp=[9]*padding+D+[9]*padding
                        assert next_center(Cp,e,g)==[9]*padding+raw_base+[9]*padding
                        assert norm(Cp,e)[1]==norm(D,e)[1]
                    if C[0]!=9:
                        tested+=1
                        x=raw[0]
                        if x==9:
                            assert predicted(e,g,C[0]),(C,e,g,x)
                        # One-sided implication only: predicted() may allow
                        # an incoming high-end carry not realized by this C.
                        if x==9:
                            assert g==0
                            assert (e,C[0]) in ((0,14),(1,4)),(C,e,g,raw)
                            states[(e,g,C[0])]+=1
                            if len(raw)>=4 and raw[:2]==[9,9]:
                                assert len(C)>=4 and C[:2]==([14,14] if e==0 else [4,4]),(C,e,g,raw)
                                two_trim[(e,tuple(C[:2]))]+=1
                            # ensure real symmetric trimming is possible
                            assert raw[-1]==9
                            if len(raw)>2:center_trims[(e,g)]+=1
    assert tested>0
    print('ALL CHECKS PASSED')
    print('canonical-state/gamma pairs tested:',tested)
    print('center first-neutral conditions (e,g,head):',dict(sorted(states.items())))
    print('candidates with 2 neutral pairs at each end:',dict(sorted(two_trim.items())))
    print('actual nonempty one-pair-trim candidates:',dict(sorted(center_trims.items())))

if __name__=='__main__':audit()

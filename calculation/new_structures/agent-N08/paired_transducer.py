#!/usr/bin/env python3
"""Exact finite-state folded palindrome-pair transducer, base >= 2.

Input is (half, centre); centre=None denotes an even full length.
This file also provides *independent digit normalisation* for randomized tests.
"""
from itertools import product
import random

def unfold(half, centre):
    return list(half) + ([] if centre is None else [centre]) + list(reversed(half))

def fold(word):
    assert word==word[::-1]
    n=len(word)
    return tuple(word[:n//2]), (word[n//2] if n%2 else None)

def step_digits(P,b):
    carry=0
    digits=[]
    for p in P:
        v=p+carry
        digits.append(v%b)
        carry=v//b
    if carry:digits.append(carry)
    assert digits[-1]!=0
    return digits,[digits[i]+digits[-1-i] for i in range(len(digits))],carry

def transitions(b,gamma,state,p):
    """State=(lower incoming carry, upper outward carry, preceding upper digit).
    The inward upper carry is guessed in {0,1}; midpoint verifies it.
    """
    low_c,high_out,prev_upper=state
    for high_inner in (0,1):
        if (p+high_inner)//b!=high_out:continue
        low_digit=(p+low_c)%b
        high_digit=(p+high_inner)%b
        out=low_digit+high_digit if gamma==0 else low_digit+(1 if prev_upper<0 else prev_upper)
        yield ((p+low_c)//b,high_inner,high_digit),out

def terminals(b,gamma,state,centre):
    low_c,high_out,prev_upper=state
    if centre is None:
        if low_c!=high_out:return
        if gamma==0:yield ((),None)
        elif prev_upper>=0:yield ((),2*prev_upper)
    else:
        if (centre+low_c)//b!=high_out:return
        middle=(centre+low_c)%b
        if gamma==0:yield ((),2*middle)
        elif prev_upper>=0:yield ((middle+prev_upper,),None)

def enumerate_folds(b,half,centre,gamma):
    paths=[((0,gamma,-1),())]
    for p in half:
        paths=[(state2,output+(v,)) for state,output in paths
               for state2,v in transitions(b,gamma,state,p)]
    return [(output+extra,c2) for state,output in paths
            for extra,c2 in terminals(b,gamma,state,centre)]

def selftest():
    cases=0
    for b,maxn in [(2,10),(3,7),(4,6),(10,4),(13,3)]:
        for n in range(2,maxn+1):
            for h in product(range(2*b-1),repeat=n//2):
                if h[0]==0:continue
                for c in (range(2*b-1) if n%2 else (None,)):
                    digits,P2,gamma=step_digits(unfold(h,c),b)
                    assert enumerate_folds(b,h,c,gamma)==[fold(P2)]
                    assert enumerate_folds(b,h,c,1-gamma)==[]
                    cases+=1
    rng=random.Random(20261028)
    for _ in range(20000):
        b=rng.randint(2,40);n=rng.randint(2,180)
        h=[rng.randrange(1,2*b-1)]+[rng.randrange(2*b-1) for i in range(n//2-1)]
        c=rng.randrange(2*b-1) if n%2 else None
        _,P2,gamma=step_digits(unfold(h,c),b)
        assert enumerate_folds(b,h,c,gamma)==[fold(P2)]
        assert enumerate_folds(b,h,c,1-gamma)==[]
    print("FOLDED_TRANSDUCER_EXHAUSTIVE",cases,"RANDOM",20000,"PASS")

if __name__=="__main__":selftest()

#!/usr/bin/env python3
"""Independent grade-school / integer checks and exhaustive small-radix coverage.
Run from this directory: python3 independent_checks.py
"""
from random import Random
from regular_certificate import (step_pairs,decode_pair,pairs_from_digits,
                                 reverse_add_digits,all_pairs,odd_pairs,discover_bad)

def toint(ds,b):
    a=0
    for x in reversed(ds):a=a*b+x
    return a

def todigits(n,b):
    if not n:return [0]
    v=[]
    while n:v.append(n%b);n//=b
    return v

rng=Random(7007)
count=0
for b in range(2,31):
    for m in range(0,11):
        for z in range(100):
            centre=None if (m and z%2==0) else rng.randrange(b)
            if m==0 and centre==0:centre=1
            P=[rng.randrange(2*b-1) for i in range(m)]
            if P and P[0]==0:P[0]=rng.randint(1,2*b-2)
            ds=decode_pair(P,centre,b)
            assert ds[-1]>0
            # Two independently coded ordinary update implementations.
            n=toint(ds,b); nxt=n+toint(ds[::-1],b)
            digits=todigits(nxt,b)
            check=reverse_add_digits(ds,b)
            assert digits==check,(b,P,centre)
            actual=pairs_from_digits(digits)
            expected=step_pairs(P,centre,b)
            assert actual==(expected[0],expected[1]),(b,P,centre,actual,expected)
            assert len(digits)==len(ds)+expected[2]
            count+=1
    assert discover_bad(all_pairs(b)) is None
    assert discover_bad(odd_pairs(b)) is not None
print('PASS: exact paired transducer vs independent Python int and digit-list',count,'cases, bases 2..30; all-positive DFA closure / odd-witness counterexample all pass')
# Exhaust every source number n of at most four digits in small bases.
exhaustive=0
for b in range(2,9):
    for n in range(1,b**4):
        ds=todigits(n,b)
        P,c=pairs_from_digits(ds)
        out=step_pairs(P,c,b)
        s=todigits(n+toint(ds[::-1],b),b)
        assert (out[0],out[1])==pairs_from_digits(s)
        assert out[2]==len(s)-len(ds)
        exhaustive+=1
print('PASS: exhaustive ordinary integers with up to four digits',exhaustive,'cases, bases 2..8')

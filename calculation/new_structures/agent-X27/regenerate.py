#!/usr/bin/env python3
"""Independent exact integer exhaustive controls for even-base parity regeneration."""
from collections import Counter
from random import Random

def digits(n,b):
    v=[]
    while n:v.append(n%b);n//=b
    return v or [0]

def number(ds,b):
    result=0
    for x in reversed(ds):result=result*b+x
    return result

def check(n,b):
    ds=digits(n,b);m=len(ds)
    ps=[ds[i]+ds[m-1-i] for i in range(m)]
    if any(p&1 for p in ps):return 'odd-input'
    hi=next((i for i in range((m+1)//2) if ps[i]>=b),None)
    step=n+number(ds[::-1],b)
    nd=digits(step,b)
    if hi is None:
        assert nd==nd[::-1],(n,b,ps,'no high yet successor nonpal')
        return 'no-carry-palindrome'
    pos=max(0,hi-1)
    assert pos < len(nd)//2,(n,b,hi,len(nd))
    assert (nd[pos]+nd[len(nd)-1-pos])%2==1,(n,b,ps,hi,nd)
    return 'regenerated-odd'

def main():
    totals={}
    for b in (2,4,6,8,10):
        count=Counter()
        for n in range(b,b**5):count[check(n,b)]+=1
        totals[b]=dict(count)
    rng=Random(20261028)
    for b in (2,4,6,8,10,12,16,32):
        for _ in range(2000):
            m=rng.randrange(2,200)
            d=[rng.randrange(b) for _ in range(m)]
            d[-1]=rng.randrange(1,b)
            check(number(d,b),b)
    print('EXHAUSTIVE EVEN-BASE CONTROL:',totals)
    print('RANDOM LONG CONTROL: 16000 cases, 2..199 digit words, bases 2,4,6,8,10,12,16,32')
    print('REGENERATION ALL CONTROLS PASSED')

if __name__=='__main__':main()

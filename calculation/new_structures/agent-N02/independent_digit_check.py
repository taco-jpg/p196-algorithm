#!/usr/bin/env python3
"""Independent checks using ordinary digits N and schoolbook N+reverse(N).
Does not import the carry transition implementation; only compares public API.
"""
import random
from carry_relation import relation_outputs


def digits_of_pairword(half,odd,base):
    """Produce a positive N with the requested symmetric pair sums."""
    n=2*len(half)-int(odd)
    d=[0]*n
    for i,a in enumerate(half):
        j=n-1-i
        if i==j:
            assert a%2==0
            d[i]=a//2
        else:
            # Force the most significant digit positive, even when a0 is small.
            low=min(base-1,a-1) if i==0 else min(base-1,a)
            d[i]=low
            d[j]=a-low
    assert d[-1]!=0
    return d


def ordinary_reverse_add(d,base):
    # No pairword normalizer; add the original integer's digits to its reverse.
    n=len(d)
    out=[]; carry=0
    for j in range(n):
        s=d[j]+d[n-1-j]+carry
        out.append(s%base);carry=s//base
    if carry:out.append(carry)
    assert out[-1]!=0
    return out


def half_of_pairword(d):
    return tuple(d[i]+d[-i-1] for i in range((len(d)+1)//2))


def trial():
    r=random.Random(20261029)
    checks=0
    for b in (2,3,9,10,13,50):
        for _ in range(2000):
            k=r.randint(1,100)
            odd=bool(r.randrange(2))
            half=[r.randrange(2*b-1) for __ in range(k)]
            half[0]=r.randint(1,2*b-2)
            if odd:
                half[-1]=2*r.randrange(b)
                if k==1 and half[0]==0:half[0]=2
            d=digits_of_pairword(half,odd,b)
            new=ordinary_reverse_add(d,b)
            gam=len(new)-len(d)
            expected=(gam,half_of_pairword(new))
            observed=relation_outputs(tuple(half),odd,b)
            assert observed=={expected},(b,half,odd,observed,expected)
            checks+=1
    print('INDEPENDENT_DIGIT_REVERSE_ADD_PASS',checks,'cases across bases 2,3,9,10,13,50')

if __name__=='__main__':trial()
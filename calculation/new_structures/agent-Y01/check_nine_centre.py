#!/usr/bin/env python3
"""Independent ordinary-decimal big-integer check for the all-width maximal 18-centre theorem.

The exhaustive and randomized tests corroborate the PAPER PROOF, not replace it.
No finite-horizon Lychrel survival statement is tested or asserted.
"""
from itertools import product
from random import Random

def canonical_integer(W, length):
    """Make an actual canonical decimal integer with pairword W 18^length reverse(W)."""
    low = [max(0, x - 9) for x in W]
    high = [min(9, x) for x in W]
    digits = low + [9] * length + high[::-1]  # units-first
    return int(''.join(str(d) for d in digits[::-1]))

def coeffs_from_integer(value):
    s = str(value)
    return [int(s[i]) + int(s[-1-i]) for i in range(len(s))]

def centred_18_length(coeffs):
    mid = len(coeffs) // 2
    if coeffs[mid] != 18:
        return 0
    start = mid
    while start > 0 and coeffs[start-1] == 18:
        start -= 1
    return len(coeffs) - 2*start

def check(W, length):
    assert length >= 1 and W and 1 <= W[0] <= 18
    assert all(0 <= x <= 18 for x in W) and W[-1] != 18
    n = canonical_integer(W, length)
    sn = str(n)
    assert coeffs_from_integer(n) == list(W) + [18]*length + list(W[::-1])
    successor = n + int(sn[::-1])  # genuine arbitrary-precision integer calculation
    gamma = len(str(successor)) - len(sn)
    assert gamma in (0,1)
    actual = centred_18_length(coeffs_from_integer(successor))
    c = 0
    for x in W:
        c = (x+c)//10
    expected = length-1 if gamma else (length if c else max(0,length-2))
    assert actual == expected, (W,length,gamma,c,actual,expected)
    return gamma,c,actual

def run():
    counts={}
    total=0
    for a in (1,2,3):
        for suffix in product(range(19),repeat=a-1):
            for lead in range(1,19):
                W=(lead,)+suffix
                if W[-1]==18:
                    continue
                for length in range(1,8):
                    gamma,c,_=check(W,length)
                    counts[(gamma,c)]=counts.get((gamma,c),0)+1
                    total+=1
    rng=Random(20261028)
    for _ in range(50000):
        a=rng.randint(1,17)
        W=[rng.randint(1,18)]+[rng.randint(0,18) for _ in range(a-1)]
        if W[-1]==18:
            W[-1]=17
        length=rng.randint(1,107)
        gamma,c,_=check(tuple(W),length)
        counts[(gamma,c)]=counts.get((gamma,c),0)+1
        total+=1
    assert set(counts)=={(0,0),(0,1),(1,0),(1,1)}
    assert check((5,5),14)==(0,0,12)
    print("PASS maximal-18-centre formula; whole-decimal big integers:",total)
    print("Branch counts:",sorted(counts.items()))

if __name__=="__main__":
    run()

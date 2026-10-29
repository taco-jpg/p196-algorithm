#!/usr/bin/env python3
"""Exact base-b predecessor pairword decoder using two end carries."""
from __future__ import annotations
from random import Random

def inverse_pairword(target: str, n: int, b: int = 10):
    """Unique possible width-n LSB-first palindromic pairword for target, or None."""
    ds = [int(c) for c in target[::-1]]
    assert 2 <= b <= 10 and target[0] != '0' and all(d < b for d in ds)
    if len(ds) not in (n, n+1):
        return None
    overflow = len(ds) == n+1
    if overflow and ds[n] != 1:
        return None
    states = {(0, int(overflow)): None}
    history = []
    for i in range(n // 2):
        j = n-1-i
        next_states = {}
        for state in states:
            low_carry, high_out = state
            for low_next in (0, 1):
                s = ds[i] + b*low_next - low_carry
                if not 0 <= s <= 2*b-2 or (i == 0 and s == 0):
                    continue
                for high_before in (0, 1):
                    if s + high_before != ds[j] + b*high_out:
                        continue
                    next_state = (low_next, high_before)
                    next_states.setdefault(next_state, (state, s))
        states = next_states
        history.append(states)
        if not states:
            return None
    possible = []
    for state in states:
        low, high = state
        if n % 2:
            s = ds[n//2] + b*high - low
            if not (0 <= s <= 2*b-2 and s % 2 == 0):
                continue
            mid = [s]
        else:
            if low != high:
                continue
            mid = []
        lower = []
        cursor = state
        for k in range(n//2-1, -1, -1):
            parent, s = history[k][cursor]
            lower.append(s)
            cursor = parent
        lower.reverse()
        p = lower + mid + lower[::-1]
        possible.append(p)
    if not possible:
        return None
    assert all(p == possible[0] for p in possible)
    p = possible[0]
    if normalize(p, b) != ds:
        raise AssertionError('inverse produced incorrect carry normal form')
    return p

def normalize(p, b=10):
    c=0;out=[]
    for x in p:
        q=x+c
        out.append(q%b)
        c=q//b
    if c: out.append(c)
    while len(out)>1 and out[-1]==0:out.pop()
    return out

def fibre_count(p, b=10):
    n=len(p)
    assert p==p[::-1]
    total=1
    for i in range(n//2):
        v=p[i]
        if i==0:
            options=sum(0 <= v-a < b for a in range(1,b))
        else:
            options=sum(0 <= v-a < b for a in range(b))
        total*=options
    if n%2:
        total*=int(p[n//2]%2==0 and (n != 1 or p[0] != 0))
    return total

def pairword(num: int, b=10):
    digs=[]
    while num:
        digs.append(num%b);num//=b
    if not digs:digs=[0]
    return [a+z for a,z in zip(digs,digs[::-1])]

def tests():
    for n in range(1,5):
        for x in range(10**(n-1),10**n):
            target=str(x+int(str(x)[::-1]))
            recovered=inverse_pairword(target,n)
            assert recovered==pairword(x)
            assert fibre_count(recovered)>=1
    rng=Random(71907)
    for n in (1,2,3,4,8,17,41,129,1024):
        for _ in range(120):
            t=str(rng.randrange(1,10))+''.join(str(rng.randrange(10)) for _ in range(n-1))
            for source_n in (n,n-1):
                if source_n<1:continue
                p=inverse_pairword(t,source_n)
                assert p is None or (len(p)==source_n and p==p[::-1]
                    and normalize(p)==list(map(int,t[::-1])))
    print('INVERSE_FIBRE_PASSED exhaustive sources 1..9999, 2040 random target/width cases')

if __name__=='__main__':tests()

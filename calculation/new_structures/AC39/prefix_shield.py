#!/usr/bin/env python3
"""AC39: exact two-ended carry-cone certificate for rooted phase-6 p12/m9.

The computed induction is valid for every possible physical interior.
It proves only finite-epoch outer-prefix restoration, not a Lychrel certificate.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import random
import sys

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

# Exact zero-based B6/W6 from lattice_kinks/data/lat_p12m9.txt.
B6 = (2,11,3,6,0,1,17,7,2,14,9,14,1,2,9,5,9,17,14,4,17,4,
      12,15,9,18,9,7,10,16,10,6,12,8)
W6 = (5,9,16,0,9,11,1,10,8)
G = (1,0,0,0)*30

def normalize(seq, carry=0):
    out = []
    for a in seq:
        assert 0 <= a <= 18 and carry in (0,1)
        z = a + carry
        out.append(z % 10)
        carry = z // 10
    return tuple(out), carry

def options(a):
    """Both possible upper inlet carries; NO strict-phase W9 filter."""
    lo, _ = normalize(a, 0)
    w = len(a)
    for inlet in (0,1):
        hi, gamma = normalize(a[::-1], inlet)
        if gamma == 0:
            out = tuple(lo[i]+hi[w-1-i] for i in range(w))
        else:
            out = (lo[0]+1,)+tuple(lo[i]+hi[w-i] for i in range(1,w))
        assert all(0 <= x <= 18 for x in out)
        yield inlet, gamma, out

def shield(prefix, steps=120):
    trace = []
    for t in range(steps):
        a,b = tuple(options(prefix))
        assert a[1] == b[1] == G[(t+6)%120]
        common = next((i for i,(x,y) in enumerate(zip(a[2],b[2])) if x!=y),len(prefix))
        nxt = a[2][:common]
        trace.append((t+1,len(prefix),len(nxt),a[1],
                      hashlib.sha256(bytes(nxt)).hexdigest()))
        prefix = nxt
        assert prefix
    return prefix,trace

def pair(n):
    d = [int(x) for x in str(n)[::-1]]
    return tuple(d[i]+d[-1-i] for i in range(len(d)))

def realize(p):
    assert p == p[::-1] and p[0] > 0
    d = [0]*len(p)
    for i in range(len(p)//2):
        hi = min(p[i],9)
        d[i],d[-1-i] = p[i]-hi,hi
    if len(p)%2:
        assert p[len(p)//2]%2 == 0
        d[len(p)//2] = p[len(p)//2]//2
    n = int(''.join(map(str,d[::-1])))
    assert pair(n) == p
    return n

def schoolbook(d):
    carry = 0
    out = []
    for x,y in zip(d,d[::-1]):
        z = x+y+carry
        out.append(z%10)
        carry = z//10
    if carry:out.append(carry)
    assert out[-1] > 0
    return out

def control(j,u,c,q,k):
    h = B6 + W6*q + tuple(j) + tuple(u)*k
    source = h+tuple(c)+h[::-1]
    n = realize(source)
    ds = [int(x) for x in str(n)[::-1]]
    gamma = []
    for t in range(120):
        oldlen = len(ds)
        ds = schoolbook(ds)
        n = n + int(str(n)[::-1])
        assert ds == [int(x) for x in str(n)[::-1]],(q,k,t)
        gamma.append(len(ds)-oldlen)
    target_h = B6+W6*q+tuple(j)+tuple(u)*(k+5)
    target = target_h+tuple(c)+target_h[::-1]
    actual = tuple(ds[i]+ds[-1-i] for i in range(len(ds)))
    assert actual == pair(n)
    assert actual[:70] == target[:70]
    assert actual[12] == target[12] == 1
    assert gamma == [G[(t+6)%120] for t in range(120)]
    first = next((i for i,(x,y) in enumerate(zip(actual,target)) if x!=y),None)
    if first is None and len(actual)!=len(target):
        first = min(len(actual),len(target))
    return first

def main():
    arg = argparse.ArgumentParser()
    arg.add_argument('--check',action='store_true')
    arg.add_argument('--verbose',action='store_true')
    a = arg.parse_args()
    start = B6+W6*14
    end,trace = shield(start)
    assert len(start)==160 and len(end)==70 and end==start[:70]
    assert sum(x[3] for x in trace)==30
    if a.verbose:
        for t in trace:print('TRACE',json.dumps(t))
    print('UNIFORM_PREFIX',json.dumps(dict(input=160,output=70,steps=120,
          overflows=30,site12=end[12],
          digest=hashlib.sha256(json.dumps(trace).encode()).hexdigest())))
    if a.check:
        rng = random.Random(390120)
        U = []
        for v in range(0,19,2):
            b=(9,v,18-v)
            for s in range(3):U.append(b[s:]+b[:s])
        assert len(U)==len(set(U))==30
        out = []
        for u in U:
            j=tuple(rng.randrange(19) for _ in range(6))
            for c in ((4,4),(4,14,4)):
                out.append(control(j,u,c,14,100))
        for q,k in ((20,80),(40,160),(80,320),(160,640)):
            for c in ((4,4),(4,14,4)):
                out.append(control((18,2,0,5,11,9),(9,0,18),c,q,k))
        assert len(out)==68 and all(x is not None for x in out)
        from collections import Counter
        print('INDEPENDENT_CONTROLS',json.dumps(dict(cases=68,steps=8160,
              mismatch_histogram=dict(Counter(out)))))

if __name__=='__main__':
    main()

#!/usr/bin/env python3
"""seeds.py -- smallest suspected Lychrel seeds per base (no palindrome within `steps` reverse-and-add steps)."""
import sys, os, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import nbs

def is_pal_int(b, x):
    d = nbs.digits(b, x); return d == d[::-1]

def survives(b, n, steps):
    x = n
    for t in range(steps + 1):
        d = nbs.digits(b, x)
        if d == d[::-1]: return False
        x = x + sum(v * b ** k for k, v in enumerate(d[::-1]))
    return True

def candidates(b, count=3, steps=300, nmax=10**7, tlimit=120):
    out = []; t0 = time.time()
    for n in range(b, nmax):          # at least two digits
        if survives(b, n, steps):
            out.append(n)
            if len(out) >= count: break
        if time.time() - t0 > tlimit: break
    return out

if __name__ == '__main__':
    res = {}
    fn = 'data/candidates.json'
    if os.path.exists(fn): res = json.load(open(fn))
    for b in range(int(sys.argv[1]), int(sys.argv[2]) + 1):
        if str(b) in res: continue
        t0 = time.time()
        c = candidates(b, count=6, steps=300, tlimit=float(sys.argv[3]) if len(sys.argv) > 3 else 100)
        res[str(b)] = c
        print(b, c, round(time.time() - t0, 1), flush=True)
        json.dump(res, open(fn, 'w'))

#!/usr/bin/env python3
"""latcheck.py -- check my infinite-line cell CA (ascending carry a_i, descending carry delta_i) reproduces W3/W7 lattice evolution.
v_i' = (v_i + a_i)%b + (v_i + delta_i)%b                       (gam = 0)
v_i' = (v_i + a_i)%b + (v_{i-1} + delta_{i-1})%b                (gam = 1)
a_i = [v_{i-1}+a_{i-1} >= b],  delta_i = [v_{i+1} + delta_{i+1} >= b]."""
import sys
def load(fn):
    tok = open(fn).read().split(); it = iter(tok)
    p = int(next(it)); nB = int(next(it)); m = int(next(it)); b = int(next(it))
    gam = [int(next(it)) for _ in range(p)]
    W = [[int(next(it)) for _ in range(m)] for _ in range(p)]
    cup = [[int(next(it)) for _ in range(m)] for _ in range(p)]
    return p, nB, m, b, gam, W, cup
def ring_carries(v, b):
    m = len(v)
    a = [0] * m
    for _ in range(4):
        for i in range(m):
            a[(i + 1) % m] = 1 if v[i] + a[i] >= b else 0
    d = [0] * m
    for _ in range(4):
        for i in range(m - 1, -1, -1):
            d[(i - 1) % m] = 1 if v[i] + d[i] >= b else 0
    # delta_i = [v_{i+1} + delta_{i+1} >= b]  -> d[i] holds delta_i? define below properly
    return a
def carries(v, b):
    m = len(v)
    a = [0] * m     # a[i] = ascending carry into cell i
    for _ in range(5):
        for i in range(m):
            a[(i + 1) % m] = 1 if v[i] + a[i] >= b else 0
    dl = [0] * m    # dl[i] = descending carry into mirror of cell i = [v_{i+1}+dl[i+1] >= b]
    for _ in range(5):
        for i in range(m - 1, -1, -1):
            dl[i] = 1 if v[(i + 1) % m] + dl[(i + 1) % m] >= b else 0
    return a, dl
def check(fn):
    p, nB, m, b, gam, W, cup = load(fn)
    bad = 0
    for t in range(p):
        v = W[t]; a, dl = carries(v, b)
        if a != cup[t]: bad += 1; print('cup mismatch t', t)
        nv = []
        for i in range(m):
            if gam[t] == 0: nv.append((v[i] + a[i]) % b + (v[i] + dl[i]) % b)
            else: nv.append((v[i] + a[i]) % b + (v[(i - 1) % m] + dl[(i - 1) % m]) % b)
        if nv != W[(t + 1) % p]:
            bad += 1; print('evolution mismatch at t', t, 'gam', gam[t]); print(' got ', nv); print(' want', W[(t + 1) % p])
    print(fn, 'p', p, 'm', m, 'gam', gam, 'bad', bad)
if __name__ == '__main__':
    for fn in sys.argv[1:]: check(fn)

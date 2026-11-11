#!/usr/bin/env python3
"""Plain fold simulation of a window on a band background (band periodic in x, carries = periodic fixed point).
Lists all exact periodic orbits of depth K and says which contain a given target window.
Usage: foldsim.py LATFILE K target (space separated cells, bottom first)"""
import sys, itertools
fn, K = sys.argv[1], int(sys.argv[2])
target = tuple(map(int, sys.argv[3:]))
tk = open(fn).read().split()
BASE, T, nB, s = map(int, tk[:4])
assert nB == 0
clk = list(map(int, tk[4:4 + T]))
v = list(map(int, tk[4 + T:]))
R = [v[t * s:(t + 1) * s] for t in range(T)]
M = 8  # periods of background below the window

def percarry(row):
    al = [0] * s
    for _ in range(3):
        for c in range(s):
            al[(c + 1) % s] = 1 if row[c] + al[c] >= BASE else 0
    return al

AL = [percarry(R[t]) for t in range(T)]

def step(t, j, par, w):
    """one exact fold step; returns (t', j', par', w') or None if the background below breaks"""
    c = j + M * s
    h = c + K
    P = [R[t][x % s] for x in range(c)] + list(w)
    a = [0] * (h + 1)
    a[0] = AL[t][0]
    for x in range(h):
        a[x + 1] = 1 if P[x] + a[x] >= BASE else 0
    e = [(P[x] + a[x]) % BASE for x in range(h)]
    Din = a[h] if par == 0 else a[h - 1]
    b = [0] * h
    b[h - 1] = Din
    for x in range(h - 1, 0, -1):
        b[x - 1] = 1 if P[x] + b[x] >= BASE else 0
    r = [(P[x] + b[x]) % BASE for x in range(h)]
    g = clk[t]
    tn = (t + 1) % T
    dh = 1 if (g == 1 and par == 0) else 0
    h2 = h + dh
    Q = [None] * h2
    for y in range(h2):
        if y == h:  # new top cell at a frame shift
            Q[y] = 2 * r[h - 1]
        elif y - g >= 0:
            Q[y] = e[y] + r[y - g]
    c2 = h2 - K
    for y in range(max(g, 2 * s), c2):  # skip the lowest columns (boundary of the finite stretch)
        if Q[y] != R[tn][y % s]:
            return None
    return (tn, c2 % s, (par + g) % 2, tuple(Q[c2:]))

found = {}
states = [(t, j, par, w) for t in range(T) for j in range(s) for par in (0, 1) for w in itertools.product(range(2 * BASE - 1), repeat=K)
          if not (par == 1 and w[-1] % 2)]
nxt = {}
for st in states:
    y = step(*st)
    if y is not None:
        nxt[st] = y
color = {}
cycles = []
for st in nxt:
    if st in color:
        continue
    path = []
    x = st
    while x in nxt and x not in color:
        color[x] = len(cycles) + 1
        path.append(x)
        x = nxt[x]
    if x in nxt and x in path:
        cyc = path[path.index(x):]
        cycles.append(cyc)
    for p in path:
        color[p] = -1
print('K', K, 'exact periodic orbits', len(cycles), 'periods', sorted(len(c) for c in cycles))
for c in cycles:
    has = [st for st in c if st[3] == target]
    print(' period', len(c), 'phases', sorted({(st[0], st[1], st[2]) for st in c})[:3], 'contains target' if has else '', has[:4] if has else '', 'windows:', [st[3] for st in c])

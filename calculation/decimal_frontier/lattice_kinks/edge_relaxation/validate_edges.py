#!/usr/bin/env python3
"""End-to-end check of the relaxation edges on the states that matter:
embed (phase, window) into a genuine full palindrome (exterior + lattice + window + a cell realising (Din, ghost)
+ random rest + centre), do one genuine pair-word step, and compare with window_step (new window and lattice-intact flag)."""
import sys, random
from klib import *

name, fn, K, N = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
lat = load(name); base = lat.nB + 5 * lat.m
prev = []
for line in open(fn):
    a = list(map(int, line.split()))
    prev.append(((a[1], a[2], a[3]), tuple(a[4:])))
rng = random.Random(11)
# prioritise extensions of accepting states
accp = [v for v in prev if v[1][0] != lat.cell(v[0][0], base + v[0][1])]
cases = 0; bad = 0; okc = 0
def embed(ph, win, Din, ghost):
    t, j, par = ph
    for attempt in range(200):
        # place the window at absolute c with (c-nB) % m == j, inside a long number of parity par
        c = base + j + lat.m * rng.randrange(2, 6)
        h_min = c + K + 4
        n = 2 * (h_min + rng.randrange(3, 30)) + par
        if n % 2 != par: n += 1
        h = (n + 1) // 2
        low = lat.row(t, c) + list(win)
        # carry out of the window top (ascending), given exact lattice below
        car = 0
        for v in low: car = (v + car) // 10
        # choose P_{c+K}, D_{c+K} realising Din and ghost
        opts = [(P, D) for P in range(19) for D in (0, 1) if (P + D) // 10 == Din and (P + car) % 10 == ghost]
        if not opts: return None
        P, D = rng.choice(opts)
        nxt = 0 if D == 0 else rng.randrange(10, 19)
        low += [P, nxt]
        while len(low) < h: low.append(rng.randrange(19))
        if n % 2 == 1 and low[h - 1] % 2: low[h - 1] -= 1
        # cell c+K+1 must produce D_{c+K} = D: need floor((nxt + D_{c+K+1})/10) == D
        Pf = full_from_lower(low, n)
        carr, ov = carries(Pf)
        if carr[n - 1 - (c + K)] != D: continue       # carry into mirror of cell c+K
        if (Pf[c + K] + carr[c + K]) % 10 != ghost: continue
        if carr[n - 1 - (c + K - 1)] != Din: continue
        return c, n, Pf
    return None

pool = [(v, x) for v in accp for x in range(19)]
rng.shuffle(pool)
others = [(v, x) for v in rng.sample(prev, min(len(prev), 2000)) for x in rng.sample(range(19), 3)]
for (v, x) in pool[:N] + others[:N]:
    ph, w5 = v; win = list(w5) + [x]
    t, j, par = ph
    g = lat.g[t]; dh = 1 if (g == 1 and par == 0) else 0
    for Din in (0, 1):
        for ghost in (range(10) if dh else [rng.randrange(10)]):
            r = embed(ph, win, Din, ghost)
            if r is None: continue
            c, n, Pf = r
            P2, gam = pairword_step(Pf)
            if gam != g: continue
            new, ok = window_step(lat, t, c, n, win, Din, ghost)
            real = P2[c + dh:c + dh + K]
            real_ok = all(P2[xx] == lat.cell(t + 1, xx) for xx in range(0, c + dh))
            cases += 1; okc += ok
            if new != real or ok != real_ok:
                bad += 1
                if bad < 5: print('MISMATCH', ph, win, Din, ghost, new, real, ok, real_ok)
print(f'{name} K={K}: genuine-step checks {cases}, mismatches {bad}, lattice-intact outcomes {okc}')

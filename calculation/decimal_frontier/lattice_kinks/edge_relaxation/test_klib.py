#!/usr/bin/env python3
"""Validate klib.window_step against genuine pair-word evolution of full palindromes:
exterior + lattice (exact) up to b, then a perturbed core, centre, mirror."""
import random, sys
from klib import *

def one(lat, rng, stats):
    m = lat.m
    t = rng.randrange(lat.p)
    n = rng.randrange(2 * (lat.nB + 6 * m), 2 * (lat.nB + 9 * m))
    h = (n + 1) // 2
    b = rng.randrange(lat.nB + 3 * m, h - 6)           # first possibly-perturbed cell
    low = lat.row(t, h)
    # perturb the core [b, h): mixture of lattice-like and random cells, sometimes 9-rich
    mode = rng.random()
    for x in range(b, h):
        if mode < 0.3: low[x] = rng.randrange(19)
        elif mode < 0.6:
            if rng.random() < 0.3: low[x] = rng.randrange(19)
        else:
            if rng.random() < 0.15: low[x] = rng.choice([9, 9, 8, 10, rng.randrange(19)])
    if rng.random() < 0.7: low[b] = rng.randrange(19)
    if n % 2 == 1 and low[h - 1] % 2: low[h - 1] -= 1
    P = full_from_lower(low, n)
    car, ov = carries(P)
    P2, gam = pairword_step(P)
    if gam != lat.g[t % lat.p]:
        stats['gam_mismatch'] += 1
        return
    n2 = n + gam; dh = (n2 + 1) // 2 - h
    # choose a window inside the lower half, below which the word is exact lattice
    c = b if rng.random() < 0.6 else rng.randrange(lat.nB + 2 * m + 2, b + 1)
    K = rng.randrange(1, min(12, h - 2 - c) + 1)
    if c + K > h - 2: return
    win = low[c:c + K]
    Din = car[n - c - K]                 # carry into the mirror of cell c+K-1
    ghost = (P[c + K] + car[c + K]) % BASE
    new, ok = window_step(lat, t, c, n, win, Din, ghost)
    real = P2[c + dh:c + dh + K]
    assert new == real, (lat.name, t, n, c, K, win, new, real)
    real_ok = all(P2[x] == lat.cell(t + 1, x) for x in range(0, c + dh))
    assert ok == real_ok, (lat.name, t, n, c, K, ok, real_ok)
    stats['ok' if ok else 'broken'] += 1

if __name__ == '__main__':
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 3000
    rng = random.Random(1)
    for name in ['rec0', 'rec1', 'rec2', 'p12m9']:
        lat = load(name)
        print(name, 'p', lat.p, 'g', ''.join(map(str, lat.g)), 'nB', lat.nB, 'm', lat.m, 'bulk mismatches', check_bulk(lat))
        stats = {'ok': 0, 'broken': 0, 'gam_mismatch': 0}
        for _ in range(N):
            one(lat, rng, stats)
        print('  window_step == genuine:', stats)

#!/usr/bin/env python3
"""PRO-R03-e (#481) stacked exterior Q_t(q) = B2_t ++ W48_t^q ++ B1_t[11:] ++ W20_t^inf (rec2 exterior over rec1 bulk).
Checks the two join identities, then genuine pair-word steps: one step at every phase (q in 0,1,2,3,5,8, random cores at the
midpoint) and 40 consecutive steps of one ordinary integer (q in 0,3,7), comparing the exterior cells with Q_{t+1}."""
import sys, random
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '../lattice_kinks/edge_relaxation'))
from klib import load_rec, pairword_step, full_from_lower, Lat
r1, r2 = load_rec(1), load_rec(2)
print('g1', r1.g, 'g2', r2.g, 'nB1', r1.nB, 'm1', r1.m, 'nB2', r2.nB, 'm2', r2.m)
p = 8
B1, W20, B2, W48 = r1.B, r1.W, r2.B, r2.W
print('B2==B1[:11] all t:', all(B2[t] == B1[t][:11] for t in range(p)), ' len B2', len(B2[0]))
print('B1[11:17]==W48[:6] all t:', all(B1[t][11:17] == W48[t][:6] for t in range(p)))
def Q(q):
    return Lat(f'Q{q}', r1.g, [B2[t] + W48[t]*q + B1[t][11:] for t in range(p)], W20)
# genuine check: full palindromes, lower half = Q row, deep W20 to the midpoint
def genuine(q, t, n, rng=None):
    L = Q(q); h = (n + 1)//2
    low = L.row(t, h)
    if rng:  # random core near the midpoint
        for x in range(h - rng.randrange(1, 8), h): low[x] = rng.randrange(19)
    if n % 2 == 1 and low[h-1] % 2: low[h-1] -= 1
    P = full_from_lower(low, n)
    P2, gam = pairword_step(P)
    if gam != L.g[t % p]: return None
    # compare cells well below the core
    depth = L.nB + 3*L.m
    return all(P2[x] == L.cell(t+1, x) for x in range(depth))
rng = random.Random(7)
tot = bad = skip = 0
for q in [0,1,2,3,5,8]:
    for t in range(p):
        L = Q(q)
        for k in range(6):
            n = 2*(L.nB + 8*L.m) + rng.randrange(0, 2*L.m)
            r = genuine(q, t, n, rng if k % 2 else None)
            if r is None: skip += 1; continue
            tot += 1; bad += (not r)
print('genuine one-step checks', tot, 'bad', bad, 'skipped(gamma mismatch)', skip)
# multi-step: evolve one actual integer 40 steps and track Q-row agreement
for q in [0, 3, 7]:
    L = Q(q); n = 2*(L.nB + 12*L.m) + 1; h = (n+1)//2
    low = L.row(0, h)
    if low[h-1] % 2: low[h-1] -= 1
    P = full_from_lower(low, n); worst = None
    for s in range(40):
        P, gam = pairword_step(P)
        ok = 0
        while ok < (len(P)+1)//2 and P[ok] == L.cell(s+1, ok): ok += 1
        worst = ok if worst is None else min(worst, ok)
    print(f'q={q}: 40 genuine steps, lattice-exact prefix min {worst} cells (nB={L.nB}, m={L.m})')

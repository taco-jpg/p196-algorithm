#!/usr/bin/env python3
"""gam_analysis.py FILE.npz [pattern ...] -- statistics of the overflow stream of a long orbit vs surrogates."""
import sys, collections, math
import numpy as np
z = np.load(sys.argv[1]); g = z['gam'].astype(np.int8); N = len(g); p1 = g.mean()
print('N', N, 'gam density', round(p1, 4))
# runs
def runs(x, v):
    c = collections.Counter(); cur = 0
    for a in x:
        if a == v: cur += 1
        else:
            if cur: c[cur] += 1
            cur = 0
    if cur: c[cur] += 1
    return c
r0 = runs(g, 0); r1 = runs(g, 1)
print('zero-run lengths (non-overflow stretches):', dict(sorted(r0.items())))
print('one-run lengths (consecutive overflows):', dict(sorted(r1.items())))
# block entropies
def Hk(x, k):
    n = len(x) - k + 1
    keys = np.zeros(n, dtype=np.int64)
    for i in range(k): keys = keys * 2 + x[i:i + n]
    cnt = np.bincount(keys, minlength=2 ** k).astype(float); p = cnt[cnt > 0] / n
    return -(p * np.log2(p)).sum()
print('conditional entropy h_k = H_k - H_{k-1} (bits):', [round(Hk(g, k) - (Hk(g, k - 1) if k > 1 else 0), 4) for k in range(1, 17)])
rng = np.random.default_rng(1)
sh = rng.permutation(g)
print('shuffled stream h_k:', [round(Hk(sh, k) - (Hk(sh, k - 1) if k > 1 else 0), 4) for k in range(1, 9)])
# longest periodic stretch: for each p<=40, longest stretch with g[i]==g[i+p] (window not constant)
def longest_periodic(x, p):
    eq = (x[p:] == x[:-p]).astype(np.int8)
    if eq.sum() == 0: return 0
    d = np.diff(np.concatenate(([0], eq, [0]))); st = np.flatnonzero(d == 1); en = np.flatnonzero(d == -1)
    return int((en - st).max()) + p if len(st) else 0
lp = {p: longest_periodic(g, p) for p in range(1, 41)}
lps = {p: longest_periodic(sh, p) for p in range(1, 41)}
print('longest p-periodic stretch  (orbit):', lp)
print('longest p-periodic stretch  (shuffled):', lps)
# match to given periodic patterns (strings of 0/1, all rotations)
for pat in sys.argv[2:]:
    p = len(pat); best = 0
    gs = ''.join(map(str, g.tolist()))
    for rot in range(p):
        q = pat[rot:] + pat[:rot]; L = 0
        # longest stretch of gs matching periodic extension of q (starting at phase 0 of q)
        for ph in range(p):
            qq = (q[ph:] + q[:ph])
            ref = np.frombuffer((qq * (N // p + 2))[:N].encode(), dtype=np.uint8) - 48
            eq = (g == ref).astype(np.int8)
            d = np.diff(np.concatenate(([0], eq, [0]))); st = np.flatnonzero(d == 1); en = np.flatnonzero(d == -1)
            if len(st): L = max(L, int((en - st).max()))
        best = max(best, L)
    # shuffled surrogate
    bests = 0
    for rot in range(p):
        q = pat[rot:] + pat[:rot]
        for ph in range(p):
            qq = (q[ph:] + q[:ph]); ref = np.frombuffer((qq * (N // p + 2))[:N].encode(), dtype=np.uint8) - 48
            eq = (sh == ref).astype(np.int8)
            d = np.diff(np.concatenate(([0], eq, [0]))); st = np.flatnonzero(d == 1); en = np.flatnonzero(d == -1)
            if len(st): bests = max(bests, int((en - st).max()))
    print(f'pattern {pat} (p={p}): longest exact match of orbit stream to its periodic extension (any rotation): {best}; shuffled stream: {bests}')

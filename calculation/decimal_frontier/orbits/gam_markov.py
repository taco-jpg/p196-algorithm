#!/usr/bin/env python3
"""gam_markov.py FILE.npz K -- compare long periodic stretches of the real overflow stream with order-K Markov surrogates fitted to it."""
import sys, collections
import numpy as np
z = np.load(sys.argv[1]); g = z['gam'].astype(np.int64); N = len(g); K = int(sys.argv[2])
rng = np.random.default_rng(7)
def stretch_lengths(x, p, minlen):
    eq = (x[p:] == x[:-p]).astype(np.int8)
    d = np.diff(np.concatenate(([0], eq, [0]))); st = np.flatnonzero(d == 1); en = np.flatnonzero(d == -1)
    return [int(e - s) + p for s, e in zip(st, en) if e - s + p >= minlen]
def alt_stretches(x, minlen):  # strictly alternating 0101.. stretches
    return stretch_lengths(x, 2, minlen)
def fit(g, K):
    ctx = np.zeros(N - K, dtype=np.int64)
    for i in range(K): ctx = ctx * 2 + g[i:N - K + i]
    nxt = g[K:]
    c1 = np.bincount(ctx, weights=nxt, minlength=2 ** K); c = np.bincount(ctx, minlength=2 ** K)
    return c1, c
def simulate(c1, c, K, n):
    x = np.zeros(n, dtype=np.int64); x[:K] = g[:K]
    ctx = 0
    for i in range(K): ctx = ctx * 2 + x[i]
    u = rng.random(n); mask = (1 << K) - 1
    for i in range(K, n):
        cc = c[ctx]; p = (c1[ctx] / cc) if cc > 0 else 0.4
        v = 1 if u[i] < p else 0
        x[i] = v; ctx = ((ctx << 1) | v) & mask
    return x
real = {p: stretch_lengths(g, p, 30 if p == 2 else 40) for p in (2, 4, 6, 8)}
print('real: #stretches>=30 (p=2):', len(real[2]), 'lengths', sorted(real[2]))
for p in (4, 6, 8): print('real: p=%d stretches>=40: %d max %d' % (p, len(real[p]), max(real[p]) if real[p] else 0))
c1, c = fit(g, K)
for rep in range(3):
    s = simulate(c1, c, K, N)
    print('Markov-%d surrogate %d: density %.4f  #alt stretches>=30: %d  lengths %s ; p=4 >=40: %d max %d; longest 2-periodic overall %d'
          % (K, rep, s.mean(), len(alt_stretches(s, 30)), sorted(alt_stretches(s, 30))[-6:], len(stretch_lengths(s, 4, 40)), max(stretch_lengths(s, 4, 40) or [0]), max(alt_stretches(s, 2) or [0])))

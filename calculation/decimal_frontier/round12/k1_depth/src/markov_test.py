#!/usr/bin/env python3
"""r12g markov_test.py -- is Cyc(K+1) determined by a bounded top suffix of Cyc(K)?
For every s in Cyc(K) (one orbit) let X(s) = {x : (s, x) in Cyc(K+1)} (19-bit mask).  For r = 1..R test whether X(s) is a function
of (phase, top r cells of s) and of (phase, bottom r cells of s): count groups with conflicting masks.
usage: markov_test.py CYC_K CYC_K1 K [R]"""
import sys
import numpy as np
fK, fK1, K = sys.argv[1], sys.argv[2], int(sys.argv[3]); R = int(sys.argv[4]) if len(sys.argv) > 4 else 8
def load(fn):
    a = np.fromfile(fn, dtype=np.uint64).reshape(-1, 2)
    return a[:, 0].copy(), a[:, 1].copy()
lo0, hi0 = load(fK); lo1, hi1 = load(fK1)
# keys as python-free arithmetic: phase = hi >> 36 (PS = 100); cells in lo (cells 0..11) and hi low 36 bits (cells 12..)
def cells(lo, hi, n):
    out = np.zeros((len(lo), n), dtype=np.int64)
    for i in range(n):
        b = 5 * i
        if b + 5 <= 64: out[:, i] = (lo >> np.uint64(b)) & np.uint64(31)
        elif b >= 64: out[:, i] = (hi >> np.uint64(b - 64)) & np.uint64(31)
        else: out[:, i] = ((lo >> np.uint64(b)) | (hi << np.uint64(64 - b))) & np.uint64(31)
    return out
ph0 = (hi0 >> np.uint64(36)).astype(np.int64); c0 = cells(lo0, hi0, K)
ph1 = (hi1 >> np.uint64(36)).astype(np.int64); c1 = cells(lo1, hi1, K + 1)
# map Cyc(K+1) states to their projection's row in Cyc(K)
def keyrows(ph, c, n):
    k = ph.copy()
    for i in range(n): k = k * 19 + c[:, i]
    return k   # fits int64 for n <= 12; for larger n use a tuple hash
if K <= 12:
    k0 = keyrows(ph0, c0, K); k1 = keyrows(ph1, c1[:, :K], K)
else:
    k0 = np.array([hash((int(p),) + tuple(r)) for p, r in zip(ph0, c0)], dtype=np.int64)
    k1 = np.array([hash((int(p),) + tuple(r)) for p, r in zip(ph1, c1[:, :K])], dtype=np.int64)
order = np.argsort(k0); ks = k0[order]
pos = np.searchsorted(ks, k1); assert np.all(ks[pos] == k1), 'projection of Cyc(K+1) not inside Cyc(K)'
mask = np.zeros(len(k0), dtype=np.int64)
np.bitwise_or.at(mask, order[pos], (1 << c1[:, K]).astype(np.int64))
print(f'K={K}: |Cyc(K)| = {len(k0)} (one orbit), |Cyc(K+1)| = {len(k1)}, states with no extension: {(mask == 0).sum()}, '
      f'mean extensions {np.bitwise_count(mask).mean() if hasattr(np, "bitwise_count") else "-"}')
for side in ('top', 'bottom'):
    for r in range(1, min(R, K) + 1):
        cols = c0[:, K - r:] if side == 'top' else c0[:, :r]
        g = ph0.copy()
        for i in range(r): g = g * 19 + cols[:, i]
        o = np.lexsort((mask, g)); gs = g[o]; ms = mask[o]
        newg = np.r_[True, gs[1:] != gs[:-1]]
        conflict = (~newg) & (ms != np.r_[ms[:1], ms[:-1]])
        gid = np.cumsum(newg) - 1
        nconf = len(np.unique(gid[conflict]))
        print(f'  {side} r={r}: groups {newg.sum()}, groups with conflicting extension sets {nconf}')

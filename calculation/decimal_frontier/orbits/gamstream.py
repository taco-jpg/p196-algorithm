#!/usr/bin/env python3
"""gamstream.py BASE SEEDSPEC T OUT.npy -- record the overflow stream gam_t (1 iff x_{t+1} has one more digit than x_t) of a long orbit.
Also records the lowest 4 and top 4 pair-word coefficients per step (bottom/top 'exterior' state) as int8 arrays."""
import sys, os, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rar, orbit2
b = int(sys.argv[1]); dg = orbit2.parse_seed(sys.argv[2], b); T = int(sys.argv[3]); out = sys.argv[4]
g = np.zeros(T, dtype=np.uint8); low = np.zeros((T, 4), dtype=np.int8)
d = dg.copy(); t0 = time.time()
for t in range(T):
    P = rar.pairword(d); nd, c = rar.normalize(P, b)
    g[t] = c; low[t, :min(4, len(P))] = P[:4]
    if c: nd = np.concatenate((nd, np.array([1], dtype=np.int16)))
    d = nd
    if rar.is_pal(d): print('palindrome at', t); g = g[:t + 1]; low = low[:t + 1]; break
np.savez_compressed(out, gam=g, low=low)
print('done', len(g), 'digits', len(d), 'gam density', g.mean(), round(time.time() - t0, 1), 's')

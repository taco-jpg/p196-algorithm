#!/usr/bin/env python3
"""latcell1.py -- single-cell time graph of the lowest defect cell sitting on a lattice at position j0 (stationary wall, ANY period multiple of p).
nodes (v,t); edge for each din with [v+din>=b]==G_t.  A stationary periodic defect (any width above) needs a cycle through a node with v != lattice value."""
import sys
sys.path.insert(0, 'lat'); sys.path.insert(0, '.')
from latcheck import load, carries
from cells2 import sccs
def analyze(fn):
    p, nB, m, b, gam, W, cup = load(fn)
    R = 2 * b - 1
    out = []
    for j0 in range(m):
        a = []; G = []; dd = []
        for t in range(p):
            v = W[t]; at, dl = carries(v, b)
            a.append(at[j0]); G.append(dl[(j0 - 1) % m]); dd.append((v[(j0 - 1) % m] + dl[(j0 - 1) % m]) % b)
        edges = {}
        for t in range(p):
            for v in range(R):
                for din in (0, 1):
                    if (1 if v + din >= b else 0) != G[t]: continue
                    if gam[t] == 0: vn = (v + a[t]) % b + (v + din) % b
                    else: vn = (v + a[t]) % b + dd[t]
                    if vn > R - 1: continue
                    edges.setdefault((v, t), set()).add((vn, (t + 1) % p))
        edges = {k: sorted(v) for k, v in edges.items()}
        comps = sccs(edges)
        cyc = [c for c in comps if len(c) > 1 or any(w in set(c) for w in edges.get(c[0], []))]
        offl = []
        for c in cyc:
            if any(v != W[t][j0 % m] for (v, t) in c): offl.append((len(c), sorted({v for v, t in c})))
        out.append((j0, len(cyc), offl))
    return out
if __name__ == '__main__':
    for fn in sys.argv[1:]:
        res = analyze(fn)
        print(fn, 'positions with an off-lattice cyclic SCC:', [(j, o) for j, n, o in res if o])
        print('   cyclic SCC counts per j0:', [n for j, n, o in res])

#!/usr/bin/env python3
"""latcell2.py -- time automaton on the 2 lowest defect cells above a lattice (stationary wall, ALL periods that are multiples of p, all widths above).
usage: latcell2.py latfile"""
import sys
sys.path.insert(0, 'lat'); sys.path.insert(0, '.')
from latcheck import load, carries
from cells2 import sccs
def build(fn, j0):
    p, nB, m, b, gam, W, cup = load(fn)
    R = 2 * b - 1
    a = []; G = []; dd = []
    for t in range(p):
        v = W[t]; at, dl = carries(v, b)
        a.append(at[j0]); G.append(dl[(j0 - 1) % m]); dd.append((v[(j0 - 1) % m] + dl[(j0 - 1) % m]) % b)
    edges = {}
    for t in range(p):
        for v0 in range(R):
            A1 = 1 if v0 + a[t] >= b else 0
            da0 = (v0 + a[t]) % b
            for v1 in range(R):
                da1 = (v1 + A1) % b
                for din1 in (0, 1):
                    din0 = 1 if v1 + din1 >= b else 0
                    if (1 if v0 + din0 >= b else 0) != G[t]: continue
                    dd0 = (v0 + din0) % b; dd1 = (v1 + din1) % b
                    if gam[t] == 0: n0 = da0 + dd0; n1 = da1 + dd1
                    else: n0 = da0 + dd[t]; n1 = da1 + dd0
                    if n0 > R - 1 or n1 > R - 1: continue
                    edges.setdefault((v0, v1, t), []).append((n0, n1, (t + 1) % p))
    return p, m, b, W, edges
def analyze(fn):
    res = []
    p, nB, m, b, gam, W, cup = load(fn)
    for j0 in range(m):
        p, m, b, W, edges = build(fn, j0)
        comps = sccs(edges)
        cyc = [c for c in comps if len(c) > 1 or any(w in set(c) for w in edges.get(c[0], []))]
        off = [c for c in cyc if any(v0 != W[t][j0] for (v0, v1, t) in c)]
        res.append((j0, len(cyc), [(len(c), sorted({n[0] for n in c})) for c in off]))
    return res
if __name__ == '__main__':
    for fn in sys.argv[1:]:
        res = analyze(fn)
        print(fn, 'off-lattice cyclic SCCs on 2 cells:', [(j, o) for j, n, o in res if o] or 'NONE')
        print('  (cyclic SCC counts per j0:', [n for j, n, o in res], ')')

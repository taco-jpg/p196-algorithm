#!/usr/bin/env python3
"""latcellw.py -- width-w time automaton on the w lowest defect cells above a lattice at position j0 (stationary wall, ALL periods multiple of p).
Iterative deepening: nodes at width w are restricted to prefixes lying in an off-lattice cyclic SCC of width w-1.  Empty set => NO stationary periodic defect
(any period multiple of p, any width, any content above).  usage: latcellw.py latfile [wmax] [j0 list]"""
import sys
sys.path.insert(0, 'lat'); sys.path.insert(0, '.')
from latcheck import load, carries
from cells2 import sccs

def lattice_links(fn, j0):
    p, nB, m, b, gam, W, cup = load(fn)
    a = []; G = []; dd = []
    for t in range(p):
        v = W[t]; at, dl = carries(v, b)
        a.append(at[j0 % m]); G.append(dl[(j0 - 1) % m]); dd.append((v[(j0 - 1) % m] + dl[(j0 - 1) % m]) % b)
    return p, m, b, gam, W, a, G, dd

def step_nodes(b, gam, a0, G0, dd0, vs, t):
    """all successors of node (vs, t) over din_top in {0,1}; vs tuple of w values; returns list of (vs', din_top choice) """
    w = len(vs); R = 2 * b - 1
    # ascending carries
    asc = [a0]
    for i in range(w): asc.append(1 if vs[i] + asc[i] >= b else 0)
    out = []
    for dtop in (0, 1):
        din = [0] * w          # din[i] = descending carry into mirror of cell i
        d = dtop
        for i in range(w - 1, -1, -1):
            din[i] = d
            d = 1 if vs[i] + din[i] >= b else 0
        # d is now delta_{-1} = required G0
        if d != G0: continue
        dig = [(vs[i] + din[i]) % b for i in range(w)]
        nv = []
        ok = True
        for i in range(w):
            x = (vs[i] + asc[i]) % b
            y = dig[i] if gam == 0 else (dd0 if i == 0 else dig[i - 1])
            s = x + y
            if s > R - 1: ok = False; break
            nv.append(s)
        if ok: out.append(tuple(nv))
    return out

def run(fn, j0, wmax):
    p, m, b, gam, W, a, G, dd = lattice_links(fn, j0)
    R = 2 * b - 1
    # width 1
    allowed = None   # set of prefix nodes (vs, t) allowed (from previous level's off-lattice SCCs)
    hist = []
    for w in range(1, wmax + 1):
        edges = {}
        if allowed is None:
            cand = [((v,), t) for t in range(p) for v in range(R)]
        else:
            cand = [(pre + (v,), t) for (pre, t) in allowed for v in range(R)]
        cs = set(cand)
        for (vs, t) in cand:
            for nv in step_nodes(b, gam[t], a[t], G[t], dd[t], vs, t):
                tgt = (nv, (t + 1) % p)
                edges.setdefault((vs, t), []).append(tgt)
        # restrict edges to targets in cs (necessary: targets must also be allowed prefix-wise)
        edges = {k: [x for x in v if x in cs] for k, v in edges.items()}
        edges = {k: v for k, v in edges.items() if v}
        comps = sccs(edges)
        keep = set()
        for c in comps:
            if len(c) == 1 and c[0] not in edges.get(c[0], []): continue
            if any(vs[0] != W[t][j0 % m] for (vs, t) in c):
                keep.update(c)
        hist.append((w, len(cand), len(keep)))
        print('   j0', j0, 'w', w, 'cand', len(cand), 'keep', len(keep), flush=True)
        if not keep: return hist, False
        allowed = {(vs, t) for (vs, t) in keep}
    return hist, True

if __name__ == '__main__':
    fn = sys.argv[1]; wmax = int(sys.argv[2]) if len(sys.argv) > 2 else 6
    p, nB, m, b, gam, W, cup = load(fn)
    j0s = [int(x) for x in sys.argv[3].split(',')] if len(sys.argv) > 3 else list(range(m))
    for j0 in j0s:
        hist, alive = run(fn, j0, wmax)
        print(fn, 'j0', j0, 'alive' if alive else 'DEAD', hist, flush=True)

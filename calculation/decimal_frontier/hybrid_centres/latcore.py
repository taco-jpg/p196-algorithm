#!/usr/bin/env python3
"""latcore.py -- stationary hybrid wall (A = 0) between a lattice (below) and an absorbing core (above): width-w time automaton with the TOP forced to the core vacuum.
Decides, for ALL periods (multiples of lcm(p, loop period)) at once, whether a stationary periodic defect of width <= wmax exists.
  top conditions:  delta_top(t) = k(t),  ascending carry out of the defect a_w(t) = k(t),  gam_t=1: (v_{w-1}+k)%b == y(t).
usage: latcore.py latfile wmax [j0 list]"""
import sys, math
sys.path.insert(0, 'lat'); sys.path.insert(0, '.')
from latcheck import load, carries
from cells2 import sccs
from latcellw import lattice_links, step_nodes
LOOPS = [[0], [18], [6, 12], [2, 4, 8, 16, 14, 10]]

def forced_succ(b, gam, a0, G0, dd0, vs, k, y):
    w = len(vs); R = 2 * b - 1
    asc = [a0]
    for i in range(w): asc.append(1 if vs[i] + asc[i] >= b else 0)
    if asc[w] != k: return None
    din = [0] * w; d = k
    for i in range(w - 1, -1, -1):
        din[i] = d; d = 1 if vs[i] + din[i] >= b else 0
    if d != G0: return None
    dig = [(vs[i] + din[i]) % b for i in range(w)]
    if gam == 1 and dig[w - 1] != y: return None
    nv = []
    for i in range(w):
        x = (vs[i] + asc[i]) % b
        yv = dig[i] if gam == 0 else (dd0 if i == 0 else dig[i - 1])
        s = x + yv
        if s > R - 1: return None
        nv.append(s)
    return tuple(nv)

def run(fn, j0, wmax, verbose=True, links=None, loops=None):
    p, m, b, gam, W, a, G, dd = links if links else lattice_links(fn, j0)
    LP = loops if loops else LOOPS
    R = 2 * b - 1
    allowed = None; res = {}
    for w in range(1, wmax + 1):
        cand = [((v,), t) for t in range(p) for v in range(R)] if allowed is None else [(pre + (v,), t) for (pre, t) in allowed for v in range(R)]
        # free-top relaxation (for pruning the next level)
        cs = set(cand); edges = {}
        for (vs, t) in cand:
            for nv in step_nodes(b, gam[t], a[t], G[t], dd[t], vs, t):
                tgt = (nv, (t + 1) % p)
                if tgt in cs: edges.setdefault((vs, t), []).append(tgt)
        comps = sccs(edges); keep = set()
        for c in comps:
            if len(c) == 1 and c[0] not in edges.get(c[0], []): continue
            if any(vs[0] != W[t][j0 % m] for (vs, t) in c): keep.update(c)
        # forced-top decision for each loop / phase
        for lp in LP:
            per = len(lp); Tn = p * per // math.gcd(p, per)
            for s in range(per):
                ks = [1 if lp[(s + tau) % per] >= b else 0 for tau in range(Tn)]
                ys = [(lp[(s + tau) % per] + ks[tau]) % b for tau in range(Tn)]
                fe = {}
                fc = [(vs, tau) for (vs, t) in keep for tau in range(t, Tn, p)]
                fcs = set(fc)
                for (vs, tau) in fc:
                    t = tau % p
                    nv = forced_succ(b, gam[t], a[t], G[t], dd[t], vs, ks[tau], ys[tau])
                    if nv is None: continue
                    tgt = (nv, (tau + 1) % Tn)
                    if tgt in fcs: fe.setdefault((vs, tau), []).append(tgt)
                fcomps = sccs(fe)
                hit = []
                for c in fcomps:
                    if len(c) == 1 and c[0] not in fe.get(c[0], []): continue
                    if any(vs[0] != W[tau % p][j0 % m] for (vs, tau) in c): hit.append(c)
                if hit:
                    res.setdefault((tuple(lp), s), []).append((w, len(hit), sorted(max(hit, key=len))[:3]))
        if verbose: print(f"  j0={j0} w={w} free-nodes={len(cand)} keep={len(keep)} hits_so_far={ {k: [x[0] for x in v] for k, v in res.items()} }", flush=True)
        if not keep: return res, False
        allowed = keep
    return res, True

if __name__ == '__main__':
    fn = sys.argv[1]; wmax = int(sys.argv[2])
    p, nB, m, b, gam, W, cup = load(fn)
    j0s = [int(x) for x in sys.argv[3].split(',')] if len(sys.argv) > 3 else list(range(m))
    for j0 in j0s:
        res, alive = run(fn, j0, wmax, verbose=False)
        print(fn, 'j0', j0, 'free-automaton', 'alive' if alive else 'DEAD', 'HITS' if res else 'no hybrid wall', res if res else '', flush=True)

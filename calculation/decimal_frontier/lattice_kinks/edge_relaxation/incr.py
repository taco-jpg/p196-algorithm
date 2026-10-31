#!/usr/bin/env python3
"""Exact incremental computation of the cyclic part of the K-window relaxation automaton.
Cyc(K) = states lying on some cycle.  Projection lemma: the bottom K-1 cells of a state on a K-cycle lie on a
(K-1)-cycle (the (K-1)-relaxation is driven by the true carry/digit of cell K-1).  Hence
Cyc(K) = cyclic-SCC states of the subgraph induced on Cyc(K-1) x {0..18}.
Accepting = window bottom cell off-lattice.  'No accepting cyclic SCC at K' means: no infinite run of the
relaxation with the bottom cell off-lattice infinitely often, i.e. no kink (ANY time period) whose deepest-defect
frame has >= K cells below the centre.
usage: incr.py lat dumpfile K0 Kmax   (dumpfile: cyclic states at K0 from relax2 ... dump)"""
import sys, time
from collections import defaultdict
from klib import *

name, fn, K0, Kmax = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
lat = load(name); base = lat.nB + 5 * lat.m

def nxt(ph):
    t, j, par = ph; g = lat.g[t]; dh = 1 if (g == 1 and par == 0) else 0
    return ((t + 1) % lat.p, (j + dh) % lat.m, (par + g) % 2), dh

def acc(v):
    (t, j, par), win = v
    return win[0] != lat.cell(t, base + j)

def scc(nodes, E):
    index = {}; low = {}; onst = set(); st = []; comps = []; idx = 0
    for root in nodes:
        if root in index: continue
        index[root] = low[root] = idx; idx += 1; st.append(root); onst.add(root)
        work = [(root, iter(E[root]))]
        while work:
            v, it = work[-1]; adv = False
            for w in it:
                if w not in index:
                    index[w] = low[w] = idx; idx += 1; st.append(w); onst.add(w)
                    work.append((w, iter(E[w]))); adv = True; break
                elif w in onst and index[w] < low[v]: low[v] = index[w]
            if adv: continue
            work.pop()
            if work:
                u = work[-1][0]
                if low[v] < low[u]: low[u] = low[v]
            if low[v] == index[v]:
                comp = []
                while True:
                    w = st.pop(); onst.discard(w); comp.append(w)
                    if w == v: break
                comps.append(comp)
    return comps

Cyc = []
for line in open(fn):
    a = list(map(int, line.split()))
    Cyc.append(((a[1], a[2], a[3]), tuple(a[4:])))
assert all(len(w) == K0 for _, w in Cyc)
print(f'{name}: |Cyc({K0})| = {len(Cyc)}, accepting {sum(acc(v) for v in Cyc)}', flush=True)
for K in range(K0 + 1, Kmax + 1):
    t0 = time.time()
    cand = set((ph, w + (x,)) for (ph, w) in Cyc for x in range(19))
    E = {}
    for v in cand:
        (t, j, par), win = v
        ph2, dh = nxt((t, j, par))
        outs = set()
        for Din in (0, 1):
            for gh in (range(10) if dh else [0]):
                new, ok = window_step(lat, t, base + j, 1000 + par, list(win), Din, gh)
                if ok:
                    w2 = (ph2, tuple(new))
                    if w2 in cand: outs.add(w2)
        E[v] = outs
    comps = scc(list(cand), E)
    cyc = [c for c in comps if len(c) > 1 or c[0] in E[c[0]]]
    Cyc = [v for c in cyc for v in c]
    accs = [c for c in cyc if any(acc(v) for v in c)]
    nacc = sum(1 for c in accs for v in c if acc(v))
    print(f'{name} K={K}: candidates {len(cand)}, cyclic states {len(Cyc)} in {len(cyc)} SCCs '
          f'(sizes {sorted(len(c) for c in cyc)}), accepting SCCs {len(accs)}, accepting states {nacc}  '
          f'[{time.time()-t0:.0f}s]', flush=True)
    if not accs:
        # the remaining cycles: are they exactly the all-lattice cycles?
        alllat = all(v[1] == tuple(lat.cell(v[0][0], base + v[0][1] + i) for i in range(K)) for v in Cyc)
        print(f'  NO accepting cycle at K={K}; remaining cyclic states all-lattice: {alllat}', flush=True)
        break
    with open(f'cyc_{name}_K{K}.txt', 'w') as f:
        for ci, c in enumerate(cyc):
            for (ph, w) in c: f.write(f'{ci} {ph[0]} {ph[1]} {ph[2]} ' + ' '.join(map(str, w)) + '\n')

#!/usr/bin/env python3
"""symgraph.py (r14a): check that the big SCC of the interface graph is invariant under R (time rotation by 2) and C (complement), as labelled graph."""
import sys, os, collections
sys.path.insert(0, os.path.expanduser('~/p196_run/mchk14'))
import ifscc
g = [1, 0] * 4; d = 8
states, adj, level = ifscc.build(g, d)
ids = {s: i for i, s in enumerate(states)}
n = len(states)
succ = [sorted(set(a.values())) for a in adj]
comps = [c for c in ifscc.tarjan(n, succ) if len(c) > 1 or c[0] in succ[c[0]]]
comps.sort(key=len, reverse=True)
comp = comps[0]; cs = set(comp)
edges = {v: {col: w for col, w in adj[v].items() if w in cs} for v in comp}
print('comp', len(comp))
def R_state(st):
    c, xb, A, root = st
    return (tuple(c[(t+2)%8] for t in range(8)), tuple(xb[(t+2)%8] for t in range(8)), tuple(A[(t+2)%8] for t in range(8)), root)
def C_state(st):
    c, xb, A, root = st
    # complement: c -> 1-c; xb -> 18-xb (for g=1 entries; 0 entries at g=0 stay 0); A mask -> swap bits
    swap = lambda a: ((a & 1) << 1) | ((a >> 1) & 1)
    return (tuple(1 - x for x in c), tuple(18 - xb[t] if g[t] else 0 for t in range(8)), tuple(swap(a) for a in A), root)
def Rcol(col): return tuple(col[(t+2)%8] for t in range(8))
def Ccol(col): return tuple(18 - x for x in col)
for name, f, fc in (('R', R_state, Rcol), ('C', C_state, Ccol), ('RC', lambda s: R_state(C_state(s)), lambda col: Rcol(Ccol(col)))):
    badn = 0; bade = 0; mapped = 0
    for v in comp:
        im = f(states[v])
        j = ids.get(im)
        if j is None or j not in cs:
            badn += 1
            continue
        mapped += 1
        # edges: for each edge v -col-> w, image edge j -fc(col)-> im(w)
        for col, w in edges[v].items():
            imw = ids.get(f(states[w]))
            target = edges[j].get(fc(col))
            if target != imw:
                bade += 1
    print(name, 'nodes mapped into comp', mapped, 'not mapped', badn, 'edge mismatches', bade)
# 48-cycle edge tags invariant? (skip)

#!/usr/bin/env python3
"""cells2.py -- TIME-automaton for the two lowest cells above a neutral band (A=0 / stationary-wall case, ALL periods at once).
Nodes (v0,v1,phase).  Edge for each free din1 in {0,1}.  Any periodic (period multiple of p) solution of cells 0,1 is a closed walk;
report nontrivial SCCs and whether cell 0 can be non-9 on a cycle."""
import sys
sys.setrecursionlimit(1000000)

def build(b, gam, e1, nodes_filter=None):
    p = len(gam); N = b - 1; R = 2 * b - 1
    edges = {}
    for ph in range(p):
        a0 = e1[ph]
        for v0 in range(R):
            A1 = 1 if v0 + a0 >= b else 0
            da0 = (v0 + a0) % b
            for v1 in range(R):
                da1 = (v1 + A1) % b
                for din1 in (0, 1):
                    din0 = 1 if v1 + din1 >= b else 0
                    # flip at bottom: [v0+din0>=b] == 1-e1
                    if (1 if v0 + din0 >= b else 0) != 1 - a0: continue
                    dd0 = (v0 + din0) % b; dd1 = (v1 + din1) % b
                    if gam[ph] == 0:
                        n0 = da0 + dd0; n1 = da1 + dd1
                    else:
                        n0 = da0 + N * a0; n1 = da1 + dd0
                    if n0 > 2 * b - 2 or n1 > 2 * b - 2: continue
                    edges.setdefault((v0, v1, ph), []).append((n0, n1, (ph + 1) % p))
    return edges

def sccs(edges):
    # iterative Tarjan
    index = {}; low = {}; onstack = set(); stack = []; res = []; idx = [0]
    nodes = set(edges) | {w for vs in edges.values() for w in vs}
    for root in nodes:
        if root in index: continue
        work = [(root, iter(edges.get(root, [])))]
        index[root] = low[root] = idx[0]; idx[0] += 1; stack.append(root); onstack.add(root)
        while work:
            v, it = work[-1]
            adv = False
            for w in it:
                if w not in index:
                    index[w] = low[w] = idx[0]; idx[0] += 1; stack.append(w); onstack.add(w)
                    work.append((w, iter(edges.get(w, [])))); adv = True; break
                elif w in onstack:
                    low[v] = min(low[v], index[w])
            if adv: continue
            work.pop()
            if work:
                u = work[-1][0]; low[u] = min(low[u], low[v])
            if low[v] == index[v]:
                comp = []
                while True:
                    w = stack.pop(); onstack.discard(w); comp.append(w)
                    if w == v: break
                res.append(comp)
    return res

def analyze(b, gam, e1, label=''):
    edges = build(b, gam, e1)
    comps = sccs(edges)
    N = b - 1
    cyc = []
    for c in comps:
        cs = set(c)
        if len(c) > 1 or any(w in cs for w in edges.get(c[0], [])):
            cyc.append(c)
    print(f"{label}: nodes with edges {len(edges)}, cyclic SCCs {len(cyc)}")
    for c in cyc:
        v0s = sorted({n[0] for n in c}); v1s = sorted({n[1] for n in c})
        triv = all(n[0] == N for n in c)
        print(f"   SCC size {len(c)}  v0 values {v0s}  v1 values {v1s}  {'(cell0 == N only)' if triv else '*** cell 0 non-trivial ***'}")
    return cyc

if __name__ == '__main__':
    from runsat import stream
    from streams_all import collect
    for name in ('p11', 'p12'):
        cyc = stream(name); p = len(cyc)
        gam = [cyc[t][1] for t in range(p)]; e1 = [cyc[t][2] for t in range(p)]
        analyze(10, gam, e1, f"decimal {name}")
    # control base 4
    analyze(4, [0,0,1,0,1,1], [0,1,0,1,0,1], "base4 g=001011 e=010101")
    analyze(4, [0,0,1,0,1,1], [1,0,1,0,1,0], "base4 g=001011 e=101010")

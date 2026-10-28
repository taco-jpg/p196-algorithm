#!/usr/bin/env python3
"""life.py -- lifetime bound of the lowest non-9 cell above the N-pad: longest path in the w-cell time graph restricted to v0 != 9
(DAG if no cyclic SCC has v0 != 9).  A >= T/L - 1 pops per period T would follow.  usage: life.py p11|p12 wmax"""
import sys
sys.setrecursionlimit(1000000)
sys.path.insert(0, '.'); sys.path.insert(0, 'lat')
from latcellw import step_nodes
from runsat import stream
def lifetimes(name, wmax):
    cyc = stream(name); p = len(cyc); b = 10; N = 9
    gam = [c[1] for c in cyc]; e1 = [c[2] for c in cyc]
    a0 = e1; G0 = [1 - x for x in e1]; dd0 = [N * x for x in e1]
    R = 19
    allowed = None
    for w in range(1, wmax + 1):
        if allowed is None: cand = [((v,), t) for t in range(p) for v in range(R) if v != 9]
        else: cand = [(pre + (v,), t) for (pre, t) in allowed for v in range(R)]
        cs = set(cand)
        edges = {}
        for (vs, t) in cand:
            for nv in step_nodes(b, gam[t], a0[t], G0[t], dd0[t], vs, t):
                if nv[0] == 9: continue
                tgt = (nv, (t + 1) % p)
                if tgt in cs: edges.setdefault((vs, t), []).append(tgt)
        # longest path (number of edges) in graph on v0 != 9 -- detect cycles
        color = {}; best = {}
        cyc_found = False
        for root in cand:
            if root in color: continue
            stack = [(root, iter(edges.get(root, [])))]; color[root] = 1; best[root] = 0
            while stack:
                v, it = stack[-1]
                adv = False
                for u in it:
                    if u not in color:
                        color[u] = 1; best[u] = 0; stack.append((u, iter(edges.get(u, [])))); adv = True; break
                    elif color[u] == 1: cyc_found = True
                    else: best[v] = max(best[v], 1 + best[u])
                if adv: continue
                color[v] = 2; stack.pop()
                if stack:
                    par = stack[-1][0]; best[par] = max(best[par], 1 + best[v])
        L = max(best.values()) if best else 0
        # nodes that can continue: keep those having at least one successor? allowed set for next width = all candidate nodes (relaxation)
        print(f"{name} w={w}: nodes {len(cand)} edges {sum(len(v) for v in edges.values())} cycle_with_v0_ne_9={cyc_found} longest alive path (edges) = {L}", flush=True)
        # next level: prefixes that appear in some edge (source or target)
        keep = set(edges) | {u for v in edges.values() for u in v}
        allowed = keep
        if not keep: break
if __name__ == '__main__':
    lifetimes(sys.argv[1], int(sys.argv[2]))

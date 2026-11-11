#!/usr/bin/env python3
"""scc_struct.py (r14a): compress the big SCC of the clock-10 d=8 interface graph into branch nodes and chains; report chain lengths and the position of the shortest cycles."""
import sys, os, collections, json
sys.path.insert(0, os.path.expanduser('~/p196_run/mchk14'))
import ifscc
g = [1, 0] * 4
d = 8
states, adj, level = ifscc.build(g, d)
n = len(states)
succ = [sorted(set(a.values())) for a in adj]
comps = [c for c in ifscc.tarjan(n, succ) if len(c) > 1 or c[0] in succ[c[0]]]
comps.sort(key=len, reverse=True)
comp = comps[0]; cs = set(comp)
edges = {v: [(col, w) for col, w in adj[v].items() if w in cs] for v in comp}
indeg = collections.Counter()
for v in comp:
    for col, w in edges[v]:
        indeg[w] += 1
branch = [v for v in comp if len(edges[v]) >= 2 or indeg[v] >= 2]
print('nodes', len(comp), 'edges', sum(len(e) for e in edges.values()), 'branch nodes', len(branch))
outd = collections.Counter(len(edges[v]) for v in comp)
ind = collections.Counter(indeg[v] for v in comp)
print('outdegree histogram', sorted(outd.items()), 'indegree histogram', sorted(ind.items()))
# chains: from each branch node, follow each out-edge until next branch node
bs = set(branch)
chains = []
for u in branch:
    for col, w in edges[u]:
        path = [(col, w)]
        x = w
        while x not in bs:
            col2, x2 = edges[x][0]
            path.append((col2, x2))
            x = x2
        chains.append((u, x, len(path)))
print('chains', len(chains))
cl = sorted(c[2] for c in chains)
print('chain length histogram', sorted(collections.Counter(cl).items()))
# compressed graph: branch-level adjacency with lengths
out = collections.defaultdict(list)
for u, v, L in chains:
    out[u].append((v, L))
print('compressed: branch node -> (next branch, chain length)')
ids = {v: i for i, v in enumerate(sorted(branch))}
for u in sorted(branch):
    print(ids[u], 'outdeg', len(edges[u]), 'indeg', indeg[u], [(ids[v], L) for v, L in out[u]])
# the shortest cycles through the compressed graph: list simple cycles (by branch nodes) with total length <= 110
import itertools
cycles = []
def dfs(start, v, pathlen, path, vis):
    for (w, L) in out[v]:
        nl = pathlen + L
        if nl > 110: continue
        if w == start:
            cycles.append((nl, list(path) + [(v, w, L)]))
        elif w not in vis and ids[w] > ids[start]:
            vis.add(w); path.append((v, w, L))
            dfs(start, w, nl, path, vis)
            path.pop(); vis.discard(w)
for b in sorted(branch):
    dfs(b, b, 0, [], {b})
print('simple cycles in compressed graph, length <= 110:')
for nl, p in sorted(cycles, key=lambda x: x[0]):
    print(nl, [(ids[a], L) for (a, b, L) in p])

#!/usr/bin/env python3
"""walks.py (r14a): enumerate ALL primitive closed walks (simple or not) of length <= Lmax in the big SCC of the clock-10, d=8 interface graph.
Writes lat files for every primitive label word (one representative per class under cyclic rotation) and a class table.
usage: walks.py Lmax outdir
"""
import sys, os, collections, json
sys.path.insert(0, os.path.expanduser('~/p196_run/mchk14'))
import ifscc
sys.setrecursionlimit(1000000)
Lmax = int(sys.argv[1]); out = sys.argv[2]
os.makedirs(out, exist_ok=True)
g = [1, 0] * 4
d = 8
states, adj, level = ifscc.build(g, d)
n = len(states)
succ = [sorted(set(a.values())) for a in adj]
comps = [c for c in ifscc.tarjan(n, succ) if len(c) > 1 or c[0] in succ[c[0]]]
comps.sort(key=len, reverse=True)
comp = comps[0]
print('nodes', n, 'comps', [len(c) for c in comps])
cs = set(comp)
order = {v: k for k, v in enumerate(sorted(comp))}
# edges inside the comp
edges = {v: [(col, w) for col, w in adj[v].items() if w in cs] for v in comp}
ne = sum(len(x) for x in edges.values())
print('edges in comp', ne)
# BFS tree head
par = {0: None}
q = collections.deque([0])
while q:
    v = q.popleft()
    for col, w in adj[v].items():
        if w not in par:
            par[w] = (v, col)
            q.append(w)
def head(v):
    p = []
    while par[v] is not None:
        u, col = par[v]
        p.append(col)
        v = u
    p.reverse()
    return p
# distance to each node inside the comp (reverse BFS) for pruning
rev = {v: [] for v in comp}
for v in comp:
    for col, w in edges[v]:
        rev[w].append(v)
def dist_to(s):
    dist = {s: 0}
    dq = collections.deque([s])
    while dq:
        x = dq.popleft()
        for y in rev[x]:
            if y not in dist:
                dist[y] = dist[x] + 1
                dq.append(y)
    return dist
found = {}  # canonical rotated word -> (s0, head node, word)
count_walks = collections.Counter()
for s0 in sorted(comp):
    dist = dist_to(s0)
    allowed = lambda v: order[v] >= order[s0]
    # iterative DFS over walks starting at s0 of length <= Lmax, allowed nodes >= s0 in order
    stack = [(s0, 0)]
    path = []  # labels
    nodes = [s0]
    # DFS with explicit recursion (depth <= Lmax)
    def dfs(v, L):
        for col, w in edges[v]:
            if order[w] < order[s0]:
                continue
            if L + 1 + dist.get(w, 10**9) > Lmax:
                continue
            path.append(col)
            if w == s0:
                # closed walk found
                word = tuple(path)
                m = len(word)
                # primitive?
                prim = True
                for p in range(1, m):
                    if m % p == 0 and word == word[:p] * (m // p):
                        prim = False
                        break
                if prim:
                    # canonical cyclic rotation
                    best = min(word[i:] + word[:i] for i in range(m))
                    if best not in found:
                        found[best] = (s0, word)
                    count_walks[m] += 1
            if L + 1 < Lmax:
                dfs(w, L + 1)
            path.pop()
    dfs(s0, 0)
print('primitive words (up to rotation):', len(found))
bylen = collections.Counter(len(k) for k in found)
print('by length', sorted(bylen.items()))
# write files for the words; name: wL_k
idx = collections.Counter()
index = []
for word in sorted(found, key=lambda w: (len(w), w)):
    s0, word0 = found[word]
    L = len(word)
    k = idx[L]; idx[L] += 1
    name = f'w{L}_{k}.txt'
    hd = head(s0)
    with open(os.path.join(out, name), 'w') as f:
        f.write(f'10 {d} {len(hd)} {L}\n')
        f.write(' '.join(map(str, g)) + '\n')
        for t in range(d):
            f.write(' '.join(str(c[t]) for c in hd) + '\n')
        for t in range(d):
            f.write(' '.join(str(c[t]) for c in word0) + '\n')
    index.append(name)
print('files', len(index))

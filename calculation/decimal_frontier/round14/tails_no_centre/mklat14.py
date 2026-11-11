#!/usr/bin/env python3
"""mklat14.py (main session, round 14 scoping): lattice files for the tails of the interface graph.
usage: mklat14.py G d outdir maxcycle
Writes one file per primitive simple cycle of length <= maxcycle of each non-trivial SCC (head = BFS path from the root); format of mc13b/mc13c lat files."""
import sys, os, collections
sys.setrecursionlimit(100000)
import ifscc

G = sys.argv[1]
d = int(sys.argv[2])
out = sys.argv[3]
maxc = int(sys.argv[4])
os.makedirs(out, exist_ok=True)
g = [int(ch) for ch in (G * (d // len(G) + 1))[:d]]
states, adj, level = ifscc.build(g, d)
n = len(states)
succ = [sorted(set(a.values())) for a in adj]
comps = [c for c in ifscc.tarjan(n, succ) if len(c) > 1 or c[0] in succ[c[0]]]
comps.sort(key=len, reverse=True)
# BFS tree from root
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


def write(name, hd, cyc):
    with open(os.path.join(out, name), 'w') as f:
        f.write(f'{ifscc.b} {d} {len(hd)} {len(cyc)}\n')
        f.write(' '.join(map(str, g)) + '\n')
        for t in range(d):
            f.write(' '.join(str(c[t]) for c in hd) + '\n')
        for t in range(d):
            f.write(' '.join(str(c[t]) for c in cyc) + '\n')


total = 0
for ci, comp in enumerate(comps):
    cs = set(comp)
    order = {v: k for k, v in enumerate(sorted(comp))}
    found = []
    seen_words = set()
    # simple cycles with smallest node as start (DFS bounded by maxc)
    for s0 in sorted(comp):
        path = []
        onp = set([s0])

        def dfs(v):
            if len(found) > 20000:
                return
            for col, w in adj[v].items():
                if w == s0:
                    if len(path) + 1 <= maxc:
                        found.append((s0, path + [col]))
                elif w in cs and order[w] > order[s0] and w not in onp and len(path) + 1 < maxc:
                    onp.add(w)
                    path.append(col)
                    dfs(w)
                    path.pop()
                    onp.discard(w)
        dfs(s0)
    bylen = collections.Counter(len(c) for s, c in found)
    print(f'SCC {ci}: nodes {len(comp)}: simple cycles <= {maxc}: {len(found)}; by length {sorted(bylen.items())}', flush=True)
    for k, (s0, cyc) in enumerate(sorted(found, key=lambda x: len(x[1]))):
        # primitive label word only
        L = len(cyc)
        if any(L % p == 0 and cyc == cyc[:p] * (L // p) for p in range(1, L)):
            continue
        name = f'b{ifscc.b}_{"p"+G if len(G)>4 else G}_d{d}_scc{ci}_len{L}_{k}.txt' if ifscc.b != 10 else f'{"p"+G if len(G)>4 else G}_d{d}_scc{ci}_len{L}_{k}.txt'
        write(name, head(s0), cyc)
        total += 1
print('files', total)

#!/usr/bin/env python3
"""Compare the cycles of my interface graph (clock 10, d=8) with the independent position automaton dump (bauto3 -dump sccdump.txt)."""
import collections, sys, os
sys.setrecursionlimit(100000)
import ifscc
L = int(sys.argv[1]) if len(sys.argv) > 1 else 128
G = '10'; d = 8
g = [int(ch) for ch in (G * (d // len(G) + 1))[:d]]
states, adj, level = ifscc.build(g, d)
n = len(states)
succ = [sorted(set(a.values())) for a in adj]
comps = [c for c in ifscc.tarjan(n, succ) if len(c) > 1 or c[0] in succ[c[0]]]
def canon(word):
    m = len(word)
    return min(tuple(word[i:] + word[:i]) for i in range(m))
def cycles(nodes, edges, L):
    """edges: dict node -> list of (col, target); returns the set of canonical primitive label words of simple cycles <= L"""
    order = {v: k for k, v in enumerate(sorted(nodes))}
    res = set()
    nset = set(nodes)
    for s0 in sorted(nodes):
        path = []
        onp = {s0}
        def dfs(v):
            for col, w in edges[v]:
                if w == s0:
                    if len(path) + 1 <= L:
                        res.add(canon(path + [col]))
                elif w in nset and order[w] > order[s0] and w not in onp and len(path) + 1 < L:
                    onp.add(w); path.append(col); dfs(w); path.pop(); onp.discard(w)
        dfs(s0)
    return res
mine = set()
for c in comps:
    e = {v: list(adj[v].items()) for v in c}
    mine |= cycles(c, e, L)
print('my interface graph: distinct cycle words (up to rotation) <=', L, ':', len(mine), sorted(collections.Counter(len(w) for w in mine).items()))
comps2 = []
cur = None
for line in open(os.path.join(os.environ.get('P196_H', '..'), 'mchk13b/sccdump.txt')):
    t = line.split()
    if not t:
        continue
    if t[0] == 'COMP':
        cur = collections.defaultdict(list); comps2.append(cur)
    elif t[0] == 'E':
        a, b = int(t[1]), int(t[2]); col = tuple(map(int, t[3:11]))
        cur[a].append((col, b)); cur[b]
other = set()
for c in comps2:
    other |= cycles(list(c.keys()), c, L)
print('bauto3 dump: distinct cycle words <=', L, ':', len(other), sorted(collections.Counter(len(w) for w in other).items()))
rev = set(canon(list(w)[::-1]) for w in other)
print('same set, same direction:', mine == other, '; same set, reversed direction:', mine == rev)
print('only mine (vs best direction):', len(mine - (other if len(mine & other) >= len(mine & rev) else rev)), ' only bauto:', len((other if len(mine & other) >= len(mine & rev) else rev) - mine))
base = other if len(mine & other) >= len(mine & rev) else rev
print('direction used:', 'same' if base is other else 'reversed')
extra = base - mine
core = set(v for c in comps for v in c)
closed = 0
for w in extra:
    ok = False
    for s in core:
        v = s
        for col in w:
            v = adj[v].get(col)
            if v is None:
                break
        if v == s:
            ok = True
            break
    closed += ok
print('words only in the bauto list:', len(extra), 'of which closed walks of my graph:', closed, '; lengths', sorted(set(len(w) for w in extra)))

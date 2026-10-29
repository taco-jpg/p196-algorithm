#!/usr/bin/env python3
"""Independent small control for the base-4 periodic position automaton.

No C++ code imported. Output is checked against bauto5 in test_bauto5_scc.sh.
"""
import sys

b = 4
g = tuple(map(int, "101100"))
p = len(g)
gi = [t for t in range(p) if g[t]]
yi = {t: i for i, t in enumerate(gi)}
root = (0, sum(bit << t for t, bit in enumerate(g)), tuple([1] * len(gi)))

def successors(state, first):
    low, high, Y = state
    found = set()
    for x0 in range(int(first), 2 * b - 1):
        xs, hn = [0] * p, [0] * p
        def walk(t, x):
            if first and x == 0:
                return
            for c in (0, 1):
                if (x + c) // b != (high >> t) & 1:
                    continue
                nxt = (x + ((low >> t) & 1)) % b
                nxt += Y[yi[t]] if g[t] else (x + c) % b
                xs[t], hn[t] = x, c
                if t + 1 < p:
                    walk(t + 1, nxt)
                elif nxt == x0:
                    L = sum(((xs[k] + ((low >> k) & 1)) // b) << k for k in range(p))
                    H = sum(hn[k] << k for k in range(p))
                    Z = tuple((xs[k] + hn[k]) % b for k in gi)
                    found.add((L, H, Z))
        walk(0, x0)
    return found

keys = [root]
index = {root: 0}
adj = []
for i, state in enumerate(keys):
    nxt = []
    for target in successors(state, i == 0):
        if target not in index:
            index[target] = len(keys)
            keys.append(target)
        nxt.append(index[target])
    adj.append(nxt)
    assert len(keys) <= 10000, "control unexpectedly large"

sys.setrecursionlimit(100000)
order = [-1] * len(keys)
lowlink = [-1] * len(keys)
stack = []
on = set()
number = 0
cycles = []
def visit(v):
    global number
    order[v] = lowlink[v] = number
    number += 1
    stack.append(v)
    on.add(v)
    for w in adj[v]:
        if order[w] < 0:
            visit(w)
            lowlink[v] = min(lowlink[v], lowlink[w])
        elif w in on:
            lowlink[v] = min(lowlink[v], order[w])
    if lowlink[v] == order[v]:
        comp = []
        while True:
            w = stack.pop()
            on.remove(w)
            comp.append(w)
            if w == v:
                break
        if len(comp) > 1 or any(w in adj[w] for w in comp):
            cycles.append(len(comp))
for v in range(len(keys)):
    if order[v] < 0:
        visit(v)

values = (len(keys), sum(map(len, adj)), len(cycles))
print(f"states={values[0]} edges={values[1]} nontrivial_sccs={values[2]}")
assert values == (957, 1012, 4), values

#!/usr/bin/env python3
"""r12f3: exhaustive analysis of the ROOT WINDOW automaton G_c (all window rows X in {0..18}^c, free inlet bit
b = beta_c(t), exact folded law with the root rule).  Self-contained (own step function, no SAT, no imports from
the other r12f encodings).
Part 1 (c = 1, column 0 only): P -> 2P+b (P <= 8, no overflow); P = 9: b=0 -> 18 (no overflow), b=1 -> 10
(overflow); P >= 10 -> P-9 (overflow).  Weight of a step w = 4*gamma - 1.  Prints the SCC of 10, ALL simple cycles
with their weights, a potential pi (Bellman-Ford from 10) with w(u->v) >= pi(v) - pi(u) for every edge inside the
SCC, and the tight edges (equality).  If no cycle has negative weight and the only cycle made of tight edges is the
reference cycle 10->1->2->5->10, then every closed walk 10 -> 10 of length N with exactly N/4 overflows (total
weight 0) uses only tight edges, hence is the reference cycle repeated: clock (1000)^(N/4).
Part 2 (c = 1..C): product G_c x Z_4 (phase t mod 4), start (s0,0), s0 = (B0 W0^inf)[0:c]; an edge leaving phase f
is STANDARD iff gamma = [f == 0].  Computes the SCC of (s0,0) (forward from (s0,0) intersected with backward) and
counts its non-standard edges.  If there are none, every return of the window to s0 (any length, any overflow
count, any inlet sequence) has the standard clock.
Usage: rootcycles.py C"""
import sys
from collections import deque
B0 = (10, 4, 6, 6, 7, 12, 9, 16, 16, 13, 0, 2, 10, 17, 7, 0, 18, 6, 5, 18, 4, 18, 14, 9, 14, 8, 12, 17, 10, 4, 6, 4, 0, 5)
W0 = (5, 18, 4, 8, 1, 15, 4, 0, 5)


def step(X, b):
    c = len(X); al = [0] * (c + 1); be = [0] * (c + 1); be[c] = b
    for i in range(c):
        al[i + 1] = 1 if X[i] + al[i] >= 10 else 0
    for i in range(c - 1, -1, -1):
        be[i] = 1 if X[i] + be[i + 1] >= 10 else 0
    g = be[0]
    lo = [(X[i] + al[i]) % 10 for i in range(c)]
    hi = [(X[i] + be[i + 1]) % 10 for i in range(c)]
    if g == 0:
        Y = tuple(lo[i] + hi[i] for i in range(c))
    else:
        Y = (lo[0] + 1,) + tuple(lo[i] + hi[i - 1] for i in range(1, c))
    return Y, g


def part1():
    succ = {P: sorted(set(step((P,), b) for b in (0, 1))) for P in range(19)}
    for P in range(19):
        print("  edge", P, "->", [(Y[0], g) for Y, g in succ[P]])
    fw = {10}; dq = deque([10])
    while dq:
        u = dq.popleft()
        for Y, g in succ[u]:
            if Y[0] not in fw:
                fw.add(Y[0]); dq.append(Y[0])
    bw = {10}; ch = True
    while ch:
        ch = False
        for u in range(19):
            if u not in bw and any(Y[0] in bw for Y, g in succ[u]):
                bw.add(u); ch = True
    scc = sorted(fw & bw)
    print("SCC of 10:", scc, " (not in SCC:", sorted(set(range(19)) - set(scc)), ")")
    E = {u: [(Y[0], 4 * g - 1, g) for Y, g in succ[u] if Y[0] in scc] for u in scc}
    cyc = set()

    def dfs(s, v, path, w):
        for u, wt, g in E[v]:
            if u == s:
                cyc.add((tuple(path), w + wt))
            elif u > s and u not in path:
                dfs(s, u, path + [u], w + wt)
    for s in scc:
        dfs(s, s, [s], 0)
    cyc = sorted(cyc, key=lambda z: z[1] / len(z[0]))
    print("simple cycles in the SCC:", len(cyc))
    for p, w in cyc:
        print("  weight %3d length %2d mean %+.3f  %s" % (w, len(p), w / len(p), p))
    zero = [p for p, w in cyc if w == 0]; neg = [p for p, w in cyc if w < 0]
    print("negative-weight cycles:", neg, " zero-weight cycles:", zero)
    pi = {u: (0 if u == 10 else 10 ** 9) for u in scc}
    for _ in range(len(scc) + 1):
        for u in scc:
            for v, wt, g in E[u]:
                if pi[u] + wt < pi[v]:
                    pi[v] = pi[u] + wt
    ok = all(wt >= pi[v] - pi[u] for u in scc for v, wt, g in E[u])
    tight = [(u, v) for u in scc for v, wt, g in E[u] if wt == pi[v] - pi[u]]
    print("potential pi (Bellman-Ford from 10):", pi)
    print("w(u->v) >= pi(v)-pi(u) on every SCC edge:", ok)
    print("tight edges:", tight)
    T = {u: [v for (a, v) in tight if a == u] for u in scc}
    tc = set()

    def dfs2(s, v, path):
        for u in T[v]:
            if u == s:
                tc.add(tuple(path))
            elif u > s and u not in path:
                dfs2(s, u, path + [u])
    for s in scc:
        dfs2(s, s, [s])
    print("cycles of tight edges:", sorted(tc))
    concl = ok and sorted(tc) == [(1, 2, 5, 10)] and not neg
    print("CONCLUSION part1:", "every closed walk 10->10 with N/4 overflows has clock (1000)^(N/4)" if concl
          else "NOT ESTABLISHED", flush=True)
    return concl


def part2(C):
    for c in range(1, C + 1):
        s0 = tuple((B0 + W0 * 20)[:c])
        start = (s0, 0)
        fw = {start}; dq = deque([start]); adj = {}
        while dq:
            u = dq.popleft(); X, f = u; out = []
            for b in (0, 1):
                Y, g = step(X, b); v = (Y, (f + 1) % 4); out.append((v, g))
                if v not in fw:
                    fw.add(v); dq.append(v)
            adj[u] = out
        radj = {}
        for u, out in adj.items():
            for v, g in out:
                radj.setdefault(v, []).append(u)
        bw = {start}; dq = deque([start])
        while dq:
            v = dq.popleft()
            for u in radj.get(v, []):
                if u not in bw:
                    bw.add(u); dq.append(u)
        scc = fw & bw
        ns = set((u, v) for u in scc for v, g in adj[u] if v in scc and g != (1 if u[1] == 0 else 0))
        print(f"c={c} s0={s0}: forward-reachable product states {len(fw)}, SCC of (s0,0) {len(scc)}, "
              f"non-standard edges inside the SCC {len(ns)}", flush=True)
        if not ns:
            print(f"CONCLUSION part2 c={c}: every return of the window [0,{c}) to s0 (any length, any count, any "
                  f"inlet) has the standard clock", flush=True)


if __name__ == "__main__":
    part1()
    part2(int(sys.argv[1]) if len(sys.argv) > 1 else 3)

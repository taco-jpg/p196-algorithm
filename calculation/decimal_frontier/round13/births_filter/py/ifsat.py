#!/usr/bin/env python3
"""ifsat.py: interface automaton of T-periodic heads (r13c).
Interface at level a: c[t] (forward carry into column a), xb[t] (digit of column a-1, only used at gamma=1 phases; -1 = root: part=1),
A[t] (allowed values of H_a, bitmask 1<<H), root flag (digit>=1 at column 0).
Successors: add one T-periodic column v(0..T-1) (closed T-walk of the relative level-1 graph).
Usage: ifsat.py g T [maxstates]
Prints BFS levels: new states per level until saturation."""
import sys, collections
b = 10

def col_succ(g, T, st):
    c, xb, A, root = st
    res = []
    n = len(c)
    # DFS over closed T-walks of the single column
    # successors of (t, v): list of y values reachable (dedupe parallel)
    def step(t, v):
        ys = {}
        for h in (0, 1):
            H = (v + h) // b
            if not (A[t] >> H) & 1: continue
            if g[t]:
                part = 1 if xb[t] == -1 else (xb[t] + H) % b
            else:
                part = (v + h) % b
            y = (v + c[t]) % b + part
            ys.setdefault(y, 0)
            ys[y] |= (1 << h)
        return ys
    starts = range(1, 19) if root else range(0, 19)
    path = [0] * (T + 1)
    out = []
    def dfs(t):
        if t == T:
            if path[T] == path[0]:
                out.append(tuple(path[:T]))
            return
        for y in step(t, path[t]):
            if y < 0 or y > 2 * b - 2: continue
            path[t + 1] = y
            dfs(t + 1)
    for v0 in starts:
        path[0] = v0
        dfs(0)
    return out

def succ_iface(g, T, st, col):
    c, xb, A, root = st
    cn = [0] * T; xn = [0] * T; An = [0] * T
    for t in range(T):
        v = col[t]; vnext = col[(t + 1) % T]
        cn[t] = (v + c[t]) // b
        xn[t] = v if g[t] else 0
        mask = 0
        for h in (0, 1):
            H = (v + h) // b
            if not (A[t] >> H) & 1: continue
            part = (1 if xb[t] == -1 else (xb[t] + H) % b) if g[t] else (v + h) % b
            y = (v + c[t]) % b + part
            if y == vnext: mask |= (1 << h)
        An[t] = mask
    return (tuple(cn), tuple(xn), tuple(An), False)

def main():
    gw = sys.argv[1]; T = int(sys.argv[2]); cap = int(sys.argv[3]) if len(sys.argv) > 3 else 10**7
    g = [int(ch) for ch in (gw * (T // len(gw) + 1))[:T]]
    root = (tuple([0]*T), tuple([-1]*T), tuple(1 << g[t] for t in range(T)), True)
    seen = {root: 0}; frontier = [root]; level = 0
    ncols = 0
    while frontier and len(seen) < cap:
        nxt = []
        for st in frontier:
            for col in col_succ(g, T, st):
                ncols += 1
                s2 = succ_iface(g, T, st, col)
                if s2 not in seen:
                    seen[s2] = level + 1
                    nxt.append(s2)
        level += 1
        print(f"level {level}: new={len(nxt)} total={len(seen)} cols={ncols}", flush=True)
        frontier = nxt
    print(f"SAT g={gw} T={T} states={len(seen)} a0={level-1 if not frontier else 'CAP'} cols={ncols}")
main()

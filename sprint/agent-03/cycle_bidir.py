#!/usr/bin/env python3
"""Find a forward cycle through a word of the k-column abstraction by bidirectional BFS.

forward side : w -> forward_prefix(w, e), e in {0,1}
backward side: p -> prefix_predecessors(p)   (the repo's executable inverse; every edge is
               re-checked with forward_prefix before it is used)
Usage: cycle_bidir.py K DEPTH_FWD DEPTH_BWD w_0 ... w_{K-1}
Prints the cycle length and the carry list (input for Lean `cycleOK`), or 'none'.
"""
import sys

sys.path.insert(0, __import__("os").path.dirname(__file__))
from fwdref import forward_prefix, prefix_predecessors  # noqa: E402


def find_cycle(w, dfw, dbw):
    w = tuple(w)
    fpar = {w: None}           # word -> (prev word, carry)
    frontier = [w]
    for _ in range(dfw):
        nxt = []
        for u in frontier:
            for e in (0, 1):
                v = tuple(forward_prefix(list(u), e))
                if v not in fpar:
                    fpar[v] = (u, e)
                    nxt.append(v)
        frontier = nxt
    # backward BFS from w; bpar[x] = (next word toward w, carry used x -> next)
    bpar = {w: None}
    frontier = [w]
    best = None
    for depth in range(dbw + 1):
        # check meeting: a word x in fpar (reached from w) that is a strict predecessor-chain start
        for x in frontier:
            if x in fpar and (x != w or depth > 0):
                # length = dist_f(x) + depth
                df = 0
                y = x
                while fpar[y] is not None:
                    y = fpar[y][0]
                    df += 1
                if df + depth > 0 and (best is None or df + depth < best[0]):
                    best = (df + depth, x)
        if best is not None or depth == dbw:
            break
        nxt = []
        for p in frontier:
            for s in prefix_predecessors(list(p)):
                s = tuple(s)
                if len(s) != len(w) or s[0] == 0:
                    continue
                es = [e for e in (0, 1) if tuple(forward_prefix(list(s), e)) == p]
                assert es, "inverse edge not confirmed by forward map"
                if s not in bpar:
                    bpar[s] = (p, es[0])
                    nxt.append(s)
        frontier = nxt
    if best is None:
        return None
    _, x = best
    # forward part w -> x
    fwd_part = []
    y = x
    while fpar[y] is not None:
        u, e = fpar[y]
        fwd_part.append(e)
        y = u
    fwd_part.reverse()
    # backward part x -> w
    bwd_part = []
    y = x
    while bpar[y] is not None:
        p, e = bpar[y]
        bwd_part.append(e)
        y = p
    carries = fwd_part + bwd_part
    # verify
    v = list(w)
    for e in carries:
        v = forward_prefix(v, e)
    assert tuple(v) == w and len(carries) > 0
    return carries


if __name__ == "__main__":
    k, dfw, dbw = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    w = [int(x) for x in sys.argv[4:4 + k]]
    c = find_cycle(w, dfw, dbw)
    if c is None:
        print("none")
    else:
        print(len(c), "[" + ",".join(map(str, c)) + "]")

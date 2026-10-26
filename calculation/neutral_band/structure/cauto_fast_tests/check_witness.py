#!/usr/bin/env python3
"""Independent check of every witness in a cauto output file (python re-implementation of the C step, from ctest.py)."""
import re, sys
def cstep(b, C, e1, g, v):
    m = len(C); c = e1; DC = []
    for x in C:
        DC.append((x + c) % b); c = (x + c) // b
    if c != 1 - e1: return None
    yd = (b - 1) * e1
    if g == 0: cp = [DC[k] + DC[m - 1 - k] for k in range(m)]
    else:
        W = DC + [yd]; cp = [W[k] + W[m - k] for k in range(m + 1)]
    n = len(cp)
    if v:
        if n - 2 * v < 1: return None
        if any(x != b - 1 for x in cp[:v]) or any(x != b - 1 for x in cp[n - v:]): return None
        cp = cp[v:n - v]
    return cp
n = ok = nowit = 0
for line in open(sys.argv[1]):
    if not line.startswith('FEASIBLE'): continue
    n += 1
    mt = re.match(r"FEASIBLE(?:_CLASS)? b=(\d+) e=(\d+) g=(\d+) v=(\d+) m0=(\d+)", line)
    b = int(mt[1]); e = [int(x) for x in mt[2]]; g = [int(x) for x in mt[3]]; v = [int(x) for x in mt[4]]
    Cs = [[int(x) for x in m.split(',')] for m in re.findall(r" C\d+=\[([^\]]*)\]", line)]
    if not Cs: nowit += 1; continue
    P = len(e); good = len(Cs) == P and all(c == c[::-1] and all(0 <= x <= 2 * b - 2 for x in c) for c in Cs)
    for t in range(P):
        if not good: break
        nx = cstep(b, Cs[t], e[t], g[t], v[t])
        if nx != Cs[(t + 1) % P]: good = False
    ok += good
print(f"{sys.argv[1]}: FEASIBLE lines {n}, with witness {n - nowit}, witnesses valid {ok}")
sys.exit(0 if ok == n - nowit else 1)

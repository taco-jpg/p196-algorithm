#!/usr/bin/env python3
"""Run the Python reference (klib.window_step, incr-style SCC, exact centre check) on a 9-wire with a fixed stream:
a period-1 'lattice' of 9s whose upward carry is the stream bit and downward carry its complement."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "decimal_frontier", "lattice_kinks", "edge_relaxation"))
import klib
from klib import window_step
clock, stream, K0file, K0, Kmax = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5])
p = len(clock)
class WireLat:
    def __init__(s):
        s.name = 'wire'; s.g = [int(ch) for ch in clock]; s.p = p; s.nB = 0; s.m = 1
    def cell(s, t, x): return 9
    def row(s, t, L): return [9] * L
lat = WireLat()
st = [int(ch) for ch in stream]
klib.bulk_up_carry = lambda lat_, t, x: st[t % p]
klib.bulk_up_carry_any = lambda lat_, t, x: st[t % p]
klib.bulk_down_carry = lambda lat_, t, x: 1 - st[t % p]
klib.bulk_e = lambda lat_, t, x: (9 + st[t % p]) % 10
klib.bulk_r = lambda lat_, t, x: (9 + 1 - st[t % p]) % 10
c0 = 1000
def nxt(ph):
    t, j, par = ph; g = lat.g[t]; dh = 1 if (g == 1 and par == 0) else 0
    return ((t + 1) % p, 0, (par + g) % 2), dh
def acc(v): return v[1][0] != 9
data = open(K0file, 'rb').read(); NW = 19 ** K0
Cyc = []
for i in range(0, len(data), 16):
    k = int.from_bytes(data[i:i + 16], 'little'); ph = k >> 100; par = ph % 2; ph //= 2; t = ph   # m = 1 -> j = 0
    Cyc.append(((t, 0, par), tuple((k >> (5 * q)) & 31 for q in range(K0))))
sys.setrecursionlimit(10**6)
def scc(nodes, E):
    index = {}; low = {}; onst = set(); stck = []; comps = []; idx = 0
    for root in nodes:
        if root in index: continue
        index[root] = low[root] = idx; idx += 1; stck.append(root); onst.add(root); work = [(root, iter(E[root]))]
        while work:
            v, it = work[-1]; adv = False
            for w in it:
                if w not in index:
                    index[w] = low[w] = idx; idx += 1; stck.append(w); onst.add(w); work.append((w, iter(E[w]))); adv = True; break
                elif w in onst and index[w] < low[v]: low[v] = index[w]
            if adv: continue
            work.pop()
            if work:
                u = work[-1][0]
                if low[v] < low[u]: low[u] = low[v]
            if low[v] == index[v]:
                comp = []
                while True:
                    w = stck.pop(); onst.discard(w); comp.append(w)
                    if w == v: break
                comps.append(comp)
    return comps
print(f'wire clock={clock} stream={stream}: |Cyc({K0})|={len(Cyc)} accepting {sum(acc(v) for v in Cyc)}')
for K in range(K0 + 1, Kmax + 1):
    cand = set((ph, w + (x,)) for (ph, w) in Cyc for x in range(19)); E = {}
    for v in cand:
        (t, j, par), win = v; ph2, dh = nxt((t, j, par)); outs = set()
        for Din in (0, 1):
            for gh in (range(10) if dh else [0]):
                new, ok = window_step(lat, t, c0, 1000 + par, list(win), Din, gh)
                if ok and (ph2, tuple(new)) in cand: outs.add((ph2, tuple(new)))
        E[v] = outs
    comps = scc(list(cand), E)
    cyc = [c for c in comps if len(c) > 1 or c[0] in E[c[0]]]
    Cyc = [v for c in cyc for v in c]
    print(f'K={K}: cyclic {len(Cyc)}, accepting {sum(acc(v) for v in Cyc)}', flush=True)
    # exact centre check inside Cyc(K)
    S = set(Cyc); succ = {}
    for (ph, w) in S:
        t, j, par = ph; n = 2 * (c0 + K) - par
        a = [st[t]]
        for v in w: a.append((v + a[-1]) // 10)
        Din = a[K] if par == 0 else a[K - 1]; gh = (w[K - 1] + Din) % 10
        new, ok = window_step(lat, t, c0, n, list(w), Din, gh)
        v2 = (nxt(ph)[0], tuple(new))
        if ok and v2 in S: succ[(ph, w)] = v2
    seen = {}; cycles = 0
    for v in succ:
        if v in seen: continue
        path = []; x = v
        while x in succ and x not in seen: seen[x] = 'g'; path.append(x); x = succ[x]
        if x in seen and seen[x] == 'g': cycles += 1
        for y in path: seen[y] = 'b'
    print(f'      exact centre cycles inside Cyc({K}): {cycles}', flush=True)

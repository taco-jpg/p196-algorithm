#!/usr/bin/env python3
"""r11f chain 8: K-head lifting for a fixed overflow clock G (Agent120 exterior head, same rule as
calculation/decimal_frontier/exterior_census/py/khead_family.py and issue #481 PRO-R01-d-8a07).
Vertex = (phase mod |G|, x_0..x_{K-1}), x_0 in 1..B*2-2 (root digit >= 1), x_i in 0..2B-2.
Edge for each upper carry h in {0,1}: backward carries H_K=h, H_i=(x_i+H_{i+1})//B, overflow g=H_0 must equal G[phase];
forward carries L_0=0; daughter y_i=(x_i+L_i)%B + (g ? (i==0 ? 1 : (x_{i-1}+H_i)%B) : (x_i+H_{i+1})%B).
Every closed walk at width K+1 projects to a closed walk at width K (truncation is a graph map), and a 9-padded finite periodic
exterior gives a closed walk at every K. So: S_K = vertices of cyclic SCCs that contain a ROOT vertex (phase ph0, prefix = root)
[mode 'root'], lifted K -> K+1 by appending all 2B-1 digits. If S_K is empty, no periodic exterior with clock G^omega, ANY period,
ANY width, has that phase-ph0 prefix.  Mode 'all': S_K = all cyclic vertices (no root restriction), for reproducing the census.
usage: khead_root.py G K_max mode [root e.g. 9,17,5] [ph0] [B]"""
import sys, math
sys.setrecursionlimit(1000000)
G = [int(c) for c in sys.argv[1]]; P = len(G); Kmax = int(sys.argv[2]); mode = sys.argv[3]
root = tuple(int(v) for v in sys.argv[4].split(',')) if len(sys.argv) > 4 and sys.argv[4] != '-' else ()
ph0 = int(sys.argv[5]) if len(sys.argv) > 5 else 0; B = int(sys.argv[6]) if len(sys.argv) > 6 else 10
NX = 2 * B - 1
def trans(x, h):
    K = len(x); H = [0] * (K + 1); H[K] = h
    for i in range(K - 1, -1, -1): H[i] = (x[i] + H[i + 1]) // B
    g = H[0]; L = 0; y = []
    for i in range(K):
        part = (1 if i == 0 else (x[i - 1] + H[i]) % B) if g else (x[i] + H[i + 1]) % B
        y.append((x[i] + L) % B + part); L = (x[i] + L) // B
    return tuple(y), g
def sccs(nodes, out):
    idx = {}; low = {}; st = []; on = set(); comps = []; cnt = 0
    for v0 in nodes:
        if v0 in idx: continue
        stack = [(v0, iter(out.get(v0, ())))]; idx[v0] = low[v0] = cnt; cnt += 1; st.append(v0); on.add(v0)
        while stack:
            u, it = stack[-1]; adv = False
            for w in it:
                if w not in idx:
                    idx[w] = low[w] = cnt; cnt += 1; st.append(w); on.add(w); stack.append((w, iter(out.get(w, ())))); adv = True; break
                elif w in on: low[u] = min(low[u], idx[w])
            if adv: continue
            stack.pop()
            if stack: low[stack[-1][0]] = min(low[stack[-1][0]], low[u])
            if low[u] == idx[u]:
                comp = []
                while True:
                    w = st.pop(); on.discard(w); comp.append(w)
                    if w == u: break
                if len(comp) > 1 or comp[0] in out.get(comp[0], ()): comps.append(comp)
    return comps
def period(comp, out):
    cs = set(comp); r = comp[0]; dist = {r: 0}; q = [r]; gg = 0
    for u in q:
        for w in out.get(u, ()):
            if w not in cs: continue
            if w not in dist: dist[w] = dist[u] + 1; q.append(w)
            else: gg = math.gcd(gg, dist[u] + 1 - dist[w])
    return gg
def isroot(v):
    ph, x = v
    return ph == ph0 and x[:len(root)] == root
S = None
for K in range(1, Kmax + 1):
    if K == 1: nodes = [(ph, (x,)) for ph in range(P) for x in range(1, NX)]
    else: nodes = [(ph, x + (d,)) for (ph, x) in S for d in range(NX)]
    nodeset = set(nodes); out = {}; arcs = 0
    for v in nodes:
        ph, x = v; lst = []
        for h in (0, 1):
            y, g = trans(x, h)
            if g == G[ph]:
                w = ((ph + 1) % P, y)
                if w in nodeset and w not in lst: lst.append(w)
        if lst: out[v] = lst; arcs += len(lst)
    comps = sccs(nodes, out)
    if mode == 'root' and K >= len(root): comps = [c for c in comps if any(isroot(v) for v in c)]
    elif mode == 'root': comps = [c for c in comps if any(v[0] == ph0 and root[:K] == v[1] for v in c)]
    S = [v for c in comps for v in c]
    info = sorted([(len(c), period(c, out)) for c in comps], reverse=True)
    nroot = sum(1 for v in S if v[0] == ph0 and v[1][:len(root)] == root) if root else 0
    ph0pre = sorted(set(v[1][:3] for v in S if v[0] == ph0)) if K <= 3 else None
    print(f'K={K}: candidates {len(nodes)} arcs {arcs} | core {len(S)} (root vertices {nroot}) SCCs(size,period) {info[:6]}{" ..." if len(info) > 6 else ""}'
          + (f' phase-{ph0} prefixes {ph0pre}' if ph0pre is not None and len(ph0pre) < 40 else ''), flush=True)
    if K == 3 and mode == 'root':
        for c in comps:
            third = {}
            for (ph, x) in c: third.setdefault(ph, set()).add(x)
            print('  K3 root SCC per phase:', {ph: sorted(third[ph]) for ph in sorted(third)}, flush=True)
    if not S:
        print(f'=> core EMPTY at K={K}'); break
    if K == Kmax:
        # dump the third-coordinate profile and a sample cycle
        prof = {}
        for (ph, x) in S:
            if len(x) >= 3: prof.setdefault(ph, set()).add(x[2])
        print('third-coordinate values per phase:', {ph: sorted(prof[ph]) for ph in sorted(prof)})

#!/usr/bin/env python3
"""r12e: spines of a khxt -anc / -coreproj dump (ancestor windows at one level k), for a primitive word with L = P.
1. transition graph between ancestor windows of consecutive phases (z[:k-MARGIN] == trans(x, h)[:k-MARGIN], label H_0 = g_t);
2. closed P-walks of that graph (= the spines, if the graph is a union of cycles);
3. for each spine the reach interface I_c = (c_c(t), delta_c(t), rho_c(t) at overflow times) at every cut c <= k-MARGIN
   (backward carries from the digits; determined below the topmost non-9 digit); repeated interfaces I_c = I_d are reported
   (a repeat = a cycle of the reach graph = a position-periodic infinite exterior);
4. position-periodicity of the cell columns (vectors over time) of each spine.
usage: spine_iface.py DUMP WORD [MARGIN=40]"""
import sys, collections
fn, word = sys.argv[1], sys.argv[2]; MARGIN = int(sys.argv[3]) if len(sys.argv) > 3 else 40
b = 10; g = [int(c) for c in word]; P = len(g)
W = collections.defaultdict(list)
for l in open(fn):
    if l.startswith('#') or l.startswith('ANC') or ':' not in l: continue
    h, xs = l.split(':'); t = int(h.split()[1]); W[t].append([int(v) for v in xs.split()])
k = len(W[0][0]); kk = k - MARGIN
def trans(x, hbit):
    K = len(x); H = [0] * (K + 1); H[K] = hbit
    for i in range(K - 1, -1, -1): H[i] = (x[i] + H[i + 1]) // b
    gg = H[0]; Lc = [0] * (K + 1)
    for i in range(K): Lc[i + 1] = (x[i] + Lc[i]) // b
    y = [((x[i] + Lc[i]) % b) + ((1 if i == 0 else (x[i - 1] + H[i]) % b) if gg else (x[i] + H[i + 1]) % b) for i in range(K)]
    return y, gg
nw = sum(len(W[t]) for t in range(P))
print(f"level {k}: {nw} ancestor windows, per phase {[len(W[t]) for t in range(P)]}; comparing the lowest {kk} digits")
E = {}
for t in range(P):
    t1 = (t + 1) % P
    for i, x in enumerate(W[t]):
        tg = set()
        for hb in (0, 1):
            y, gg = trans(x, hb)
            if gg != g[t]: continue
            for j, z in enumerate(W[t1]):
                if z[:kk] == y[:kk]: tg.add(j)
        E[(t, i)] = sorted(tg)
print("out-degree histogram:", dict(collections.Counter(len(v) for v in E.values())))
if nw > 6 * P: print("too many windows for walk enumeration"); sys.exit()
spines = []
def dfs(t, i, path):
    if t == P:
        if i == path[0]: spines.append(list(path[:-1]))
        return
    for j in E.get((t, i), []):
        path.append(j); dfs(t + 1, j, path); path.pop()
for i0 in range(len(W[0])): dfs(0, i0, [i0])
print(f"closed {P}-walks through phase 0: {len(spines)}")
for si, sp in enumerate(spines[:8]):
    cols = [W[t][sp[t]] for t in range(P)]
    # forward carries Lf[t][c] (into position c) and backward carries Hb[t][c] (None above the topmost non-9 digit)
    Lf = []; Hb = []
    for t in range(P):
        x = cols[t]; L = [0] * (k + 1)
        for i in range(k): L[i + 1] = (x[i] + L[i]) // b
        Lf.append(L)
        top = max((i for i in range(k) if x[i] != 9), default=-1)
        H = [None] * (k + 1)
        if top >= 0:
            H[top] = 1 if x[top] >= b else 0
            for i in range(top - 1, -1, -1): H[i] = (x[i] + H[i + 1]) // b
        Hb.append(H)
    assert all(Hb[t][0] == g[t] for t in range(P)), "label check failed"
    seen = {}; rep = None; last = 0
    for c in range(1, kk):
        if any(Hb[t][c] is None for t in range(P)): break
        key = (tuple(Lf[t][c] for t in range(P)), tuple(Hb[t][c] for t in range(P)), tuple((cols[t][c - 1] + Hb[t][c]) % b for t in range(P) if g[t]))
        if key in seen and rep is None: rep = (seen[key], c)
        seen.setdefault(key, c); last = c
    colper = None
    for q in range(1, kk // 2):
        if all(cols[t][i] == cols[t][i + q] for t in range(P) for i in range(kk // 2, kk - q)): colper = q; break
    print(f"spine {si}: phase-0 digits 40..64: {' '.join(map(str, cols[0][40:64]))}")
    print(f"   interfaces at cuts 1..{last}: {len(seen)} distinct; first repeat (c, d): {rep}; column period on [{kk//2},{kk}): {colper}")
    print(f"   9-fraction of digits on [100,{kk}): {sum(cols[t][i] == 9 for t in range(P) for i in range(100, kk)) / (P * max(1, kk - 100)):.3f}")

#!/usr/bin/env python3
"""r13b pylevels.py: Python verification (reference rule klib.window_step, explicit reachability) of the E_acc level step.
Input: E_acc(K-1) file (C++ eset3). Computes E_acc(K,T) from candidates E_acc(K-1) x {0..18} in pure Python
(closed T-walks through an accepting state, explicit set-based forward/backward with an 'accepting seen' flag) and compares
with the C++ E_acc(K) file (if it exists).  usage: pylevels.py NAME ORBIT L K DIR"""
import sys, struct, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../lattice_kinks/edge_relaxation'))
from klib import load, window_step
name, oi, LL, K, d = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
lat = load(name); P = lat.p; M = lat.m
def nxt(t, j, par):
    g = lat.g[t]; dh = 1 if (g == 1 and par == 0) else 0
    return (t + 1) % P, (j + dh) % M, (par + g) % 2
NPH = 2 * P * M; seen = {}; reps = []
for s in range(NPH):
    if s in seen: continue
    reps.append(s); t, j, par = (s // 2) // M, (s // 2) % M, s % 2; x = s
    while True:
        seen[x] = len(reps) - 1; t, j, par = nxt(t, j, par); x = (t * M + j) * 2 + par
        if x == s: break
s = reps[oi]; Ph = []; t, j, par = (s // 2) // M, (s // 2) % M, s % 2
while True:
    Ph.append((t, j, par)); t, j, par = nxt(t, j, par)
    if (t, j, par) == Ph[0]: break
Lo = len(Ph); T = LL * Lo; base = lat.nB + 5 * lat.m
def readset(fn, K):
    f = open(fn, 'rb'); lo, W = struct.unpack('ii', f.read(8)); assert lo == Lo
    R = []
    for l in range(Lo):
        n = struct.unpack('Q', f.read(8))[0]; data = f.read(8 * W * n); S = set()
        for i in range(n):
            words = struct.unpack_from('<%dQ' % W, data, 8 * W * i)
            S.add(tuple((words[q // 12] >> (5 * (q % 12))) & 31 for q in range(K)))
        R.append(S)
    return R
t0 = time.time()
Eprev = readset(f'{d}/E_K{K-1}.bin', K - 1)
cand = [[p + (x,) for p in Eprev[l] for x in range(19)] for l in range(Lo)]
candS = [set(c) for c in cand]
print(f'K={K}: parents {sum(len(x) for x in Eprev)} candidates {sum(len(c) for c in cand)}', flush=True)
def succ(l, w):
    t, j, par = Ph[l]; dh = 1 if (lat.g[t] == 1 and par == 0) else 0; c = base + j; n = 100 + par; res = set()
    for Din in (0, 1):
        for gh in (range(10) if dh else [0]):
            new, ok = window_step(lat, t, c, n, list(w), Din, gh)
            if ok:
                v = tuple(new)
                if v in candS[(l + 1) % Lo]: res.add(v)
    return res
adj = [{w: succ(l, w) for w in cand[l]} for l in range(Lo)]
print('edges built', sum(sum(len(v) for v in adj[l].values()) for l in range(Lo)), f'{time.time()-t0:.0f}s', flush=True)
# trim
alive = [set(cand[l]) for l in range(Lo)]
ch = True
while ch:
    ch = False
    for l in range(Lo):
        nl = (l + 1) % Lo; hasin = set()
        for w in list(alive[l]):
            ss = [v for v in adj[l][w] if v in alive[nl]]
            if not ss: alive[l].discard(w); ch = True
            hasin.update(ss)
        rem = alive[nl] - hasin
        if rem: alive[nl] -= rem; ch = True
acc = [{w for w in alive[l] if w[0] != lat.cell(Ph[l][0], base + Ph[l][1])} for l in range(Lo)]
anc = min(range(Lo), key=lambda l: (len(alive[l]) if alive[l] else 10**18))
Enew = [set() for _ in range(Lo)]
if alive[anc]:
    for s in alive[anc]:
        F0 = [set() for _ in range(T + 1)]; F1 = [set() for _ in range(T + 1)]
        (F1 if s in acc[anc] else F0)[0].add(s)
        for k in range(T):
            l = (anc + k) % Lo; nl = (l + 1) % Lo; last = (k + 1 == T)
            for x in F0[k]:
                for y in adj[l][x]:
                    if y not in alive[nl]: continue
                    if (not last) and (y in acc[nl]): F1[k + 1].add(y)
                    else: F0[k + 1].add(y)
            for x in F1[k]:
                for y in adj[l][x]:
                    if y in alive[nl]: F1[k + 1].add(y)
        if s not in F1[T]: continue
        B0 = [set() for _ in range(T + 1)]; B1 = [set() for _ in range(T + 1)]; B0[T].add(s)
        for k in range(T - 1, -1, -1):
            l = (anc + k) % Lo; nl = (l + 1) % Lo; last = (k + 1 == T)
            for x in alive[l]:
                z0 = z1 = False
                for y in adj[l][x]:
                    if y not in alive[nl]: continue
                    if (not last) and (y in acc[nl]):
                        if y in B0[k + 1] or y in B1[k + 1]: z1 = True
                    else:
                        if y in B0[k + 1]: z0 = True
                        if y in B1[k + 1]: z1 = True
                if z0: B0[k].add(x)
                if z1: B1[k].add(x)
        for k in range(T):
            l = (anc + k) % Lo
            Enew[l] |= (F1[k] & (B0[k] | B1[k])) | (F0[k] & B1[k])
tot = sum(len(x) for x in Enew); print(f'K={K}: Python E_acc = {tot}  accepting {sum(len(x & acc[l]) for l, x in enumerate(Enew))}  ({time.time()-t0:.0f}s)')
import os
fn = f'{d}/E_K{K}.bin'
if os.path.exists(fn):
    C = readset(fn, K); same = all(C[l] == Enew[l] for l in range(Lo))
    print(f'K={K}: C++ file E_acc = {sum(len(x) for x in C)}  SETS {"EQUAL" if same else "DIFFER"}')
else:
    print(f'K={K}: no C++ file (C++ reports EMPTY) ; Python total {tot} => {"EMPTY agrees" if tot == 0 else "PYTHON NON-EMPTY: DIFFERENCE"}')

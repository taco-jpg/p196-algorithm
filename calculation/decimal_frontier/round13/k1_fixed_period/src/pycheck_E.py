#!/usr/bin/env python3
import os
"""r13b pycheck_E.py: independent computation of E(K,T) for small K with the repo's reference rule klib.window_step
(different code from kcommon.h wstep; Python, explicit tuples, explicit closed-walk search by forward/backward reachability
through the T unrolled layers). Compares the set E(K,T) with an eset2 E_K file if given.
usage: pycheck_E.py NAME ORBIT L KMAX [EDIR] [EACCDIR]  (NAME = rec0|rec1|rec2)"""
import sys, struct, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../lattice_kinks/edge_relaxation'))
import klib
from klib import load, window_step
name, oi, LL, Kmax = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
edir = sys.argv[5] if len(sys.argv) > 5 and sys.argv[5] != '-' else None
eacc = sys.argv[6] if len(sys.argv) > 6 else None
lat = load(name); P = lat.p; M = lat.m
# phases, orbit order (same convention as kcommon: phase id (t*M+j)*2+par, orbits by smallest id)
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
Lo = len(Ph); T = LL * Lo
base = lat.nB + 5 * lat.m
def succs(l, w):
    t, j, par = Ph[l]; dh = 1 if (lat.g[t] == 1 and par == 0) else 0
    c = base + j; n = 100 + par
    res = set()
    for Din in (0, 1):
        for gh in (range(10) if dh else [0]):
            new, ok = window_step(lat, t, c, n, list(w), Din, gh)
            if ok: res.add(tuple(new))
    return res
E = [{()} for _ in range(Lo)]
t0 = time.time()
for K in range(1, Kmax + 1):
    cand = [{p + (x,) for p in E[l] for x in range(19)} for l in range(Lo)]
    # graph on candidates
    adj = [{} for _ in range(Lo)]
    for l in range(Lo):
        nl = (l + 1) % Lo
        for w in cand[l]:
            adj[l][w] = [v for v in succs(l, w) if v in cand[nl]]
    # trim to bi-infinite core
    alive = [set(cand[l]) for l in range(Lo)]
    changed = True
    while changed:
        changed = False
        for l in range(Lo):
            nl = (l + 1) % Lo
            hasin = set()
            for w in alive[l]:
                for v in adj[l][w]:
                    if v in alive[nl]: hasin.add(v)
            na = {w for w in alive[l] if any(v in alive[nl] for v in adj[l][w])}
            if len(na) != len(alive[l]): changed = True; alive[l] = na
            nb = alive[nl] & hasin
            if len(nb) != len(alive[nl]): changed = True; alive[nl] = nb
    # anchor: first layer with smallest size
    anc = min(range(Lo), key=lambda l: len(alive[l]))
    # reverse adjacency
    rev = [{} for _ in range(Lo)]
    for l in range(Lo):
        nl = (l + 1) % Lo
        for w in alive[l]:
            for v in adj[l][w]:
                if v in alive[nl]:
                    rev[nl].setdefault(v, []).append(w)
    Enew = [set() for _ in range(Lo)]
    for s in alive[anc]:
        Fs = [{s}]
        for k in range(T):
            l = (anc + k) % Lo; nl = (l + 1) % Lo; R = set()
            for x in Fs[-1]:
                for y in adj[l][x]:
                    if y in alive[nl]: R.add(y)
            Fs.append(R)
        if s not in Fs[T]: continue
        Bs = [None] * (T + 1); Bs[T] = {s}
        for k in range(T - 1, -1, -1):
            nl = (anc + k + 1) % Lo; R = set()
            for y in Bs[k + 1]:
                for x in rev[nl].get(y, []): R.add(x)
            Bs[k] = R
        for k in range(T):
            Enew[(anc + k) % Lo] |= (Fs[k] & Bs[k])
    Etot = sum(len(x) for x in Enew)
    msg = f'K={K} candidates={sum(len(c) for c in cand)} core={sum(len(a) for a in alive)} anchor={len(alive[anc])} E={Etot} t={time.time()-t0:.0f}s'
    # compare with eset2 file
    if edir:
        fn = f'{edir}/E_K{K}.bin'
        try:
            f = open(fn, 'rb'); lo, W = struct.unpack('ii', f.read(8)); assert lo == Lo
            same = True; tot = 0
            for l in range(Lo):
                n = struct.unpack('Q', f.read(8))[0]; data = f.read(8 * W * n)
                got = set()
                for i in range(n):
                    words = struct.unpack_from('<%dQ' % W, data, 8 * W * i); cells = tuple((words[q // 12] >> (5 * (q % 12))) & 31 for q in range(K))
                    got.add(cells)
                if got != Enew[l]:
                    same = False
                tot += n
            msg += f' | eset2 file E={tot} SETS {"EQUAL" if same and tot == Etot else "DIFFER"}'
        except FileNotFoundError:
            msg += ' | (no file)'
    print(msg, flush=True)
    E = Enew
    # ---- E_acc: closed T-walks through an accepting state (bottom cell off lattice), from the full E(K) graph
    A = [set() for _ in range(Lo)]
    for l in range(Lo):
        t, j, par = Ph[l]
        lv = lat.cell(t, base + j)
        for w in Enew[l]:
            if w[0] != lv: A[l].add(w)
    EnewAcc = [set() for _ in range(Lo)]
    for s in Enew[anc]:
        # forward DP (flag = accepting seen among steps 0..k)
        F0 = [{}, ]; F0 = [set() for _ in range(T + 1)]; F1 = [set() for _ in range(T + 1)]
        (F1 if s in A[anc] else F0)[0].add(s)
        for k in range(T):
            l = (anc + k) % Lo; nl = (l + 1) % Lo; last = (k + 1 == T)
            for x in F0[k]:
                for y in adj[l][x]:
                    if y not in Enew[nl]: continue
                    if (not last) and (y in A[nl]): F1[k + 1].add(y)
                    else: F0[k + 1].add(y)
            for x in F1[k]:
                for y in adj[l][x]:
                    if y not in Enew[nl]: continue
                    F1[k + 1].add(y)
        if s not in F1[T]: continue
        B0 = [set() for _ in range(T + 1)]; B1 = [set() for _ in range(T + 1)]; B0[T].add(s)
        for k in range(T - 1, -1, -1):
            l = (anc + k) % Lo; nl = (l + 1) % Lo; last = (k + 1 == T)
            for x in Enew[l]:
                z0 = False; z1 = False
                for y in adj[l][x]:
                    if y not in Enew[nl]: continue
                    if (not last) and (y in A[nl]):
                        if y in B0[k + 1] or y in B1[k + 1]: z1 = True
                    else:
                        if y in B0[k + 1]: z0 = True
                        if y in B1[k + 1]: z1 = True
                if z0: B0[k].add(x)
                if z1: B1[k].add(x)
        for k in range(T):
            l = (anc + k) % Lo
            EnewAcc[l] |= (F1[k] & (B0[k] | B1[k])) | (F0[k] & B1[k])
    totA = sum(len(x) for x in EnewAcc)
    msg2 = f'K={K} E_acc={totA} accepting states in E_acc={sum(len(x & A[l]) for l, x in enumerate(EnewAcc))}'
    if eacc:
        fn = f'{eacc}/E_K{K}.bin'
        try:
            f = open(fn, 'rb'); lo, W = struct.unpack('ii', f.read(8)); same = True; tot = 0
            for l in range(Lo):
                n = struct.unpack('Q', f.read(8))[0]; data = f.read(8 * W * n); got = set()
                for i in range(n):
                    words = struct.unpack_from('<%dQ' % W, data, 8 * W * i); cells = tuple((words[q // 12] >> (5 * (q % 12))) & 31 for q in range(K))
                    got.add(cells)
                if got != EnewAcc[l]: same = False
                tot += n
            msg2 += f' | eset3 file E_acc={tot} SETS {"EQUAL" if same and tot == totA else "DIFFER"}'
        except FileNotFoundError:
            msg2 += ' | (no eset3 file)'
    print(msg2, flush=True)

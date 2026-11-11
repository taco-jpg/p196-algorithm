#!/usr/bin/env python3
"""r12d: universal two-inlet shield thresholds q0(H) for H = 80K, K = 1..6 (rec0, rec1) and H = 192K (rec2),
same shield() as lemma2.py part A (copied verbatim), plus an independent re-implementation (retsat.rooted_rows)
for cross-checking.  q0(H) = minimal q such that every rooted state T^t(P(q,C)), t <= H, keeps the root B_t W_t
for ANY interior (both inner carries), with the clock forced and the prefix away from the midpoint.
usage: shield4.py"""
import os, sys
_HERE = os.path.dirname(os.path.abspath(__file__))
for _p in (os.path.join(_HERE, 'repo/calculation/decimal_frontier/lattice_kinks/edge_relaxation'),   # Studio work dir copy
           os.path.join(_HERE, '../../lattice_kinks/edge_relaxation')):                              # repository layout
    if os.path.exists(os.path.join(_p, 'klib.py')): sys.path.insert(0, _p); break
from klib import load_rec
from retsat import rooted_rows


def norm(a, c):
    d = []
    for x in a:
        v = x + c; d.append(v % 10); c = v // 10
    return d, c


def make(cap, W, g):          # verbatim from lemma2.py
    p = len(g); nB = len(cap[0]); m = len(W[0])
    def step(prefix):
        k = len(prefix); low, carry = norm(prefix, 0); outs = []
        for inc in (0, 1):
            high = [0]*k; c = inc
            for i in range(k-1, -1, -1):
                v = prefix[i] + c; high[i] = v % 10; c = v // 10
            out = [low[0]+1] + [low[i]+high[i-1] for i in range(1, k)] if c else [low[i]+high[i] for i in range(k)]
            outs.append((c, out))
        if outs[0][0] != outs[1][0]: return None, []
        a, b2 = outs[0][1], outs[1][1]
        mm = next((i for i in range(k) if a[i] != b2[i]), k)
        return outs[0][0], a[:mm]
    def shield(q, H, Cmin=4):
        pr = cap[0] + W[0]*q; n = 2*len(pr) + Cmin; k0 = len(pr)
        for t in range(H+1):
            if not (len(pr) + 2 <= n//2): return False, t, 'midpoint'
            if pr[:nB+m] != cap[t % p] + W[t % p]: return False, t, f'root (prefix {len(pr)})'
            if t == H: return True, t, f'prefix {k0}->{len(pr)}'
            gg, pr = step(pr)
            if gg != g[t % p]: return False, t, 'clock'
            n += gg
    return shield


def shield_indep(R, q, H):
    """independent: rooted_rows prefix keeps B_t W_t for t <= H and stays 2 below the midpoint (|C| = 4)"""
    half0 = R.B[0] + R.W[0]*q; n = 2*len(half0) + 4
    try:
        rows = rooted_rows(half0, R.g, H)
    except ValueError:
        return False
    for t in range(H+1):
        pr = rows[t]
        if not (len(pr) + 2 <= n//2): return False
        if pr[:R.nB+R.m] != R.B[t % R.p] + R.W[t % R.p]: return False
        if t < H: n += R.g[t % R.p]
    return True


if __name__ == '__main__':
    for rec, base in [(r, b) for (r, b) in ((0, 80), (1, 80), (2, 192)) if str(r) in (sys.argv[1] if len(sys.argv) > 1 else '012')]:
        R = load_rec(rec); sh = make(R.B, R.W, R.g)
        Ks = range(1, 7) if rec < 2 else range(1, 4)
        for K in Ks:
            H = base*K; qmax = 12*K + 20
            res = {q: sh(q, H) for q in range(1, qmax)}
            q0 = min(q for q in res if res[q][0])
            above = all(res[q][0] for q in range(q0, qmax))
            ind = {q: shield_indep(R, q, H) for q in range(max(1, q0-2), min(qmax, q0+6))}
            agree = all(ind[q] == res[q][0] for q in ind)
            print(f'rec{rec} m={R.m} H={H} (K={K}): q0={q0} all q in [{q0},{qmax-1}] pass: {above}; '
                  f'q0-1 -> {res[q0-1] if q0 > 1 else None}; q0 -> {res[q0]}; independent rooted_rows agrees: {agree}', flush=True)

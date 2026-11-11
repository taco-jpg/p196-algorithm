#!/usr/bin/env python3
"""r13a: SAT-based enumeration of bands with a prescribed period: all cyclic words V of length s (letters 0..2b-2, each row not all b-1)
with V_T = V under clock g (forced, T multiple of p).  Incremental cadical195; blocks each found word and all its rotations.
Output: BANDSAT s=.. T=.. true_T=.. Trot=.. twist=.. V=... (one per rotation class of solutions; words of smaller spatial period are reported once).
Usage: bandenum_sat.py --b 10 --clock 1000 --s 9 --T 12 [--limit 100000] [--timeout-per-solve SEC]"""
import sys, time, argparse
from pysat.solvers import Solver
import bandsat as BS

def enum_bands(b, clock, s, T, limit, tmo=None):
    NL = 2 * b - 1
    nv = [0]
    def new(k):
        r = nv[0] + 1; nv[0] += k; return [r + i for i in range(k)]
    S = Solver(name='cadical195')
    add = S.add_clause
    def amo(lits):
        for i in range(len(lits)):
            for j in range(i + 1, len(lits)):
                add([-lits[i], -lits[j]])
    p = len(clock)
    X = [[new(NL) for c in range(s)] for t in range(T + 1)]
    for t in range(T + 1):
        for c in range(s):
            add(list(X[t][c])); amo(X[t][c])
        add([-X[t][c][b - 1] for c in range(s)])  # not all b-1
    for t in range(T):
        g = clock[t % p]
        A = new(s); Bv = new(s)  # alpha_c, beta_c at cyclic columns
        LO = [new(b) for c in range(s)]; HI = [new(b) for c in range(s)]
        for c in range(s):
            add(list(LO[c])); amo(LO[c]); add(list(HI[c])); amo(HI[c])
            xc = X[t][c]
            cn = (c + 1) % s
            for v in range(NL):
                x = xc[v]
                if v == b - 1:
                    add([-x, -A[c], A[cn]]); add([-x, A[c], -A[cn]])
                    add([-x, -Bv[cn], Bv[c]]); add([-x, Bv[cn], -Bv[c]])
                elif v < b - 1:
                    add([-x, -A[cn]]); add([-x, -Bv[c]])
                else:
                    add([-x, A[cn]]); add([-x, Bv[c]])
                for a in (0, 1):
                    d = (v + a) % b
                    add([-x, (-A[c] if a else A[c]), LO[c][d]])
                    add([-x, (-Bv[cn] if a else Bv[cn]), HI[c][d]])
            h = HI[(c - 1) % s] if g else HI[c]
            for d1 in range(b):
                for d2 in range(b):
                    add([-LO[c][d1], -h[d2], X[t + 1][c][d1 + d2]])
    # V_T = V_0
    for c in range(s):
        for v in range(NL):
            add([-X[0][c][v], X[T][c][v]]); add([X[0][c][v], -X[T][c][v]])
    found = {}
    n = 0
    t0 = time.time()
    while n < limit:
        r = S.solve()
        if not r:
            return found, True, time.time() - t0
        m = set(l for l in S.get_model() if l > 0)
        V = [next(v for v in range(NL) if X[0][c][v] in m) for c in range(s)]
        # block all rotations of V
        for rot in range(s):
            W = V[rot:] + V[:rot]
            add([-X[0][c][W[c]] for c in range(s)])
        n += 1
        canon = min(tuple(V[r:] + V[:r]) for r in range(s))
        # true minimal period of V under the clock (multiple of p)
        tt = 0; x = list(V)
        while True:
            for t in range(p):
                x, *_ = BS.rowstep(x, clock[(tt + t) % p], b)
            tt += p
            if x == V: break
            if tt > 100000: tt = -1; break
        # Trot / twist
        x = list(V); tr = 0; twist = 0
        k = 0
        while True:
            for t in range(p):
                x, *_ = BS.rowstep(x, clock[(k * p + t) % p], b)
            k += 1
            rots = [i for i in range(s) if x == V[i:] + V[:i]]
            if rots:
                tr = k * p; twist = rots[0]; break
            if k * p > 100000: tr = -1; break
        found[canon] = (tt, tr, twist)
        print(f'BANDSAT s={s} T={T} true_T={tt} Trot={tr} twist={twist} V={",".join(map(str, canon))}', flush=True)
    return found, False, time.time() - t0

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--b', type=int, default=10); ap.add_argument('--clock', default='1000'); ap.add_argument('--s', type=int, required=True); ap.add_argument('--T', type=int, required=True)
    ap.add_argument('--limit', type=int, default=20000)
    a = ap.parse_args()
    cl = [int(c) for c in a.clock]
    t0 = time.time()
    found, complete, tt = enum_bands(a.b, cl, a.s, a.T, a.limit)
    print(f'ENUMDONE s={a.s} T={a.T} found={len(found)} complete={complete} time={tt:.1f}s', flush=True)

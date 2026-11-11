#!/usr/bin/env python3
"""Main-session independent spot check of r13a's L and R instances: own one-hot encoding (rectangle window), written from the
folded law; no code shared with bandsat.py / bandsat2.py.
L: columns [0,R-1) free, column R-1 foreign (letter != W[s-1]), columns >= R = band; left port free (alpha_0 every step, hi of column -1 at
   overflow steps); right port = background beta; forced clock; final: band correct on [R,N) at time T'.
R: columns < Z = band, column Z foreign (!= W[0]), columns (Z,N) free, right port beta_N free every step, left port = background;
   final: band correct on [0, Z+delta) at time T'.
usage: lcheck.py L|R CLOCK V(comma) --tau TAU --epoch T' --R R [--solver S] [--nofor] [--rot r]
"""
import sys, argparse, time
from pysat.solvers import Solver

ap = argparse.ArgumentParser()
ap.add_argument('mode')
ap.add_argument('clock')
ap.add_argument('V')
ap.add_argument('--tau', type=int, default=0)
ap.add_argument('--epoch', type=int, required=True)
ap.add_argument('--R', type=int, default=12)
ap.add_argument('--solver', default='kissat404')
ap.add_argument('--nofor', action='store_true')
ap.add_argument('--rot', type=int, default=-1)
ap.add_argument('--delta', type=int, default=-1)
a = ap.parse_args()
g = [int(c) for c in a.clock]
p = len(g)
gamma = lambda t: g[(t + a.tau) % p]
V0 = [int(x) for x in a.V.split(',')]
s = len(V0)


def row_step(x, gam):
    n = len(x)
    if all(v == 9 for v in x):
        raise ValueError('all 9')
    al = [0] * n
    for _ in range(n + 2):
        for c in range(n):
            al[(c + 1) % n] = 1 if x[c] + al[c] >= 10 else 0
    be = [0] * n
    for _ in range(n + 2):
        for c in range(n - 1, -1, -1):
            be[c] = 1 if x[c] + be[(c + 1) % n] >= 10 else 0
    lo = [(x[c] + al[c]) % 10 for c in range(n)]
    hi = [(x[c] + be[(c + 1) % n]) % 10 for c in range(n)]
    y = [lo[c] + (hi[(c - 1) % n] if gam else hi[c]) for c in range(n)]
    return y, al, be


def background(W, T):
    rows, As, Bs = [list(W)], [], []
    for t in range(T):
        y, al, be = row_step(rows[t], gamma(t))
        rows.append(y)
        As.append(al)
        Bs.append(be)
    return rows, As, Bs


# row at time tau of the census word V0 (time 0)
cur = list(V0)
for t in range(a.tau):
    cur = row_step(cur, g[t % p])[0]
Vtau = cur
T = a.epoch


def solve_rot(rot):
    W = Vtau[rot:] + Vtau[:rot]
    rows, As, Bs = background(W, T)
    # fronts
    l = 0
    r = 0
    for t in range(T):
        v = rows[t]
        run = 0
        while v[(l + run) % s] == 9 and run < s:
            run += 1
        l += 1 + run
        run = 0
        while v[(-r - 1 - run) % s] == 9 and run < s:
            run += 1
        r += 1 + run - gamma(t)
    margin = s + 8
    S = Solver(name=a.solver)
    nvar = [0]

    def new(k):
        x = nvar[0] + 1
        nvar[0] += k
        return x

    if a.mode == 'L':
        R = a.R
        N = R + l + margin
    else:
        Z = r + margin
        N = Z + a.R + 1  # free columns (Z, N)
        R = Z
    X = [[new(19) for c in range(N)] for t in range(T + 1)]
    AL = [[new(1) for c in range(N + 1)] for t in range(T)]
    BE = [[new(1) for c in range(N + 1)] for t in range(T)]
    LO = [[new(10) for c in range(N)] for t in range(T)]
    HI = [[new(10) for c in range(N)] for t in range(T)]
    HL = [new(10) if gamma(t) else 0 for t in range(T)]
    add = S.add_clause

    def amo(base, k):
        for i in range(k):
            for j in range(i + 1, k):
                add([-(base + i), -(base + j)])

    for c in range(N):
        add([X[0][c] + v for v in range(19)])
    for t in range(T + 1):
        for c in range(N):
            amo(X[t][c], 19)
    for t in range(T):
        gam = gamma(t)
        al, be = AL[t], BE[t]
        if gam:
            add([HL[t] + d for d in range(10)])
            amo(HL[t], 10)
        if a.mode == 'L':
            # right port: background beta at column N
            add([be[N] if Bs[t][(N - R) % s] else -be[N]])
        else:
            # left port: background carries
            add([al[0] if As[t][(0 - Z) % s] else -al[0]])
            if gam:
                hdig = (rows[t][(-1 - Z) % s] + Bs[t][(0 - Z) % s]) % 10
                add([HL[t] + hdig])
        for c in range(N):
            xs = X[t][c]
            for v in range(19):
                if v == 9:
                    add([-(xs + 9), -al[c], al[c + 1]])
                    add([-(xs + 9), al[c], -al[c + 1]])
                    add([-(xs + 9), -be[c + 1], be[c]])
                    add([-(xs + 9), be[c + 1], -be[c]])
                elif v < 9:
                    add([-(xs + v), -al[c + 1]])
                    add([-(xs + v), -be[c]])
                else:
                    add([-(xs + v), al[c + 1]])
                    add([-(xs + v), be[c]])
                for aa in (0, 1):
                    d = (v + aa) % 10
                    add([-(xs + v), (-al[c] if aa else al[c]), LO[t][c] + d])
                    add([-(xs + v), (-be[c + 1] if aa else be[c + 1]), HI[t][c] + d])
            amo(LO[t][c], 10)
            amo(HI[t][c], 10)
            h = (HI[t][c - 1] if c > 0 else HL[t]) if gam else HI[t][c]
            for d1 in range(10):
                for d2 in range(10):
                    add([-(LO[t][c] + d1), -(h + d2), X[t + 1][c] + d1 + d2])
    if a.mode == 'L':
        for c in range(R, N):
            add([X[0][c] + W[(c - R) % s]])
        if not a.nofor:
            add([-(X[0][R - 1] + W[s - 1])])
        for c in range(R, N):
            add([X[T][c] + rows[T][(c - R) % s]])
    else:
        ov = sum(gamma(t) for t in range(T))
        delta = ov // 2 if a.delta < 0 else a.delta
        for c in range(0, Z):
            add([X[0][c] + W[(c - Z) % s]])
        if not a.nofor:
            add([-(X[0][Z] + W[0])])
        for c in range(0, Z + delta):
            add([X[T][c] + rows[T][(c - Z) % s]])
    t0 = time.time()
    res = S.solve()
    S.delete()
    return res, time.time() - t0, N


rots = range(s) if a.rot < 0 else [a.rot]
allu = True
out = []
for rot in rots:
    res, sec, N = solve_rot(rot)
    if res:
        allu = False
    out.append(f'rot{rot}:{"SAT" if res else "UNSAT"}({sec:.1f}s,N={N})')
print(f'{a.mode} clock={a.clock} V={a.V} tau={a.tau} T={T} R={a.R} solver={a.solver}{" nofor" if a.nofor else ""}: ' + ' '.join(out) + (' => ALLUNSAT' if allu else ' => some SAT'), flush=True)

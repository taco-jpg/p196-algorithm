#!/usr/bin/env python3
"""r13a: L (left restoration) and R (right end) SAT instances for a general band, any base, any clock.
Derived from main_check/bcheck.py (r12f) but rewritten for general base b, word V, clock, T, with optional cone trimming.

Folded law (index c = column, increasing towards the middle):
  alpha_(c+1) = [x_c + alpha_c >= b], beta_c = [x_c + beta_(c+1) >= b]
  lo_c = (x_c+alpha_c) % b, hi_c = (x_c+beta_(c+1)) % b
  y_c = lo_c + hi_c (gamma=0),  y_c = lo_c + hi_(c-1) (gamma=1)
Couplings of a window [x0,x1): left inputs alpha_x0 and (gamma=1 steps) hi_(x0-1); right input beta_x1.
"""
import sys, time, random, argparse, resource, json, os
from pysat.solvers import Solver

CT = 10**12   # constant true literal; constant false is -CT
CF = -CT


def rowstep(x, g, b):
    n = len(x)
    st = next(i for i in range(n) if x[i] != b - 1)  # raises StopIteration if all letters are b-1
    al = [0] * n
    a = 1 if x[st] >= b else 0
    for k in range(1, n):
        i = (st + k) % n
        al[i] = a
        a = 1 if x[i] + a >= b else 0
    al[st] = a
    be = [0] * n
    h = 1 if x[st] >= b else 0
    be[st] = h
    for k in range(1, n):
        i = (st - k) % n
        h = 1 if x[i] + h >= b else 0
        be[i] = h
    lo = [(x[c] + al[c]) % b for c in range(n)]
    hi = [(x[c] + be[(c + 1) % n]) % b for c in range(n)]
    y = [lo[c] + (hi[(c - 1) % n] if g else hi[c]) for c in range(n)]
    return y, al, be, lo, hi


def background(V, clock, b):
    """rows[t], al[t], be[t], lo[t], hi[t] for t = 0..T (carries only t < T), band coordinates."""
    rows, As, Bs, Ls, Hs = [list(V)], [], [], [], []
    for g in clock:
        y, al, be, lo, hi = rowstep(rows[-1], g, b)
        rows.append(y)
        As.append(al)
        Bs.append(be)
        Ls.append(lo)
        Hs.append(hi)
    return rows, As, Bs, Ls, Hs


def run9_from(row, c, b):
    n = len(row)
    k = 0
    while k < n and row[(c + k) % n] == b - 1:
        k += 1
    return k


def run9_to(row, c, b):  # run of (b-1)'s ending at column c
    n = len(row)
    k = 0
    while k < n and row[(c - k) % n] == b - 1:
        k += 1
    return k


def left_fronts(rows, b, clock):
    """l_t: band pure on [y+l_t, inf) at time t, arbitrary context left of y (rows at phase 0 of V at y)."""
    l = [0]
    for t in range(len(clock)):
        l.append(l[-1] + 1 + run9_from(rows[t], l[-1], b))
    return l


def right_fronts(rows, b, clock):
    """r_t: band pure on (-inf, z - r_t) at time t, where the band coordinate of z is 0.
    Recurrence: b_t = -r_t is the exclusive end; the column b_t - 1 has band coordinate (-r_t - 1) mod n."""
    r = [0]
    for t, g in enumerate(clock):
        r.append(r[-1] + 1 - g + run9_to(rows[t], -r[-1] - 1, b))
    return r


class Enc:
    def __init__(self, solver='kissat404', dimacs=None):
        self.nv = 0
        self.nc = 0
        self.dimacs = dimacs
        self.cl = [] if dimacs else None
        self.S = Solver(name=solver) if not dimacs else None
        self.solver = solver

    def new(self, k=1):
        r = self.nv + 1
        self.nv += k
        return r

    def add(self, cl):
        o = []
        for l in cl:
            if l == CT:
                return
            if l != CF:
                o.append(l)
        if not o:
            raise ValueError('empty clause (constant contradiction)')
        self.nc += 1
        if self.S is None:
            self.cl.append(o)
        else:
            self.S.add_clause(o)

    def varlits(self, k):
        r = self.new(k)
        return [r + i for i in range(k)]

    def amo(self, lits):
        k = len(lits)
        for i in range(k):
            for j in range(i + 1, k):
                self.add([-lits[i], -lits[j]])

    def const(self, k, v):
        return [CT if i == v else CF for i in range(k)]


def encode_strip(E, b, clock, N, Arange, Hrange, bgl, bga, bgb, left_free, right_free):
    """Generic strip encoder.  Window columns [0,N), T = len(clock).
    At time s the letters are variables on [Arange[s], Hrange[s]) and background constants elsewhere.
    bgl(s,c), bga(s,c), bgb(s,c): background letter, alpha_c and beta_c at window column c.
    left_free: alpha_0 and (overflow steps) hi_(-1) are free (Arange[s] = 0).
    right_free: beta_N is free (Hrange[s] = N).
    Returns X, AL, BE, HL (time-indexed literal arrays)."""
    NL = 2 * b - 1
    T = len(clock)
    X = []
    for s in range(T + 1):
        row = [None] * N
        for c in range(N):
            if Arange[s] <= c < Hrange[s]:
                row[c] = E.varlits(NL)
                E.amo(row[c])
            else:
                row[c] = E.const(NL, bgl(s, c))
        X.append(row)
    # the first row: at least one letter
    for c in range(Arange[0], Hrange[0]):
        E.add(list(X[0][c]))
    AL, BE, HL = [], [], []
    for s in range(T):
        g = clock[s]
        A, H = Arange[s], Hrange[s]
        # carries at columns 0..N
        al = [None] * (N + 1)
        be = [None] * (N + 1)
        for c in range(N + 1):
            if left_free:
                if c == 0:
                    al[c] = E.new()
                elif c < H or H == N:  # H == N: alpha_N is an unconstrained output
                    al[c] = E.new()
                else:
                    al[c] = CT if bga(s, c) else CF
            else:  # exact left background
                if c <= A:
                    al[c] = CT if bga(s, c) else CF
                else:
                    al[c] = E.new()  # includes alpha_N (unconstrained output)
            if right_free:
                if c == N:
                    be[c] = E.new()
                elif c >= A:
                    be[c] = E.new()
                else:
                    be[c] = CT if bgb(s, c) else CF
            else:
                if c < H and c >= A:
                    be[c] = E.new()
                else:
                    be[c] = CT if bgb(s, c) else CF
        AL.append(al)
        BE.append(be)
        lo = [None] * N
        hi = [None] * N
        hlv = None
        if g:
            if left_free:
                hlv = E.varlits(b)
                E.add(list(hlv))
                E.amo(hlv)
        for c in range(N):
            if A <= c < H:
                lo[c] = E.varlits(b)
                hi[c] = E.varlits(b)
                E.amo(lo[c])
                E.amo(hi[c])
                xc = X[s][c]
                for v in range(NL):
                    x = xc[v]
                    # carries
                    if v == b - 1:
                        E.add([-x, -al[c], al[c + 1]])
                        E.add([-x, al[c], -al[c + 1]])
                        E.add([-x, -be[c + 1], be[c]])
                        E.add([-x, be[c + 1], -be[c]])
                    elif v < b - 1:
                        E.add([-x, -al[c + 1]])
                        E.add([-x, -be[c]])
                    else:
                        E.add([-x, al[c + 1]])
                        E.add([-x, be[c]])
                    for a in (0, 1):
                        d = (v + a) % b
                        E.add([-x, (-al[c] if a else al[c]), lo[c][d]])
                        E.add([-x, (-be[c + 1] if a else be[c + 1]), hi[c][d]])
            else:
                # constant cell: digit constants from background (carries background)
                L = bgl(s, c)
                lo[c] = E.const(b, (L + bga(s, c)) % b)
                hi[c] = E.const(b, (L + bgb(s, c + 1)) % b)
        # next letters at time s+1
        A1, H1 = Arange[s + 1], Hrange[s + 1]
        for c in range(A1, H1):
            if g:
                if c > 0:
                    h = hi[c - 1]
                else:
                    if left_free:
                        h = hlv
                    else:
                        h = E.const(b, (bgl(s, -1) + bgb(s, 0)) % b)
            else:
                h = hi[c]
            for d1 in range(b):
                if lo[c][d1] == CF:
                    continue
                for d2 in range(b):
                    if h[d2] == CF:
                        continue
                    E.add([-lo[c][d1], -h[d2], X[s + 1][c][d1 + d2]])
        HL.append(hlv)
    return X, AL, BE, HL


def letter_of(model, lits):
    vs = [v for v in range(len(lits)) if (lits[v] == CT or (lits[v] != CF and lits[v] in model))]
    return vs


def build_L(b, V, clock, R, W=None, g_final=0, foreign=True, trim=True, DELTA=None, solver='kissat404', rows_bg=None, require_period=True, dimacs=None, epoch_marks=None, ret_free=False):
    """L instance (left restoration).  Window [y-R, y+W), band V phase 0 at y, foreign letter at y-1."""
    n = len(V)
    T = len(clock)
    rows, As, Bs, Ls, Hs = background(V, clock, b) if rows_bg is None else rows_bg
    if require_period:
        assert rows[T] == list(V), ('not a period', V, rows[T])
    lf = left_fronts(rows, b, clock)
    if DELTA is None:
        DELTA = n + 3
    if W is None:
        W = lf[T] + DELTA + n + 3
    N = R + W
    E = Enc(solver, dimacs=dimacs)

    def bgl(s, c):
        return rows[s][(c - R) % n]

    def bga(s, c):
        return As[s][(c - R) % n]

    def bgb(s, c):
        return Bs[s][(c - R) % n]

    if trim:
        H = [min(N, R + lf[s] + DELTA) for s in range(T + 1)]
    else:
        H = [N] * (T + 1)
    A = [0] * (T + 1)
    X, AL, BE, HL = encode_strip(E, b, clock, N, A, H, bgl, bga, bgb, left_free=True, right_free=False)
    # initial band
    for c in range(R, H[0]):
        E.add([X[0][c][V[(c - R) % n]]])
    if foreign:
        E.add([-X[0][R - 1][V[-1]]])
    # final condition
    if g_final is not None:
        for c in range(R + g_final, H[T]):
            E.add([X[T][c][rows[T][(c - R) % n]]])
    if ret_free:
        # D-type (defect) condition: the free columns return exactly at the end (exact period junction)
        NL = 2 * b - 1
        for c in range(0, R):
            x0 = X[0][c]
            xT = X[T][c]
            for v in range(NL):
                E.add([-x0[v], xT[v]])
                E.add([x0[v], -xT[v]])
    if epoch_marks:
        # band correct on [y, inf) also at the intermediate times in epoch_marks (T_e, 2T_e, ...)
        for t_e in epoch_marks:
            for c in range(R, H[t_e]):
                E.add([X[t_e][c][rows[t_e][(c - R) % n]]])
    info = dict(N=N, W=W, T=T, front=lf[T], DELTA=DELTA, trim=trim, vars=E.nv, clauses=E.nc)
    return E, X, AL, BE, HL, info


def build_R(b, V, clock, Z=None, Rfree=12, delta=0, foreign=True, trim=True, DELTA=None, solver='kissat404', rows_bg=None, require_period=True, dimacs=None, comoving=False):
    """R instance (right end).  V phase 0 at z.  Band on (-inf, z) (window [0,Z)), free cells [z, z+Rfree), free
    right port beta_(z+Rfree), exact left background; final: band correct on (-inf, z+delta)."""
    n = len(V)
    T = len(clock)
    rows, As, Bs, Ls, Hs = background(V, clock, b) if rows_bg is None else rows_bg
    if require_period:
        assert rows[T] == list(V), ('not a period', V, rows[T])
    rf = right_fronts(rows, b, clock)
    if DELTA is None:
        DELTA = n + 3
    if Z is None:
        Z = rf[T] + DELTA + 2 * n + 3
    N = Z + Rfree
    E = Enc(solver, dimacs=dimacs)

    def bgl(s, c):
        return rows[s][(c - Z) % n]

    def bga(s, c):
        return As[s][(c - Z) % n]

    def bgb(s, c):
        return Bs[s][(c - Z) % n]

    if trim:
        A = [max(0, Z - rf[s] - DELTA) for s in range(T + 1)]
    else:
        A = [0] * (T + 1)
    H = [N] * (T + 1)
    X, AL, BE, HL = encode_strip(E, b, clock, N, A, H, bgl, bga, bgb, left_free=False, right_free=True)
    # initial band
    for c in range(A[0], Z):
        E.add([X[0][c][V[(c - Z) % n]]])
    if foreign:
        E.add([-X[0][Z][V[0]]])
    # final condition: band correct on (-inf, z+delta)
    if delta is not None:
        for c in range(A[T], Z + delta):
            E.add([X[T][c][rows[T][(c - Z) % n]]])
    if comoving:
        # R* (comoving return): columns [z+delta, z+Rfree) at time T equal the letters of [z, z+Rfree-delta) at time 0
        NL = 2 * b - 1
        for c in range(Z + delta, N):
            xT = X[T][c]
            x0 = X[0][c - delta]
            for v in range(NL):
                E.add([-xT[v], x0[v]])
                E.add([xT[v], -x0[v]])
    info = dict(N=N, Z=Z, T=T, Rfree=Rfree, front=rf[T], DELTA=DELTA, delta=delta, trim=trim, comoving=comoving, vars=E.nv, clauses=E.nc)
    return E, X, AL, BE, HL, info


def rss_gb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024 ** 3


def solve_and_report(E, tag, t0):
    tb = time.time() - t0
    r = E.S.solve()
    ans = 'SAT' if r else 'UNSAT'
    m = set(l for l in E.S.get_model() if l > 0) if r else None
    print(f'RESULT {tag} {ans} vars={E.nv} clauses={E.nc} build={tb:.1f}s total={time.time()-t0:.1f}s rss={rss_gb():.2f}GB', flush=True)
    return r, m

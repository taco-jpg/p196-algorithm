#!/usr/bin/env python3
"""r13a independent second encoding (enc2) of the L and R instances: rectangle window, direct successor relations:
no LO/HI digit variables.  gamma=0: next letter is a function of (x_c, alpha_c, beta_(c+1));
gamma=1: next letter is a function of (x_c, alpha_c, x_(c-1), beta_c).
Written from the folded law only (r12f FINAL sec. 1, r13a NOTES); shares nothing with bandsat.encode_strip except
the Enc container and the background row computation is re-implemented here."""
import sys, time
from pysat.solvers import Solver
import bandsat as BS  # only for Enc (clause container), rowstep is re-derived below


def carry(x, c, b):
    return 1 if x + c >= b else 0


def step_periodic(x, g, b):
    # periodic carries by fixed-point iteration (independent of bandsat.rowstep)
    n = len(x)
    if all(v == b - 1 for v in x):
        raise ValueError('all (b-1)')
    al = [0] * n
    for _ in range(n + 2):
        for c in range(n):
            al[(c + 1) % n] = carry(x[c], al[c], b)
    be = [0] * n
    for _ in range(n + 2):
        for c in reversed(range(n)):
            be[c] = carry(x[c], be[(c + 1) % n], b)
    lo = [(x[c] + al[c]) % b for c in range(n)]
    hi = [(x[c] + be[(c + 1) % n]) % b for c in range(n)]
    y = [lo[c] + hi[(c - 1) % n] if g else lo[c] + hi[c] for c in range(n)]
    return y, al, be


def bg(V, clock, b):
    rows = [list(V)]
    As, Bs = [], []
    for g in clock:
        y, al, be = step_periodic(rows[-1], g, b)
        rows.append(y)
        As.append(al)
        Bs.append(be)
    return rows, As, Bs


def build_rect(E, b, clock, N):
    """Common rectangle: returns X, AL (alpha_c, c=0..N), BE (beta_c, c=0..N)."""
    NL = 2 * b - 1
    T = len(clock)
    X = [[None] * N for s in range(T + 1)]
    for s in range(T + 1):
        for c in range(N):
            X[s][c] = E.varlits(NL)
            E.add(list(X[s][c]))
            E.amo(X[s][c])
    AL = [[E.new() for c in range(N + 1)] for s in range(T)]
    BE = [[E.new() for c in range(N + 1)] for s in range(T)]
    HL = []
    for s in range(T):
        g = clock[s]
        A, B = AL[s], BE[s]
        for c in range(N):
            xc = X[s][c]
            # carries
            for v in range(NL):
                if v == b - 1:
                    E.add([-xc[v], -A[c], A[c + 1]])
                    E.add([-xc[v], A[c], -A[c + 1]])
                    E.add([-xc[v], -B[c + 1], B[c]])
                    E.add([-xc[v], B[c + 1], -B[c]])
                elif v < b - 1:
                    E.add([-xc[v], -A[c + 1]])
                    E.add([-xc[v], -B[c]])
                else:
                    E.add([-xc[v], A[c + 1]])
                    E.add([-xc[v], B[c]])
        if g:
            hl = E.varlits(b)
            E.add(list(hl))
            E.amo(hl)
            HL.append(hl)
        else:
            HL.append(None)
        # next letters
        for c in range(N):
            xc = X[s][c]
            nxt = X[s + 1][c]
            if g == 0:
                for v in range(NL):
                    for a in (0, 1):
                        for bb in (0, 1):
                            w = (v + a) % b + (v + bb) % b
                            E.add([-xc[v], (-A[c] if a else A[c]), (-B[c + 1] if bb else B[c + 1]), nxt[w]])
            else:
                if c == 0:
                    hl = HL[s]
                    for v in range(NL):
                        for a in (0, 1):
                            for d in range(b):
                                w = (v + a) % b + d
                                E.add([-xc[v], (-A[c] if a else A[c]), -hl[d], nxt[w]])
                else:
                    xl = X[s][c - 1]
                    for v in range(NL):
                        for a in (0, 1):
                            for u in range(NL):
                                for bb in (0, 1):
                                    w = (v + a) % b + (u + bb) % b
                                    E.add([-xc[v], (-A[c] if a else A[c]), -xl[u], (-B[c] if bb else B[c]), nxt[w]])
    return X, AL, BE, HL


def build_L2(b, V, clock, R, W=None, g_final=0, foreign=True, solver='kissat404', rows_bg=None, require_period=True, dimacs=None, epoch_marks=None, ret_free=False, **kw):
    n = len(V)
    T = len(clock)
    rows, As, Bs = bg(V, clock, b) if rows_bg is None else (rows_bg[0], rows_bg[1], rows_bg[2])
    if require_period:
        assert rows[T] == list(V)
    lf = BS.left_fronts(rows, b, clock)
    if W is None:
        W = lf[T] + 2 * n + 8
    N = R + W
    E = BS.Enc(solver)
    X, AL, BE, HL = build_rect(E, b, clock, N)
    # right port: background high carry at column N (band coord N - R)
    for s in range(T):
        beta = Bs[s][(N - R) % n]
        E.add([BE[s][N] if beta else -BE[s][N]])
    # (left port: alpha_0 free, HL free at overflow steps)
    for c in range(R, N):
        E.add([X[0][c][V[(c - R) % n]]])
    if foreign:
        E.add([-X[0][R - 1][V[-1]]])
    if g_final is not None:
        for c in range(R + g_final, N):
            E.add([X[T][c][rows[T][(c - R) % n]]])
    if ret_free:
        for c in range(0, R):
            for v in range(2 * b - 1):
                E.add([-X[0][c][v], X[T][c][v]])
                E.add([X[0][c][v], -X[T][c][v]])
    if epoch_marks:
        for t_e in epoch_marks:
            for c in range(R, N):
                E.add([X[t_e][c][rows[t_e][(c - R) % n]]])
    return E, X, AL, BE, HL, dict(N=N, W=W, T=T, front=lf[T], trim=False, vars=E.nv, clauses=E.nc)


def build_R2(b, V, clock, Z=None, Rfree=12, delta=0, foreign=True, solver='kissat404', rows_bg=None, require_period=True, dimacs=None, comoving=False, **kw):
    n = len(V)
    T = len(clock)
    rows, As, Bs = bg(V, clock, b) if rows_bg is None else (rows_bg[0], rows_bg[1], rows_bg[2])
    if require_period:
        assert rows[T] == list(V)
    rf = BS.right_fronts(rows, b, clock)
    if Z is None:
        Z = rf[T] + 2 * n + 8
    N = Z + Rfree
    E = BS.Enc(solver)
    X, AL, BE, HL = build_rect(E, b, clock, N)
    # left port exact: alpha_0 and (overflow) hi_(-1) from background at band coordinate -Z
    for s in range(T):
        a0 = As[s][(0 - Z) % n]
        E.add([AL[s][0] if a0 else -AL[s][0]])
        if clock[s]:
            xl = rows[s][(-1 - Z) % n]
            be0 = Bs[s][(0 - Z) % n]
            E.add([HL[s][(xl + be0) % b]])
    # initial band on [0, Z)
    for c in range(0, Z):
        E.add([X[0][c][V[(c - Z) % n]]])
    if foreign:
        E.add([-X[0][Z][V[0]]])
    if delta is not None:
        for c in range(0, Z + delta):
            E.add([X[T][c][rows[T][(c - Z) % n]]])
    if comoving:
        for c in range(Z + delta, N):
            for v in range(2 * b - 1):
                E.add([-X[T][c][v], X[0][c - delta][v]])
                E.add([X[T][c][v], -X[0][c - delta][v]])
    return E, X, AL, BE, HL, dict(N=N, Z=Z, T=T, Rfree=Rfree, front=rf[T], delta=delta, trim=False, comoving=comoving, vars=E.nv, clauses=E.nc)

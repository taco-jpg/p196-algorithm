#!/usr/bin/env python3
"""r12d retsat.py -- exact SAT encoding of the fixed-centre return of the p8 lattice family.

Family (pairword, LSB first, folded column i = positions i and n-1-i):
    P(q,C) = B0 W0^q C rev(W0)^q rev(B0),  C palindromic, symbols 0..18, odd |C| -> even midpoint.
Return of period S = 2*m*p/sum(g) * K steps (80K for m=20):  T^S(P(q0,C)) == P(q0+K,C).

Exact step (no approximation): normalise P with the low carry alpha (root -> centre) and the high carry
beta (centre -> root, the continuation of alpha through the middle); digits lo_i=(P_i+alpha_i)%10,
hi_i=(P_i+beta_(i+1))%10; overflow gamma = beta_0; the new pairword is P'_i = d_i + d_(n'-1-i) with
the real digit string d (length n' = n+gamma, d_n = 1 if gamma).  Here every P'_i is produced by
mapping the positions i and n'-1-i to their digit variables (lo / middle / hi), so both parities and
the gamma-shift are handled by one formula.

Window: columns below a_t = |R_t| - margin are taken from the rooted two-inlet prefix R_t (the part of
the word that is identical for every interior, computed with both possible carry inlets, as lemma2.py);
the clock gamma_t = g_t is forced there (asserted).  Columns [a_t, M_t) are SAT variables.  The step
t -> t+1 uses columns [a_(t+1)-1, M_t); columns of that range below a_t are constants from R_t.
Every constant used is a value of R_t, so the encoding is exact for every centre (no pruning).

modes:  ret      exact return, final centre == initial centre
        lat      final lattice part only (final centre free, same length): moving / any centre of length L
        prefix   only the first k folded columns of the final word must match the target (validation vs cen2)
        planted  target = exact image of a given centre (positive control)
        sim      C fixed, no final constraint; the model is compared with klib.pairword_step every step
"""
import sys, os, time, argparse, random, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                'repo/calculation/decimal_frontier/lattice_kinks/edge_relaxation'))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../lattice_kinks/edge_relaxation'))   # repository layout
from klib import load_rec, pairword_step


# ------------------------------------------------------------------ exact reference pieces
def rooted_rows(half0, g, S):
    """two-inlet rooted prefix rows R_0..R_S (folded columns that do not depend on the interior)"""
    p = len(g); pr = list(half0); rows = [pr]
    for t in range(S):
        k = len(pr)
        if k < 2: raise ValueError(f'rooted prefix vanished at t={t}')
        lo = []; c = 0
        for i in range(k):
            v = pr[i] + c; lo.append(v % 10); c = v // 10
        outs = []
        for inlet in (0, 1):
            hi = [0] * k; b = inlet
            for i in range(k - 1, -1, -1):
                v = pr[i] + b; hi[i] = v % 10; b = v // 10
            if b: new = [lo[0] + 1] + [lo[i] + hi[i - 1] for i in range(1, k)]
            else: new = [lo[i] + hi[i] for i in range(k)]
            outs.append((b, new))
        if not (outs[0][0] == outs[1][0] == g[t % p]):
            raise ValueError(f'clock not forced by the rooted prefix at t={t}')
        A, Bq = outs[0][1], outs[1][1]
        j = next((i for i in range(k) if A[i] != Bq[i]), k)
        pr = A[:j]; rows.append(pr)
    return rows


def low_carry(row, x):
    c = 0
    for i in range(x): c = (row[i] + c) // 10
    return c


def Pword(lat, q, C):
    hh = lat.B[0] + lat.W[0] * q
    return hh + list(C) + hh[::-1]


def fold(P):
    return P[:(len(P) + 1) // 2]


def centre_of(idx, L):
    """same index -> centre map as cen2.cpp / ref2gen.py"""
    h, odd = L // 2, L % 2; r = idx; mid = None
    if odd: mid = 2 * (r % 10); r //= 10
    half = []
    for _ in range(h): half.append(r % 19); r //= 19
    half = half[::-1]
    return half + ([mid] if odd else []) + half[::-1]


def simulate(lat, q0, C, S):
    P = Pword(lat, q0, C); rows = [P]; gam = []
    for t in range(S):
        P, gg = pairword_step(P); rows.append(P); gam.append(gg)
    return rows, gam


# ------------------------------------------------------------------ CNF plumbing
class Sink:
    def __init__(s, solver=None, keep=False):
        s.S = solver; s.n = 0; s.keep = [] if keep else None
    def append(s, c):
        if s.S is not None: s.S.add_clause(c)
        if s.keep is not None: s.keep.append(c)
        s.n += 1


class Enc:
    def __init__(s, solver=None, keep=False):
        s.nv = 0; s.cl = Sink(solver, keep)
    def new(s, k=1):
        r = list(range(s.nv + 1, s.nv + 1 + k)); s.nv += k; return r
    def onehot(s, k, alo=True, amo=True):
        v = s.new(k)
        if alo: s.cl.append(list(v))
        if amo:
            for i in range(k):
                for j in range(i + 1, k): s.cl.append([-v[i], -v[j]])
        return v
    def fix(s, lit): s.cl.append([lit])
    def bit(s, var, b): s.cl.append([var] if b else [-var])


def adder(E, Pv, cin, dig, cout):
    """dig = (P + cin) % 10, cout = [P + cin >= 10]; Pv one-hot 19, cin / cout are SAT variables
    (a known carry is passed as a variable fixed by a unit clause)"""
    for x in range(19):
        for b in (0, 1):
            E.cl.append([-Pv[x], (-cin if b else cin), dig[(x + b) % 10]])
        if x >= 10: E.cl.append([-Pv[x], cout])
        elif x <= 8: E.cl.append([-Pv[x], -cout])
        else:  # x == 9: the carry passes
            E.cl.append([-Pv[x], -cin, cout]); E.cl.append([-Pv[x], cin, -cout])


# ------------------------------------------------------------------ instance
class Inst:
    def __init__(s, rec, q0, K, L, margin=2):
        s.lat = lat = load_rec(rec); s.rec = rec
        s.p, s.nB, s.m, s.g = lat.p, lat.nB, lat.m, lat.g
        s.q0, s.K, s.L = q0, K, L
        num = 2 * s.m * s.p * K
        assert num % sum(s.g) == 0
        s.S = num // sum(s.g)
        s.half0 = lat.B[0] + lat.W[0] * q0; s.H0 = len(s.half0)
        s.half1 = lat.B[0] + lat.W[0] * (q0 + K); s.H1 = len(s.half1)
        s.n = [2 * s.H0 + L]
        for t in range(s.S): s.n.append(s.n[-1] + s.g[t % s.p])
        assert s.n[s.S] == 2 * s.H1 + L, 'clock / length mismatch'
        s.M = [(x + 1) // 2 for x in s.n]
        s.R = rooted_rows(s.half0, s.g, s.S)
        s.a = [len(r) - margin for r in s.R]
        for t in range(s.S + 1):
            assert s.a[t] >= 2 and len(s.R[t]) + 2 <= s.n[t] // 2, ('rooted prefix reaches the centre', t)
        # rooted final prefix must agree with the lattice target, otherwise trivially infeasible
        s.final_prefix_ok = s.R[s.S] == s.half1[:len(s.R[s.S])]
        s.h = (L + 1) // 2   # folded centre columns

    def describe(s):
        return (f'rec{s.rec} q0={s.q0} K={s.K} L={s.L} S={s.S} n0={s.n[0]} nS={s.n[s.S]} H0={s.H0} H1={s.H1} '
                f'|R0|={len(s.R[0])} |RS|={len(s.R[s.S])} final_prefix_ok={s.final_prefix_ok}')

    def build(s, mode='ret', Cfix=None, planted=None, prefix_k=None, units=True, solver=None, keep=False,
              amo_P=True):
        E = Enc(solver, keep); S = s.S; p = s.p
        Pt = {}   # current row: col -> one-hot vars (19)
        # ---- t = 0
        b0 = s.a[1] - 1
        lo0 = min(b0, s.a[0])
        for i in range(lo0, s.M[0]):
            Pt[i] = E.onehot(19, alo=True, amo=amo_P)
            if i < s.H0: E.fix(Pt[i][s.half0[i]])
        Cv = [Pt[s.H0 + j] for j in range(s.h)]
        if s.L % 2:   # odd midpoint is even
            for x in range(1, 19, 2): E.fix(-Cv[-1][x])
        if Cfix is not None:
            for j in range(s.h): E.fix(Cv[j][Cfix[j]])
        rows = [dict(Pt)]
        for t in range(S):
            n, n2, gt = s.n[t], s.n[t + 1], s.g[t % p]
            Mt, Mt2 = s.M[t], s.M[t + 1]
            bt = s.a[t + 1] - 1
            assert bt <= s.a[t] and bt >= 1
            # constant columns [bt, a_t) (and any column in Pt below bt is ignored)
            for i in range(bt, s.a[t]):
                if i not in Pt:
                    Pt[i] = E.onehot(19, alo=True, amo=amo_P); E.fix(Pt[i][s.R[t][i]])
            if units and t > 0:
                for i in range(s.a[t], min(len(s.R[t]), Mt)): E.fix(Pt[i][s.R[t][i]])
            nlow = n // 2           # pair columns 0..nlow-1 ; if n odd the middle column is nlow
            odd = n % 2
            ab = E.new()[0]; E.bit(ab, low_carry(s.R[t], bt)); alpha = {bt: ab}
            lo = {}; hi = {}
            for i in range(bt, nlow):
                lo[i] = E.onehot(10); alpha[i + 1] = E.new()[0]
                adder(E, Pt[i], alpha[i], lo[i], alpha[i + 1])
            beta = {}
            if odd:
                dmid = E.onehot(10); cm = E.new()[0]
                adder(E, Pt[nlow], alpha[nlow], dmid, cm)
                beta[nlow] = cm
            else:
                dmid = None; beta[nlow] = alpha[nlow]
            for i in range(nlow - 1, bt - 1, -1):
                hi[i] = E.onehot(10); beta[i] = E.new()[0]
                adder(E, Pt[i], beta[i + 1], hi[i], beta[i])

            def digit(j):
                if j < nlow: return lo[j]
                if odd and j == nlow: return dmid
                if j <= n - 1: return hi[n - 1 - j]
                raise AssertionError('overflow digit inside window')
            Pn = {}
            for i in range(s.a[t + 1], Mt2):
                v = E.onehot(19, alo=True, amo=amo_P); Pn[i] = v
                j2 = n2 - 1 - i
                if j2 == i:
                    X = digit(i)
                    for x in range(10): E.cl.append([-X[x], v[2 * x]])
                    for x in range(1, 19, 2): E.fix(-v[x])
                else:
                    X, Y = digit(i), digit(j2)
                    for x in range(10):
                        for y in range(10): E.cl.append([-X[x], -Y[y], v[x + y]])
            Pt = Pn; rows.append(dict(Pt))
        # ---- final constraints
        aS = s.a[S]
        if units:
            for i in range(aS, min(len(s.R[S]), s.M[S])): E.fix(Pt[i][s.R[S][i]])
        if mode in ('ret', 'lat', 'prefix'):
            lim = s.M[S] if prefix_k is None else min(prefix_k, s.M[S])
            for i in range(aS, lim):
                if i < s.H1: E.fix(Pt[i][s.half1[i]])
                elif mode == 'ret' or (mode == 'prefix'):
                    j = i - s.H1
                    for x in range(19):
                        E.cl.append([-Cv[j][x], Pt[i][x]]); E.cl.append([Cv[j][x], -Pt[i][x]])
        elif mode == 'planted':
            for i in range(aS, s.M[S]): E.fix(Pt[i][planted[i]])
        elif mode == 'sim':
            pass
        else:
            raise ValueError(mode)
        s.E, s.Cv, s.rows = E, Cv, rows
        return E

    def decode_C(s, model):
        mset = set(l for l in model if l > 0)
        half = [next(x for x in range(19) if s.Cv[j][x] in mset) for j in range(s.h)]
        Lh = s.L // 2
        return half + half[:Lh][::-1]

    def decode_rows(s, model):
        mset = set(l for l in model if l > 0)
        out = []
        for r in s.rows:
            out.append({i: next((x for x in range(19) if v[x] in mset), None) for i, v in r.items()})
        return out


# ------------------------------------------------------------------ CLI
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('mode', choices=['ret', 'lat', 'prefix', 'planted', 'sim', 'info'])
    ap.add_argument('--rec', type=int, default=1)
    ap.add_argument('--q0', type=int, default=5)
    ap.add_argument('--K', type=int, default=1)
    ap.add_argument('--L', type=int, default=17)
    ap.add_argument('--k', type=int, default=None, help='prefix length (prefix mode)')
    ap.add_argument('--idx', type=int, default=None, help='centre index (cen2 numbering) for sim/planted')
    ap.add_argument('--seed', type=int, default=1)
    ap.add_argument('--solver', default='cadical195')
    ap.add_argument('--margin', type=int, default=2)
    ap.add_argument('--nounits', action='store_true')
    ap.add_argument('--cnf', default=None, help='write DIMACS instead of solving')
    a = ap.parse_args()
    t0 = time.time()
    I = Inst(a.rec, a.q0, a.K, a.L, a.margin)
    print('INST', I.describe(), flush=True)
    if a.mode == 'info': return
    Cfix = None; planted = None
    if a.mode in ('sim', 'planted'):
        rng = random.Random(a.seed)
        if a.idx is None:
            tot = 19 ** (a.L // 2) * (10 if a.L % 2 else 1); a.idx = rng.randrange(tot)
        C = centre_of(a.idx, a.L)
        if a.mode == 'sim': Cfix = C[:I.h]
        else:
            rows, gam = simulate(I.lat, a.q0, C, I.S)
            planted = fold(rows[-1])
            print('planted from idx', a.idx, 'C', C, flush=True)
    from pysat.solvers import Solver
    if a.cnf:
        E = I.build(a.mode, Cfix=Cfix, planted=planted, prefix_k=a.k, units=not a.nounits, keep=True)
        with open(a.cnf, 'w') as f:
            f.write(f'p cnf {E.nv} {E.cl.n}\n')
            for c in E.cl.keep: f.write(' '.join(map(str, c)) + ' 0\n')
        print('WROTE', a.cnf, E.nv, E.cl.n); return
    S = Solver(name=a.solver)
    E = I.build(a.mode, Cfix=Cfix, planted=planted, prefix_k=a.k, units=not a.nounits, solver=S)
    print(f'ENC vars={E.nv} clauses={E.cl.n} {time.time()-t0:.1f}s', flush=True)
    r = S.solve()
    dt = time.time() - t0
    if not r:
        print(f'RESULT UNSAT mode={a.mode} rec={a.rec} q0={a.q0} K={a.K} L={a.L} k={a.k} {dt:.1f}s', flush=True)
        return
    model = S.get_model()
    C = I.decode_C(model)
    print(f'RESULT SAT mode={a.mode} rec={a.rec} q0={a.q0} K={a.K} L={a.L} k={a.k} C={C} {dt:.1f}s', flush=True)
    # independent check by klib simulation
    rows, gam = simulate(I.lat, a.q0, C, I.S)
    fin = rows[-1]; tgt = Pword(I.lat, a.q0 + a.K, C)
    pre = next((i for i in range(min(len(fin), len(tgt))) if fin[i] != tgt[i]), min(len(fin), len(tgt)))
    print(f'CHECK klib: clock_ok={gam == [I.g[t % I.p] for t in range(I.S)]} exact_return={fin == tgt} prefix={pre}', flush=True)
    if a.mode == 'sim':
        dec = I.decode_rows(model); bad = 0
        for t, r in enumerate(dec):
            ft = fold(rows[t])
            for i, v in r.items():
                if v is None or ft[i] != v: bad += 1
            for i in range(len(I.R[t])):
                if I.R[t][i] != ft[i]: bad += 1
        print(f'SIMCHECK cells_compared={sum(len(r) for r in dec)} mismatches={bad}', flush=True)
    if a.mode == 'planted':
        print(f'PLANTCHECK image_matches={fold(fin)[I.a[I.S]:] == planted[I.a[I.S]:]} full={fold(fin) == planted}', flush=True)


if __name__ == '__main__':
    main()

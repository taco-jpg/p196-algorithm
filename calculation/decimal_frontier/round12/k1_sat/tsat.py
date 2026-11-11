#!/usr/bin/env python3
"""r12d tsat.py -- general exact template-return SAT for lattice exteriors (any base b; generalises retsat.py).

Pairword (LSB first) P = half ++ centre ++ rev(half),  half = B0 W0^q (rooted lattice prefix, phase 0),
centre = palindromic word whose entries are constants or free SAT symbols (0..2b-2; an odd centre's
midpoint is even).  After S exact reverse-and-add steps the word must equal the target
half' ++ centre' ++ rev(half'),  half' = B0 W0^(q+Kb)  (Kb = lattice blocks gained per side; 0 for a
stationary wall), centre' given by constants / references to free symbols / don't-care.
Lengths must agree with the forced clock: |P_S| = |P_0| + sum g.

Exact step (folded, two carries): lo_i=(P_i+alpha_i)%b, hi_i=(P_i+beta_(i+1))%b, beta continues alpha
through the middle, overflow = beta_0; P'_i = d_i + d_(n'-1-i) with the real digit string d.
Window: columns below a_t = |R_t| - margin come from the two-inlet rooted prefix R_t (exact for every
interior; the clock is forced there), columns [a_t, M_t) are SAT variables.  No pruning anywhere.
"""
import sys, os, time, json, random
_HERE = os.path.dirname(os.path.abspath(__file__))
for _p in (os.path.join(_HERE, 'repo/calculation/decimal_frontier/lattice_kinks/edge_relaxation'),   # Studio work dir copy
           os.path.join(_HERE, '../../lattice_kinks/edge_relaxation')):                              # repository layout
    if os.path.exists(os.path.join(_p, 'klib.py')): sys.path.insert(0, _p); break


# ------------------------------------------------------------------ lattices
class Lattice:
    def __init__(s, name, b, g, B, W):
        s.name, s.b = name, b
        s.g = list(g); s.p = len(g); s.B = B; s.W = W
        s.nB = len(B[0]); s.m = len(W[0])

    def cell(s, t, x):
        t %= s.p
        return s.B[t][x] if x < s.nB else s.W[t][(x - s.nB) % s.m]


def load_lattice(name):
    """rec0/rec1/rec2: decimal p8 lattices (klib); b9r0/b9r1: base-9 merged lattices; b13r0: base 13"""
    if name in ('rec0', 'rec1', 'rec2'):
        from klib import load_rec
        L = load_rec(int(name[3]))
        return Lattice(name, 10, L.g, L.B, L.W)
    fn = {'b9r0': 'cert_b9_rec0.json', 'b9r1': 'cert_b9_rec1.json'}[name]
    for d in (os.path.join(_HERE, 'ctrl'), os.path.join(_HERE, '../../lattice_formats')):   # work dir / repository
        if os.path.exists(os.path.join(d, fn)): break
    J = json.load(open(os.path.join(d, fn)))
    return Lattice(name, J['base'], J['gam'], J['B_t'], J['w_t'])


# ------------------------------------------------------------------ exact reference pieces
def pairword_step_b(P, b):
    """independent generic-base pairword step: normalise, then pair d_i + d_(n'-1-i)"""
    O = []; c = 0
    for v in P:
        s = v + c; O.append(s % b); c = s // b
    n = len(P)
    if c: O.append(c)
    n2 = len(O)
    return [O[i] + O[n2 - 1 - i] for i in range(n2)], n2 - n


def rooted_rows(half0, g, S, b):
    p = len(g); pr = list(half0); rows = [pr]
    for t in range(S):
        k = len(pr)
        if k < 2: raise ValueError(f'rooted prefix vanished at t={t}')
        lo = []; c = 0
        for i in range(k):
            v = pr[i] + c; lo.append(v % b); c = v // b
        outs = []
        for inlet in (0, 1):
            hi = [0] * k; cc = inlet
            for i in range(k - 1, -1, -1):
                v = pr[i] + cc; hi[i] = v % b; cc = v // b
            if cc: new = [lo[0] + 1] + [lo[i] + hi[i - 1] for i in range(1, k)]
            else: new = [lo[i] + hi[i] for i in range(k)]
            outs.append((cc, new))
        if not (outs[0][0] == outs[1][0] == g[t % p]):
            raise ValueError(f'clock not forced by the rooted prefix at t={t}')
        A, Bq = outs[0][1], outs[1][1]
        j = next((i for i in range(k) if A[i] != Bq[i]), k)
        pr = A[:j]; rows.append(pr)
    return rows


def low_carry(row, x, b):
    c = 0
    for i in range(x): c = (row[i] + c) // b
    return c


def fold(P):
    return P[:(len(P) + 1) // 2]


def steps_per_block(lat, K=1):
    num = 2 * lat.m * lat.p * K
    assert num % sum(lat.g) == 0
    return num // sum(lat.g)


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
    def onehot(s, k, amo=True):
        v = s.new(k); s.cl.append(list(v))
        if amo:
            for i in range(k):
                for j in range(i + 1, k): s.cl.append([-v[i], -v[j]])
        return v
    def fix(s, lit): s.cl.append([lit])
    def bit(s, var, val): s.cl.append([var] if val else [-var])


def adder(E, Pv, cin, dig, cout, b):
    """dig = (P + cin) % b, cout = [P + cin >= b]; P one-hot (2b-1), cin/cout SAT variables"""
    for x in range(2 * b - 1):
        for c in (0, 1):
            E.cl.append([-Pv[x], (-cin if c else cin), dig[(x + c) % b]])
        if x >= b: E.cl.append([-Pv[x], cout])
        elif x <= b - 2: E.cl.append([-Pv[x], -cout])
        else:
            E.cl.append([-Pv[x], -cin, cout]); E.cl.append([-Pv[x], cin, -cout])


# ------------------------------------------------------------------ template instance
class Inst:
    """centre0 / centreS: full palindromic centre specs (lists); entries int (constant), ('v', name)
    (free symbol, shared by name between start and target), or None (target only: don't care)."""
    def __init__(s, lat, q0, S, Kb, centre0, centreS, margin=2):
        s.lat = lat; b = s.b = lat.b; s.D = 2 * b - 1
        s.q0, s.S, s.Kb = q0, S, Kb
        s.half0 = lat.B[0] + lat.W[0] * q0; s.H0 = len(s.half0)
        s.final_phase_ok = (S % lat.p == 0)
        s.half1 = lat.B[0] + lat.W[0] * (q0 + Kb); s.H1 = len(s.half1)
        s.c0, s.cS = list(centre0), list(centreS)
        for c in (s.c0, s.cS):
            assert len(c) == len(c[::-1]) and all(c[i] == c[-1 - i] for i in range(len(c))), 'centre spec not palindromic'
        s.n = [2 * s.H0 + len(s.c0)]
        for t in range(S): s.n.append(s.n[-1] + lat.g[t % lat.p])
        assert s.n[S] == 2 * s.H1 + len(s.cS), f'clock/length mismatch {s.n[S]} vs {2*s.H1+len(s.cS)}'
        s.M = [(x + 1) // 2 for x in s.n]
        s.R = rooted_rows(s.half0, lat.g, S, b)
        s.a = [len(r) - margin for r in s.R]
        for t in range(S + 1):
            assert s.a[t] >= 2 and len(s.R[t]) <= s.n[t] // 2, ('rooted prefix reaches the middle column', t)
        s.final_prefix_ok = s.final_phase_ok and s.R[S] == s.half1[:len(s.R[S])]

    def describe(s):
        return (f'{s.lat.name} b={s.b} q0={s.q0} S={s.S} Kb={s.Kb} |c0|={len(s.c0)} |cS|={len(s.cS)} n0={s.n[0]} '
                f'nS={s.n[s.S]} H0={s.H0} H1={s.H1} |R0|={len(s.R[0])} |RS|={len(s.R[s.S])} final_prefix_ok={s.final_prefix_ok}')

    def build(s, solver=None, keep=False, prefix_k=None, units=True, fixvals=None, planted=None, confine_w=None,
              amo_inner=True):
        """amo_inner=False drops the at-most-one clauses of the pairword variables of rows 1..S-1: they are implied
        (two true values v1 != v2 would need (v1+c)%b == (v2+c)%b, i.e. v2 = v1 +- b, and then the carry clauses of
        the next adder contradict), so the model set is unchanged.  Row 0 (free symbols) and row S (target) keep AMO."""
        """fixvals: dict name->value (fix free symbols); planted: folded final word (overrides target)"""
        E = Enc(solver, keep); S = s.S; lat = s.lat; b = s.b; D = s.D; p = lat.p
        s.E = E; s.free = {}
        def freevar(name, mid):
            if name not in s.free:
                v = E.onehot(D); s.free[name] = v
                if fixvals is not None and name in fixvals: E.fix(v[fixvals[name]])
            v = s.free[name]
            if mid:
                for x in range(1, D, 2): E.fix(-v[x])
            return v
        def eqv(u, v):
            for x in range(D):
                E.cl.append([-u[x], v[x]]); E.cl.append([u[x], -v[x]])
        # ---- t = 0
        Pt = {}
        lo0 = min(s.a[1] - 1, s.a[0])
        L0 = len(s.c0); mid0 = (L0 - 1) // 2 if L0 % 2 else None
        for i in range(lo0, s.M[0]):
            if i < s.H0:
                Pt[i] = E.onehot(D); E.fix(Pt[i][s.half0[i]])
            else:
                j = i - s.H0; spec = s.c0[j]
                if isinstance(spec, tuple):
                    Pt[i] = freevar(spec[1], j == mid0)
                else:
                    Pt[i] = E.onehot(D); E.fix(Pt[i][spec])
        s.rows = [dict(Pt)]
        for t in range(S):
            n, n2, gt = s.n[t], s.n[t + 1], lat.g[t % p]
            bt = s.a[t + 1] - 1
            assert 1 <= bt <= s.a[t]
            for i in range(bt, s.a[t]):
                if i not in Pt:
                    Pt[i] = E.onehot(D); E.fix(Pt[i][s.R[t][i]])
            if units and t > 0:
                for i in range(s.a[t], min(len(s.R[t]), s.M[t])): E.fix(Pt[i][s.R[t][i]])
            if confine_w is not None:
                for i in range(s.a[t], s.M[t] - confine_w): E.fix(Pt[i][lat.cell(t, i)])
            nlow = n // 2; odd = n % 2
            ab = E.new()[0]; E.bit(ab, low_carry(s.R[t], bt, b)); alpha = {bt: ab}
            lo = {}; hi = {}
            for i in range(bt, nlow):
                lo[i] = E.onehot(b); alpha[i + 1] = E.new()[0]
                adder(E, Pt[i], alpha[i], lo[i], alpha[i + 1], b)
            beta = {}
            if odd:
                dmid = E.onehot(b); cm = E.new()[0]
                adder(E, Pt[nlow], alpha[nlow], dmid, cm, b); beta[nlow] = cm
            else:
                dmid = None; beta[nlow] = alpha[nlow]
            for i in range(nlow - 1, bt - 1, -1):
                hi[i] = E.onehot(b); beta[i] = E.new()[0]
                adder(E, Pt[i], beta[i + 1], hi[i], beta[i], b)
            def digit(j):
                if j < nlow: return lo[j]
                if odd and j == nlow: return dmid
                if j <= n - 1: return hi[n - 1 - j]
                raise AssertionError('overflow digit inside window')
            Pn = {}
            for i in range(s.a[t + 1], s.M[t + 1]):
                v = E.onehot(D, amo=(amo_inner or t + 1 == S)); Pn[i] = v
                j2 = n2 - 1 - i
                if j2 == i:
                    X = digit(i)
                    for x in range(b): E.cl.append([-X[x], v[2 * x]])
                    for x in range(1, D, 2): E.fix(-v[x])
                else:
                    X, Y = digit(i), digit(j2)
                    for x in range(b):
                        for y in range(b): E.cl.append([-X[x], -Y[y], v[x + y]])
            Pt = Pn; s.rows.append(dict(Pt))
        # ---- final constraints
        aS = s.a[S]
        if confine_w is not None:
            for i in range(aS, s.M[S] - confine_w): E.fix(Pt[i][lat.cell(S, i)])
        if units:
            for i in range(aS, min(len(s.R[S]), s.M[S])): E.fix(Pt[i][s.R[S][i]])
        lim = s.M[S] if prefix_k is None else min(prefix_k, s.M[S])
        LS = len(s.cS); midS = (LS - 1) // 2 if LS % 2 else None
        for i in range(aS, lim):
            if planted is not None:
                E.fix(Pt[i][planted[i]]); continue
            if i < s.H1:
                E.fix(Pt[i][s.half1[i]])
            else:
                j = i - s.H1; spec = s.cS[j]
                if spec is None: continue
                if isinstance(spec, tuple): eqv(freevar(spec[1], j == midS), Pt[i])
                else: E.fix(Pt[i][spec])
        return E

    def decode_free(s, model):
        mset = set(l for l in model if l > 0)
        return {k: next(x for x in range(s.D) if v[x] in mset) for k, v in s.free.items()}

    def realise(s, spec, vals):
        return [vals[e[1]] if isinstance(e, tuple) else e for e in spec]

    def word0(s, vals):
        return s.half0 + s.realise(s.c0, vals) + s.half0[::-1]

    def wordS(s, vals):
        return s.half1 + s.realise(s.cS, vals) + s.half1[::-1]


def simulate(lat, P, S):
    rows = [P]; gam = []
    for t in range(S):
        P, gg = pairword_step_b(P, lat.b); rows.append(P); gam.append(gg)
    return rows, gam


def fixed_centre_specs(L):
    """centre C of length L, all free: names c0..c(h-1), palindromic"""
    h = (L + 1) // 2
    half = [('v', f'c{j}') for j in range(h)]
    return half + half[:L // 2][::-1]


def solve_inst(I, solver_name='cadical195', phase_lattice=False, **kw):
    from pysat.solvers import Solver
    t0 = time.time()
    with Solver(name=solver_name) as S:
        E = I.build(solver=S, **kw)
        if phase_lattice:   # prefer lattice values when deciding (heuristic only; does not change the formula)
            lits = []
            for t, row in enumerate(I.rows):
                for i, v in row.items(): lits.append(v[I.lat.cell(t, i)])
            S.set_phases(lits)
        tenc = time.time() - t0
        r = S.solve()
        model = S.get_model() if r else None
        try:   # Kissat in PySAT has accum_stats but raises NotImplementedError
            stats = S.accum_stats() if hasattr(S, 'accum_stats') else {}
        except NotImplementedError:
            stats = {}
    return r, model, E, tenc, time.time() - t0, stats

#!/usr/bin/env python3
"""r11c: exact SAT encoding of the phase-0 central return problem.

Window = U^m ++ C ++ rev(U^m) (absolute left frame), evolved 120 steps with the
physically forced clock (1000)^30.  Outside the window the word is the periodic
U background (the C-defect cone moves outward <=122 columns in 120 steps, T12
sec. 8; margin 3m >= 162 keeps the boundary inputs exact).  Boundary inputs:
low carry entering column 0 = periodic background carry, and at overflow steps
the mirrored digit of the column left of the window = background row value.
Requirement: final window == U^(m+5) ++ C ++ rev(U^(m+5)).
"""
import sys, time, random, argparse

def T(x, c): return (x + c) // 10

def bg_rows(U, clock):
    """Periodic background rows V_t (cyclic, absolute phase), carries alpha."""
    V = list(U); rows = []; alphas = []
    for g in clock:
        n = 3
        # periodic low carry: iterate twice around
        a = [0] * n; c = 0
        for _ in range(3):
            for i in range(n):
                a[i] = c; c = T(V[i], c)
        b = [0] * (n + 1); cc = 0  # beta_i = carry entering mirrored digit of i from i+1
        bb = [0] * n
        for _ in range(3):
            for i in reversed(range(n)):
                bb[i] = cc  # beta_{i+1} seen by column i
                cc = T(V[i], cc)
        rows.append(list(V)); alphas.append(list(a))
        # bb[i] = beta_{i+1}; beta_i = bb[i-1]
        if g == 0:
            Vn = [(V[i] + a[i]) % 10 + (V[i] + bb[i]) % 10 for i in range(n)]
        else:
            Vn = [(V[i] + a[i]) % 10 + (V[i - 1] + bb[i - 1]) % 10 for i in range(n)]
        V = Vn
    rows.append(list(V))
    return rows, alphas

def simulate(U, C, m, clock):
    """Direct exact window simulation (same model as the SAT encoding)."""
    rows, alphas = bg_rows(U, clock)
    s = list(U) * m + list(C) + list(U[::-1]) * m
    for t, g in enumerate(clock):
        N = len(s); c = alphas[t][0]; e = []
        for x in s:
            z = x + c; e.append(z % 10); c = z // 10
        if g == 0:
            s = [e[j] + e[N - 1 - j] for j in range(N)]
        else:
            e.append((rows[t][2] + c) % 10)
            s = [e[j] + e[N - j] for j in range(N + 1)]
    return s, rows

class Enc:
    def __init__(self):
        self.nv = 0; self.cl = []
    def new(self, k=1):
        r = list(range(self.nv + 1, self.nv + 1 + k)); self.nv += k; return r
    def exactly_one(self, vs):
        self.cl.append(list(vs))
        for i in range(len(vs)):
            for j in range(i + 1, len(vs)):
                self.cl.append([-vs[i], -vs[j]])

def encode(U, Lc, m, clock, fixC=None, final_mode='full', tgt_override=None):
    E = Enc()
    rows, alphas = bg_rows(U, clock)
    M = 3 * m
    N = 2 * M + Lc
    # X[t]: list of one-hot var lists, symmetric aliasing
    def make_X(N):
        half = [E.new(19) for _ in range((N + 1) // 2)]
        for h in half: E.exactly_one(h)
        return [half[min(j, N - 1 - j)] for j in range(N)]
    X = make_X(N)
    init = list(U) * m + [None] * Lc + list(U[::-1]) * m
    Cvars = []
    for j in range(N):
        if init[j] is not None:
            E.cl.append([X[j][init[j]]])
    for j in range(M, M + (Lc + 1) // 2):
        Cvars.append(X[j])
    if Lc % 2:
        mid = X[M + Lc // 2]
        for v in range(1, 19, 2): E.cl.append([-mid[v]])
    if fixC is not None:
        for j, v in enumerate(fixC): E.cl.append([X[M + j][v]])
    for t, g in enumerate(clock):
        # carries c[0..N], digits e[0..N-1] (+ extended)
        c = E.new(N + 1)
        E.cl.append([c[0]] if alphas[t][0] else [-c[0]])
        e = []
        for j in range(N):
            ev = E.new(10); E.exactly_one(ev); e.append(ev)
            for x in range(19):
                for b in (0, 1):
                    lits = [-X[j][x], (-c[j] if b else c[j])]
                    z = x + b
                    E.cl.append(lits + [ev[z % 10]])
                    E.cl.append(lits + ([c[j + 1]] if z >= 10 else [-c[j + 1]]))
        if g == 1:
            ev = E.new(10); E.exactly_one(ev)
            bgv = rows[t][2]
            for b in (0, 1):
                E.cl.append([(-c[N] if b else c[N]), ev[(bgv + b) % 10]])
            e.append(ev)
            Nn = N + 1; pair = lambda j: N - j
        else:
            Nn = N; pair = lambda j: N - 1 - j
        Xn = make_X(Nn)
        for j in range((Nn + 1) // 2):
            p = pair(j)
            for a in range(10):
                for b in range(10):
                    E.cl.append([-e[j][a], -e[p][b], Xn[j][a + b]])
        X = Xn; N = Nn
    tgt = list(U) * (m + 5) + [None] * Lc + list(U[::-1]) * (m + 5)
    if tgt_override is not None: tgt = tgt_override
    assert len(tgt) == N
    for j in range((N + 1) // 2):
        if tgt[j] is not None:
            if final_mode == 'full' or abs(j - (M + 15)) <= final_mode:
                E.cl.append([X[j][tgt[j]]])
    # final C == initial C
    for i, cv in enumerate(Cvars if tgt_override is None else []):
        fv = X[M + 15 + i]
        for v in range(19):
            E.cl.append([-cv[v], fv[v]])
    return E, Cvars, X

def all_U():
    return [tuple((9, a, 18 - a)[r:] + (9, a, 18 - a)[:r]) for a in range(0, 19, 2) for r in range(3)]

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--U', type=int, default=0)
    ap.add_argument('--L', type=int, default=7)
    ap.add_argument('--m', type=int, default=54)
    ap.add_argument('--solver', default='cadical195')
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--timeout', type=float, default=0)
    a = ap.parse_args()
    clock = [1, 0, 0, 0] * 30
    U = all_U()[a.U]
    from pysat.solvers import Solver
    if a.selftest:
        sys.path.insert(0, '.')
        from cone import iterate
        random.seed(5)
        for trial in range(6):
            U = random.choice(all_U()); Lc = random.choice([1, 2, 5, 8, 13])
            h = [random.randrange(19) for _ in range((Lc + 1) // 2)]
            if Lc % 2: h[-1] &= ~1
            C = h + h[::-1] if Lc % 2 == 0 else h + h[-2::-1]
            s, _ = simulate(U, C, 54, clock)
            core, shift, _ = iterate(U, C, k=100, clock=clock)
            # align centres
            a0 = (len(s) - len(core)) // 2 if len(s) >= len(core) else None
            ok = s[a0:a0 + len(core)] == core if a0 is not None else s == core[(len(core)-len(s))//2:(len(core)+len(s))//2]
            # also check that edges stay background-periodic
            E, Cv, X = encode(U, Lc, 54, clock, fixC=C)
            with Solver(name=a.solver, bootstrap_with=E.cl) as S:
                sat = S.solve()
            tgt = list(U) * 59 + C + list(U[::-1]) * 59
            print('selftest', U, C, 'sim-vs-AC46core', ok, 'sim_return', s == tgt, 'SAT', sat, flush=True)
            assert ok and sat == (s == tgt)
        # positive control: target = simulated image of a random C, C left free
        for trial in range(2):
            U = random.choice(all_U()); Lc = 6
            h = [random.randrange(19) for _ in range(3)]; C = h + h[::-1]
            s, _ = simulate(U, C, 54, clock)
            E, Cv, X = encode(U, Lc, 54, clock, tgt_override=s)
            with Solver(name=a.solver, bootstrap_with=E.cl) as S:
                sat = S.solve(); mod = set(l for l in S.get_model() if l > 0)
            got = [next(v for v in range(19) if cv[v] in mod) for cv in Cv]
            print('positive control', U, C, 'SAT', sat, 'found half', got, flush=True)
            assert sat and simulate(U, got + got[::-1], 54, clock)[0] == s
        sys.exit(0)
    t0 = time.time()
    E, Cv, X = encode(U, a.L, a.m, clock)
    print(f'U={U} L={a.L} vars={E.nv} clauses={len(E.cl)} enc={time.time()-t0:.1f}s', flush=True)
    with Solver(name=a.solver, bootstrap_with=E.cl) as S:
        r = S.solve()
        print('RESULT', 'SAT' if r else 'UNSAT', f'time={time.time()-t0:.1f}s', flush=True)
        if r:
            mod = set(l for l in S.get_model() if l > 0)
            half = [next(v for v in range(19) if cv[v] in mod) for cv in Cv]
            C = half + half[::-1] if a.L % 2 == 0 else half + half[-2::-1]
            print('WITNESS_C', C, flush=True)

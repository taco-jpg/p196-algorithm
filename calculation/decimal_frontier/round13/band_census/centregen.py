#!/usr/bin/env python3
"""r13a: general centre SAT (style of r11c satc.py): window = V^m C rev(V^m) (absolute left frame), any base, any clock, any band V
(V = band word at time 0, phase 0 at the window start).  Evolve N steps with the forced clock; outside the window the word is the periodic
V background (requires m large: margin s*m > right-front radius + Delta).  Target: V^(m+j) C rev(V^(m+j)) (j copies gained per N steps,
S_N = 2*s*j overflows).  Selftest: --selftest (fixed C versus direct window simulation; target = simulated image with free C is SAT)."""
import sys, time, random, argparse
import bandsat as BS

def bg(V, clock, b):
    rows, As, Bs, Ls, Hs = BS.background(V, clock, b)
    return rows, As

def simulate(V, C, m, clock, b):
    """Direct window simulation in the absolute left frame (same model as the encoding)."""
    rows, alphas = bg(V, clock, b)
    s = list(V) * m + list(C) + list(V[::-1]) * m
    for t, g in enumerate(clock):
        N = len(s); c = alphas[t][0]; e = []
        for x in s:
            z = x + c; e.append(z % b); c = z // b
        if g == 0:
            s = [e[j] + e[N - 1 - j] for j in range(N)]
        else:
            e.append((rows[t][-1] + c) % b)
            s = [e[j] + e[N - j] for j in range(N + 1)]
    return s, rows

class Enc:
    def __init__(self): self.nv = 0; self.cl = []
    def new(self, k=1):
        r = list(range(self.nv + 1, self.nv + 1 + k)); self.nv += k; return r
    def exactly_one(self, vs):
        self.cl.append(list(vs))
        for i in range(len(vs)):
            for j in range(i + 1, len(vs)):
                self.cl.append([-vs[i], -vs[j]])

def encode(V, Lc, m, clock, j_shift, b, fixC=None, tgt_override=None):
    E = Enc(); NL = 2 * b - 1; sV = len(V)
    rows, alphas = bg(V, clock, b)
    M = sV * m
    N = 2 * M + Lc
    def make_X(N):
        half = [E.new(NL) for _ in range((N + 1) // 2)]
        for h in half: E.exactly_one(h)
        return [half[min(j, N - 1 - j)] for j in range(N)]
    X = make_X(N)
    init = list(V) * m + [None] * Lc + list(V[::-1]) * m
    Cvars = []
    for j in range(N):
        if init[j] is not None:
            E.cl.append([X[j][init[j]]])
    for j in range(M, M + (Lc + 1) // 2):
        Cvars.append(X[j])
    if Lc % 2:
        mid = X[M + Lc // 2]
        for v in range(1, NL, 2): E.cl.append([-mid[v]])
    if fixC is not None:
        for j, v in enumerate(fixC): E.cl.append([X[M + j][v]])
    for t, g in enumerate(clock):
        c = E.new(N + 1)
        E.cl.append([c[0]] if alphas[t][0] else [-c[0]])
        e = []
        for j in range(N):
            ev = E.new(b); E.exactly_one(ev); e.append(ev)
            for x in range(NL):
                for a in (0, 1):
                    lits = [-X[j][x], (-c[j] if a else c[j])]
                    z = x + a
                    E.cl.append(lits + [ev[z % b]])
                    E.cl.append(lits + ([c[j + 1]] if z >= b else [-c[j + 1]]))
        if g == 1:
            ev = E.new(b); E.exactly_one(ev)
            bgv = rows[t][-1]
            for a in (0, 1):
                E.cl.append([(-c[N] if a else c[N]), ev[(bgv + a) % b]])
            e.append(ev)
            Nn = N + 1; pair = lambda j: N - j
        else:
            Nn = N; pair = lambda j: N - 1 - j
        Xn = make_X(Nn)
        for j in range((Nn + 1) // 2):
            p = pair(j)
            for d1 in range(b):
                for d2 in range(b):
                    E.cl.append([-e[j][d1], -e[p][d2], Xn[j][d1 + d2]])
        X = Xn; N = Nn
    Vfin = rows[len(clock)]
    if tgt_override is None:
        m1 = m + j_shift
        M1 = sV * m1
        assert Vfin == list(V) or True
        tgt = list(Vfin) * m1 + [None] * Lc + list(Vfin[::-1]) * m1
    else:
        tgt = tgt_override
    assert len(tgt) == N, (len(tgt), N)
    for j in range((N + 1) // 2):
        if tgt[j] is not None:
            E.cl.append([X[j][tgt[j]]])
    if tgt_override is None:
        M1 = sV * (m + j_shift)
        for i, cv in enumerate(Cvars):
            fv = X[M1 + i]
            for v in range(NL):
                E.cl.append([-cv[v], fv[v]])
    return E, Cvars, X, rows

def selftest(b=10):
    from pysat.solvers import Solver
    random.seed(7)
    for trial in range(12):
        sV = random.choice([2, 3, 4, 5])
        V = [random.randrange(2 * b - 1) for _ in range(sV)]
        if all(v == b - 1 for v in V): V[0] = 0
        Lc = random.choice([2, 5, 6, 9])
        h = [random.randrange(2 * b - 1) for _ in range((Lc + 1) // 2)]
        if Lc % 2: h[-1] &= ~1
        C = h + h[::-1] if Lc % 2 == 0 else h + h[-2::-1]
        T = 24
        clock = [random.randrange(2) for _ in range(T)]
        m = (2 * T + 30) // sV + 3
        try:
            s, rows = simulate(V, C, m, clock, b)
        except StopIteration:
            print('  (all-(b-1) row during evolution; retry)', flush=True)
            continue
        E, Cv, X, rows2 = encode(V, Lc, m, clock, 0, b, fixC=C, tgt_override=s)
        with Solver(name='cadical195', bootstrap_with=E.cl) as S:
            r = S.solve()
        print('selftest', V, C, 'clock', ''.join(map(str, clock)), 'sim len', len(s), 'SAT' if r else 'UNSAT', flush=True)
        assert r
        # changed target must be UNSAT
        s2 = list(s); pos = len(s2) // 2
        s2[pos] = (s2[pos] + 1) % (2 * b - 1)
        s2[len(s2) - 1 - pos] = s2[pos]
        E2, Cv2, X2, rows3 = encode(V, Lc, m, clock, 0, b, fixC=C, tgt_override=s2)
        with Solver(name='cadical195', bootstrap_with=E2.cl) as S2:
            r2 = S2.solve()
        print('  changed target:', 'SAT' if r2 else 'UNSAT', flush=True)
        assert not r2
    print('SELFTEST PASS', flush=True)

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--b', type=int, default=10); ap.add_argument('--clock', default='1000'); ap.add_argument('--V', default=''); ap.add_argument('--N', type=int, default=120)
    ap.add_argument('--j', type=int, default=1); ap.add_argument('--Lc', type=int, default=4); ap.add_argument('--m', type=int, default=0); ap.add_argument('--solver', default='cadical195')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        selftest(a.b); selftest(9); sys.exit(0)
    from pysat.solvers import Solver
    V = [int(x) for x in a.V.split(',')]
    cl0 = [int(c) for c in a.clock]
    clock = [cl0[t % len(cl0)] for t in range(a.N)]
    rows, As, Bs, Ls, Hs = BS.background(V, clock, a.b)
    assert rows[a.N] == list(V), 'V not N-periodic'
    rf = BS.right_fronts(rows, a.b, clock)
    m = a.m if a.m else (rf[a.N] + 2 * len(V) + 8) // len(V) + 2
    t0 = time.time()
    E, Cv, X, rows2 = encode(V, a.Lc, m, clock, a.j, a.b)
    print(f'V={V} Lc={a.Lc} m={m} j={a.j} N={a.N} vars={E.nv} clauses={len(E.cl)} enc={time.time()-t0:.1f}s', flush=True)
    with Solver(name=a.solver, bootstrap_with=E.cl) as S:
        r = S.solve()
        print('RESULT', 'SAT' if r else 'UNSAT', f'time={time.time()-t0:.1f}s', flush=True)
        if r:
            mod = set(l for l in S.get_model() if l > 0)
            half = [next(v for v in range(2 * a.b - 1) if cv[v] in mod) for cv in Cv]
            C = half + half[::-1] if a.Lc % 2 == 0 else half + half[-2::-1]
            print('WITNESS_C', C, flush=True)

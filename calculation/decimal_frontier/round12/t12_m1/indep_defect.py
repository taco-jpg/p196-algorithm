#!/usr/bin/env python3
"""r12a INDEPENDENT re-implementation of the seam defect sets D_R(V).

Shares NO code with seamsat.py / rigid.py / rigid2.py / seam_check.py / cone.py: own constants, own cyclic
background, own CNF encoding ("enc2"), own genuine-orbit extraction from Python big integers.

Folded two-carry law (LSD-first digits d, length L, pair word P_i = d_i + d_(L-1-i)):
  c_0 = 0, c_(i+1) = (P_i + c_i) // 10, e_i = (P_i + c_i) % 10, gamma = c_L.
  folded:  alpha_i = c_i,  beta_x = c_(L-x),  hi_i = e_(L-1-i) = (P_i + beta_(i+1)) % 10,
           beta_i = (P_i + beta_(i+1)) // 10.
  next row: gamma=0: P'_i = e_i + hi_i;  gamma=1: P'_i = e_i + hi_(i-1)  (bulk columns).
enc2 (direct relations, no digit variables):
  X[t][i] one-hot 0..18 (i in [x0,x1)), A[t][i] (i in [x0,x1]) low carry entering column i,
  C[t][i] (i in [x0,x1]) high carry entering column i-1 from column i, H[t] one-hot 0..9 at overflow steps.
  A[t][x0] free, H[t] free (left port), C[t][x1] = constant (right port).
  X=x & A[i]=a -> A[i+1] = [x+a>=10];  X=x & C[i+1]=b -> C[i] = [x+b>=10]
  gamma=0: X[i]=x & A[i]=a & C[i+1]=b -> X'[i] = (x+a)%10 + (x+b)%10
  gamma=1: X[i]=x & A[i]=a & X[i-1]=w & C[i]=b -> X'[i] = (x+a)%10 + (w+b)%10   (i > x0)
           X[x0]=x & A[x0]=a & H=d -> X'[x0] = (x+a)%10 + d
Clock gamma_t = [t % 4 == 0] (phase-0 T12 clock).

Modes
  defect  --V v --R r [--solver s] : D_R(V) by enumeration (V = index 0..29 in the order of T12: a=0,2,..,18; rotation 0,1,2).
  genuine --V v --Lj n --R r --seed s : validation of enc2 on a genuine big-integer orbit of
           P = H C rev(H), H = B0 W0^14 J V^K (random J, C); window [y-R, y+M), y = start of the V band:
           (i) genuine beta at x1 == cyclic V background; (ii) genuine init + genuine ports -> genuine final SAT;
           (iii) one final value changed -> UNSAT; (iv) return required with genuine ports -> SAT iff genuine returns.
"""
import sys, time, random, argparse

sys.set_int_max_str_digits(1000000)
B0 = [10, 4, 6, 6, 7, 12, 9, 16, 16, 13, 0, 2, 10, 17, 7, 0, 18, 6, 5, 18, 4, 18, 14, 9, 14, 8, 12, 17, 10, 4, 6, 4, 0, 5]
W0 = [5, 18, 4, 8, 1, 15, 4, 0, 5]
M = 171
STEPS = 120


def rotations():
    out = []
    for a in range(0, 19, 2):
        w = [9, a, 18 - a]
        for r in range(3):
            out.append(w[r:] + w[:r])
    return out


def gamma(t):
    return 1 if t % 4 == 0 else 0


def cyclic_background(V):
    """rows[t] = (row, alpha_in[j], beta_in[j]) for the 3-periodic band; beta_in[j] = carry entering col j from j+1."""
    row = list(V); n = len(row); res = []
    for t in range(STEPS):
        a = [0] * n; c = 0
        for _ in range(4):
            for j in range(n):
                a[j] = c; c = (row[j] + c) // 10
        bi = [0] * n; c = 0
        for _ in range(4):
            for j in reversed(range(n)):
                bi[j] = c; c = (row[j] + c) // 10
        res.append((list(row), a, bi))
        lo = [(row[j] + a[j]) % 10 for j in range(n)]
        hi = [(row[j] + bi[j]) % 10 for j in range(n)]
        g = gamma(t)
        row = [lo[j] + (hi[j - 1] if g else hi[j]) for j in range(n)]
    return res, row


class CNF:
    def __init__(self, solver):
        self.S = solver; self.nv = 0; self.n = 0

    def var(self):
        self.nv += 1; return self.nv

    def onehot(self, k):
        vs = [self.var() for _ in range(k)]
        self.add(vs)
        for i in range(k):
            for j in range(i + 1, k):
                self.add([-vs[i], -vs[j]])
        return vs

    def add(self, c):
        self.S.add_clause(c); self.n += 1

    def bit(self, v, b):  # literal "v == b"
        return v if b else -v


def build(cnf, x0, x1, init, right_bits, left_fixed=None):
    """returns X0, XT, Aport, Hport (lists).  left_fixed = (alpha bits[120], h digits[30]) or None."""
    X = {i: cnf.onehot(19) for i in range(x0, x1)}
    X0 = dict(X)
    for i, v in init.items():
        cnf.add([X[i][v]])
    Aport = []; Hport = []
    for t in range(STEPS):
        g = gamma(t)
        A = {i: cnf.var() for i in range(x0, x1 + 1)}
        C = {i: cnf.var() for i in range(x0, x1 + 1)}
        cnf.add([cnf.bit(C[x1], right_bits[t])])
        Aport.append(A[x0])
        if left_fixed is not None:
            cnf.add([cnf.bit(A[x0], left_fixed[0][t])])
        for i in range(x0, x1):
            for x in range(19):
                for b in (0, 1):
                    cnf.add([-X[i][x], -cnf.bit(A[i], b), cnf.bit(A[i + 1], 1 if x + b >= 10 else 0)])
                    cnf.add([-X[i][x], -cnf.bit(C[i + 1], b), cnf.bit(C[i], 1 if x + b >= 10 else 0)])
        Xn = {i: cnf.onehot(19) for i in range(x0, x1)}
        if g == 0:
            for i in range(x0, x1):
                for x in range(19):
                    for a in (0, 1):
                        for b in (0, 1):
                            cnf.add([-X[i][x], -cnf.bit(A[i], a), -cnf.bit(C[i + 1], b),
                                     Xn[i][(x + a) % 10 + (x + b) % 10]])
        else:
            H = cnf.onehot(10); Hport.append(H)
            if left_fixed is not None:
                cnf.add([H[left_fixed[1][len(Hport) - 1]]])
            for x in range(19):
                for a in (0, 1):
                    for d in range(10):
                        cnf.add([-X[x0][x], -cnf.bit(A[x0], a), -H[d], Xn[x0][(x + a) % 10 + d]])
            for i in range(x0 + 1, x1):
                for x in range(19):
                    for a in (0, 1):
                        for w in range(19):
                            for b in (0, 1):
                                cnf.add([-X[i][x], -cnf.bit(A[i], a), -X[i - 1][w], -cnf.bit(C[i], b),
                                         Xn[i][(x + a) % 10 + (w + b) % 10]])
        X = Xn
    return X0, X, Aport, Hport


def right_port_bits(V, x1_phase=0):
    bg, last = cyclic_background(V)
    assert last == list(V), 'band does not return'
    # column x1-1 has phase (x1_phase-1) mod 3; carry entering it from x1
    return [bg[t][2][(x1_phase - 1) % 3] for t in range(STEPS)]


def defect(a):
    from pysat.solvers import Solver
    V = rotations()[a.V]; R = a.R; t0 = time.time()
    y = 10000; x0 = y - R; x1 = y + M
    right = right_port_bits(V)
    D = []; blocked = []
    while True:
        S = Solver(name=a.solver); cnf = CNF(S)
        init = {i: V[(i - y) % 3] for i in range(y, x1)}
        X0, XT, Ap, Hp = build(cnf, x0, x1, init, right)
        for i in range(x0, x1):
            for v in range(19):
                cnf.add([-X0[i][v], XT[i][v]])
        cnf.add([-X0[y - 1][V[2]]])
        for v in blocked:
            cnf.add([-X0[y - 1][v]])
        if not D and not blocked:
            print(f'indep defect V={V} R={R} M={M} vars={cnf.nv} clauses={cnf.n} solver={a.solver} enc={time.time()-t0:.0f}s', flush=True)
        r = S.solve()
        if not r:
            S.delete(); break
        m = set(l for l in S.get_model() if l > 0)
        cols = [next(v for v in range(19) if X0[i][v] in m) for i in range(x0, y)]
        D.append(cols[-1]); blocked.append(cols[-1])
        print('DEFECT', cols[-1], 'free columns', cols, f'{time.time()-t0:.0f}s', flush=True)
        S.delete()
    print('RESULT', 'D=' + str(sorted(D)), 'EMPTY' if not D else 'NONEMPTY', f'{time.time()-t0:.0f}s', flush=True)


# ---------------- genuine big-integer orbit -----------------
def realize(P):
    L = len(P); d = [0] * L
    for i in range(L // 2):
        d[i] = max(0, P[i] - 9); d[L - 1 - i] = P[i] - d[i]
    if L % 2:
        assert P[L // 2] % 2 == 0
        d[L // 2] = P[L // 2] // 2
    assert d[-1] > 0 and all(0 <= x <= 9 for x in d)
    return d


def genuine(a):
    from pysat.solvers import Solver
    rnd = random.Random(a.seed)
    V = rotations()[a.V]; R = a.R; n = a.Lj; K = 120
    J = [rnd.randrange(19) for _ in range(n)]
    h = [rnd.randrange(19) for _ in range(4)]; Cc = h + h[::-1]
    H = B0 + W0 * 14 + J + V * K
    P = H + Cc + H[::-1]
    d = realize(P)
    N = int(''.join(map(str, reversed(d))))
    y = 34 + 9 * 14 + n; x0 = y - R; x1 = y + M
    rows = []; al = []; hd = []; be = []
    for t in range(STEPS + 1):
        s = str(N)[::-1]; dd = [int(ch) for ch in s]; L = len(dd)
        Pt = [dd[i] + dd[L - 1 - i] for i in range(L)]
        rows.append(Pt[:x1 + 5])
        if t == STEPS:
            break
        c = [0] * (L + 1); e = [0] * L
        for i in range(L):
            z = Pt[i] + c[i]; e[i] = z % 10; c[i + 1] = z // 10
        assert c[L] == gamma(t), 'clock'
        al.append(c[x0]); be.append(c[L - x1])
        if gamma(t):
            hd.append(e[L - x0])          # hi_(x0-1) = e_(L-1-(x0-1))
        N2 = N + int(str(N)[::-1])
        assert [int(ch) for ch in str(N2)[::-1]][:L] == e
        N = N2
    out = {'V': V, 'J': J, 'C': Cc, 'R': R}
    out['i_right_is_background'] = (be == right_port_bits(V))
    init = {i: rows[0][i] for i in range(x0, x1)}
    fin = {i: rows[STEPS][i] for i in range(x0, x1)}
    for test in ('ii', 'iii', 'iv'):
        S = Solver(name=a.solver); cnf = CNF(S)
        X0, XT, Ap, Hp = build(cnf, x0, x1, init, be, left_fixed=(al, hd))
        if test == 'ii':
            for i, v in fin.items():
                cnf.add([XT[i][v]])
        elif test == 'iii':
            i = rnd.randrange(x0, x1); v = (fin[i] + 1 + rnd.randrange(17)) % 19
            for i2, v2 in fin.items():
                cnf.add([XT[i2][v if i2 == i else v2]])
        else:
            for i in range(x0, x1):
                cnf.add([XT[i][init[i]]])
        out[test] = S.solve(); S.delete()
    out['genuine_window_returns'] = all(fin[i] == init[i] for i in range(x0, x1))
    out['PASS'] = out['i_right_is_background'] and out['ii'] and not out['iii'] and (out['iv'] == out['genuine_window_returns'])
    print(out, flush=True)


# ---------------- centre side (comoving), independent version -----------------
def build_centre(cnf, x0, x1, init, V, left_bits=None, left_row2=None, right_bits=None):
    """enc2 with EXACT left port (background alpha at x0; overflow-step left digit H linked to C[x0] and the
    background value of column x0-1) and FREE right port (unless right_bits given)."""
    bg, _ = cyclic_background(V)
    if left_bits is None:
        left_bits = [bg[t][1][0] for t in range(STEPS)]           # alpha entering phase-0 column x0
        left_row2 = [bg[t][0][2] for t in range(STEPS)]           # value of column x0-1 (phase 2)
    X = {i: cnf.onehot(19) for i in range(x0, x1)}
    X0 = dict(X)
    for i, v in init.items():
        cnf.add([X[i][v]])
    Cport = []
    for t in range(STEPS):
        g = gamma(t)
        A = {i: cnf.var() for i in range(x0, x1 + 1)}
        C = {i: cnf.var() for i in range(x0, x1 + 1)}
        cnf.add([cnf.bit(A[x0], left_bits[t])])
        Cport.append(C[x1])
        if right_bits is not None:
            cnf.add([cnf.bit(C[x1], right_bits[t])])
        for i in range(x0, x1):
            for x in range(19):
                for b in (0, 1):
                    cnf.add([-X[i][x], -cnf.bit(A[i], b), cnf.bit(A[i + 1], 1 if x + b >= 10 else 0)])
                    cnf.add([-X[i][x], -cnf.bit(C[i + 1], b), cnf.bit(C[i], 1 if x + b >= 10 else 0)])
        Xn = {i: cnf.onehot(19) for i in range(x0, x1)}
        if g == 0:
            for i in range(x0, x1):
                for x in range(19):
                    for a in (0, 1):
                        for b in (0, 1):
                            cnf.add([-X[i][x], -cnf.bit(A[i], a), -cnf.bit(C[i + 1], b),
                                     Xn[i][(x + a) % 10 + (x + b) % 10]])
        else:
            H = cnf.onehot(10)
            for b in (0, 1):
                cnf.add([-cnf.bit(C[x0], b), H[(left_row2[t] + b) % 10]])
            for x in range(19):
                for a in (0, 1):
                    for d in range(10):
                        cnf.add([-X[x0][x], -cnf.bit(A[x0], a), -H[d], Xn[x0][(x + a) % 10 + d]])
            for i in range(x0 + 1, x1):
                for x in range(19):
                    for a in (0, 1):
                        for w in range(19):
                            for b in (0, 1):
                                cnf.add([-X[i][x], -cnf.bit(A[i], a), -X[i - 1][w], -cnf.bit(C[i], b),
                                         Xn[i][(x + a) % 10 + (w + b) % 10]])
        X = Xn
    return X0, X, Cport


def cdefect(a):
    from pysat.solvers import Solver
    V = rotations()[a.V]; R = a.R; Mc = 141; SH = 15; t0 = time.time()
    x0 = 30000; y = x0 + Mc; x1 = y + R
    D = []
    while True:
        S = Solver(name=a.solver); cnf = CNF(S)
        init = {i: V[(i - x0) % 3] for i in range(x0, y)}
        X0, XT, Cp = build_centre(cnf, x0, x1, init, V)
        for i in range(x0, x1):
            if i - SH < y:
                cnf.add([XT[i][V[(i - x0) % 3]]])
            else:
                for v in range(19):
                    cnf.add([-X0[i - SH][v], XT[i][v]])
        cnf.add([-X0[y][V[0]]])
        for v in D:
            cnf.add([-X0[y][v]])
        if not D:
            print(f'indep cdefect V={V} R={R} Mc={Mc} shift={SH} vars={cnf.nv} clauses={cnf.n} solver={a.solver} enc={time.time()-t0:.0f}s', flush=True)
        r = S.solve()
        if not r:
            S.delete(); break
        m = set(l for l in S.get_model() if l > 0)
        cols = [next(v for v in range(19) if X0[i][v] in m) for i in range(y, x1)]
        D.append(cols[0])
        print('DEFECT', cols[0], 'free columns', cols, f'{time.time()-t0:.0f}s', flush=True)
        S.delete()
    print('RESULT', 'E=' + str(sorted(D)), 'EMPTY' if not D else 'NONEMPTY', f'{time.time()-t0:.0f}s', flush=True)


def cgenuine(a):
    """genuine big-integer orbit of B0 W0^14 J V^K C rev(...), window [y-141, y+R) with y = first column of C:
    (i) genuine left port == cyclic background; (ii) genuine init + genuine right port -> genuine final (unshifted) SAT;
    (iii) changed final value -> UNSAT."""
    from pysat.solvers import Solver
    rnd = random.Random(a.seed)
    V = rotations()[a.V]; R = a.R; n = a.Lj; K = 120
    J = [rnd.randrange(19) for _ in range(n)]
    hlen = R + 3
    h = [rnd.randrange(19) for _ in range(hlen)]; Cc = h + h[::-1]
    H = B0 + W0 * 14 + J + V * K
    P = H + Cc + H[::-1]
    d = realize(P)
    N = int(''.join(map(str, reversed(d))))
    y = 34 + 9 * 14 + n + 3 * K; x0 = y - 141; x1 = y + R
    rows = []; al = []; r2 = []; be = []
    for t in range(STEPS + 1):
        s = str(N)[::-1]; dd = [int(ch) for ch in s]; L = len(dd)
        Pt = [dd[i] + dd[L - 1 - i] for i in range(L)]
        assert x1 + 2 < L // 2
        rows.append(Pt[:x1 + 5])
        if t == STEPS:
            break
        c = [0] * (L + 1)
        for i in range(L):
            c[i + 1] = (Pt[i] + c[i]) // 10
        assert c[L] == gamma(t)
        al.append(c[x0]); r2.append(Pt[x0 - 1]); be.append(c[L - x1])
        N = N + int(str(N)[::-1])
    bg, _ = cyclic_background(V)
    out = {'V': V, 'C': Cc, 'R': R}
    out['i_left_port_is_background'] = (al == [bg[t][1][0] for t in range(STEPS)] and r2 == [bg[t][0][2] for t in range(STEPS)])
    init = {i: rows[0][i] for i in range(x0, x1)}
    fin = {i: rows[STEPS][i] for i in range(x0, x1)}
    for test in ('ii', 'iii'):
        S = Solver(name=a.solver); cnf = CNF(S)
        X0, XT, Cp = build_centre(cnf, x0, x1, init, V, left_bits=al, left_row2=r2, right_bits=be)
        j = rnd.randrange(x0, x1); w = (fin[j] + 1 + rnd.randrange(17)) % 19
        for i, v in fin.items():
            cnf.add([XT[i][w if (test == 'iii' and i == j) else v]])
        out[test] = S.solve(); S.delete()
    out['PASS'] = out['i_left_port_is_background'] and out['ii'] and not out['iii']
    print(out, flush=True)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('mode')
    ap.add_argument('--V', type=int, default=0)
    ap.add_argument('--R', type=int, default=12)
    ap.add_argument('--Lj', type=int, default=12)
    ap.add_argument('--seed', type=int, default=1)
    ap.add_argument('--solver', default='glucose42')
    a = ap.parse_args()
    {'defect': defect, 'genuine': genuine, 'cdefect': cdefect, 'cgenuine': cgenuine}[a.mode](a)

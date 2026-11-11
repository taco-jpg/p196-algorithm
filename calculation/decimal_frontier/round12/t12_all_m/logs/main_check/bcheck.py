#!/usr/bin/env python3
"""Main-session independent check of r12f's B_1 = empty.  Written from the folded law only (r12f FINAL sec. 1, 4);
no code shared with brestore.py / mbres.py / mdefect.py / mindep.py.  Plain (non-group) instance:
columns [y-R, y-1) free, column y-1 != V[2], columns [y, y+W) = V^inf, free left port (low carry every step, high digit of
column y-R-1 at overflow steps), right port = background beta, standard clock, T = 120, final: [y+g, y+W) = V^inf.

modes:
  cones                         recurrences, row periods, isolated 9s
  validate SEED                 genuine big-integer orbit vs the encoding
  plain A ROT R [--g G] [--nofor] [--solver S]    A = even letter a, ROT = 0,1,2 rotation of (9,a,18-a)
"""
import sys, random, time, argparse, resource
from pysat.solvers import Solver

T = 120
W = 172


def gamma(s):
    return 1 if s % 4 == 0 else 0


def rotation(a, rot):
    u = [9, a, 18 - a]
    return u[rot:] + u[:rot]


def row_step(x, g):
    n = len(x)
    assert any(v != 9 for v in x), x
    al = [0] * n
    for _ in range(3):
        for c in range(n):
            al[(c + 1) % n] = 1 if x[c] + al[c] >= 10 else 0
    be = [0] * n
    for _ in range(3):
        for c in range(n - 1, -1, -1):
            be[c] = 1 if x[c] + be[(c + 1) % n] >= 10 else 0
    lo = [(x[c] + al[c]) % 10 for c in range(n)]
    hi = [(x[c] + be[(c + 1) % n]) % 10 for c in range(n)]
    y = [lo[c] + (hi[(c - 1) % n] if g else hi[c]) for c in range(n)]
    return y, al, be


def background(V, n=T):
    rows, As, Bs = [list(V)], [], []
    for s in range(n):
        y, al, be = row_step(rows[s], gamma(s))
        rows.append(y)
        As.append(al)
        Bs.append(be)
    return rows, As, Bs


def build(V, R, g=0, foreign=True, solver='kissat404', fix=None, final=True, forbid=None):
    N = R + W
    rows, As, Bs = background(V)
    assert rows[T] == list(V), (V, rows[T])
    nv = 0

    def new(k):
        nonlocal nv
        r = nv + 1
        nv += k
        return r

    X = [[new(19) for c in range(N)] for s in range(T + 1)]
    AL = [[new(1) for c in range(N + 1)] for s in range(T)]
    BE = [[new(1) for c in range(N + 1)] for s in range(T)]
    LO = [[new(10) for c in range(N)] for s in range(T)]
    HI = [[new(10) for c in range(N)] for s in range(T)]
    HL = [new(10) if gamma(s) else 0 for s in range(T)]
    S = Solver(name=solver)
    add = S.add_clause
    ncl = [0]

    def amo(base, k):
        for i in range(k):
            for j in range(i + 1, k):
                add([-(base + i), -(base + j)])
        ncl[0] += k * (k - 1) // 2

    for c in range(N):
        add([X[0][c] + v for v in range(19)])
    for s in range(T + 1):
        for c in range(N):
            amo(X[s][c], 19)
    for s in range(T):
        g_s = gamma(s)
        al, be = AL[s], BE[s]
        if g_s:
            add([HL[s] + d for d in range(10)])
            amo(HL[s], 10)
        # right port: background high carry at band coordinate N-R
        add([be[N] if Bs[s][(N - R) % 3] else -be[N]])
        for c in range(N):
            xs = X[s][c]
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
                for a in (0, 1):
                    d = (v + a) % 10
                    add([-(xs + v), (-al[c] if a else al[c]), LO[s][c] + d])
                    add([-(xs + v), (-be[c + 1] if a else be[c + 1]), HI[s][c] + d])
            amo(LO[s][c], 10)
            amo(HI[s][c], 10)
            if g_s:
                h = HI[s][c - 1] if c > 0 else HL[s]
            else:
                h = HI[s][c]
            for d1 in range(10):
                for d2 in range(10):
                    add([-(LO[s][c] + d1), -(h + d2), X[s + 1][c] + d1 + d2])
    # initial band
    for c in range(R, N):
        add([X[0][c] + V[(c - R) % 3]])
    if foreign:
        add([-(X[0][R - 1] + V[2])])
    if final:
        for c in range(R + g, N):
            add([X[T][c] + V[(c - R) % 3]])
    if fix is not None:
        for c, v in fix['x0'].items():
            add([X[0][c] + v])
        for s in range(T):
            add([AL[s][0] if fix['al0'][s] else -AL[s][0]])
            if gamma(s):
                add([HL[s] + fix['hl'][s]])
    if forbid is not None:
        c0, v0 = forbid
        add([-(X[T][c0] + v0)])
    return S, X, N, nv


def cones():
    bad = 0
    summary = {}
    for a in range(0, 19, 2):
        for rot in range(3):
            V = rotation(a, rot)
            rows, As, Bs = background(V, 120 * 40)
            # minimal period and isolated 9s
            per = next(t for t in range(4, 121 * 40, 4) if rows[t] == rows[0])  # same clock phase: t = 0 mod 4
            nines = {sum(1 for v in rows[t] if v == 9) for t in range(120 * 40)}
            l = r = 0
            ls = {}
            maxep = 0
            start = 0
            lv = [0]
            for t in range(120 * 40):
                v = rows[t]
                l += 1 + (1 if v[l % 3] == 9 else 0)
                r += 1 + (1 if v[(-r - 1) % 3] == 9 else 0) - gamma(t)
                lv.append(l)
                if (t + 1) % 120 == 0:
                    ls[(t + 1) // 120] = (l, r)
            ok = per == 120 and nines == {1}
            for j, (lj, rj) in ls.items():
                if lj > 150 * j + 2 or rj > 120 * j + 2:
                    ok = False
            # per epoch from every start phase: front restarted at 0 with the rotation that has phase 0 at the start
            e = 0
            for t0 in range(0, 120 * 3, 120):
                # at an epoch boundary the row is V itself; the front starts at any column, i.e. any rotation
                for sh in range(3):
                    l2 = 0
                    for t in range(t0, t0 + 120):
                        l2 += 1 + (1 if rows[t][(sh + l2) % 3] == 9 else 0)
                    e = max(e, l2)
            if e > 152:
                ok = False
            summary[(a, rot)] = (per, sorted(nines), ls[1], ls[2], ls[40], e, ok)
            if not ok:
                bad += 1
    for k, v in summary.items():
        print(k, v)
    print('CONES', 'PASS' if bad == 0 else f'FAIL {bad}', flush=True)


def pairword(n):
    d = [int(ch) for ch in str(n)[::-1]]
    L = len(d)
    return [d[i] + d[L - 1 - i] for i in range(L)]


def genuine(seed):
    rnd = random.Random(seed)
    B0 = [10, 4, 6, 6, 7, 12, 9, 16, 16, 13, 0, 2, 10, 17, 7, 0, 18, 6, 5, 18, 4, 18, 14, 9, 14, 8, 12, 17, 10, 4, 6, 4, 0, 5]
    W0 = [5, 18, 4, 8, 1, 15, 4, 0, 5]
    a = rnd.randrange(0, 19, 2)
    rot = rnd.randrange(3)
    V = rotation(a, rot)
    q = 20
    J = [rnd.randrange(19) for _ in range(rnd.randrange(3, 9))]
    while J[-1] == V[2]:
        J[-1] = rnd.randrange(19)
    H = B0 + W0 * q + J + V * 140
    half = [rnd.randrange(19) for _ in range(6)]
    C = half + half[::-1]
    P = H + C + H[::-1]
    L = len(P)
    d = [0] * L
    for i in range(L // 2):
        hi_, lo_ = (P[i] + 1) // 2, P[i] // 2
        d[i], d[L - 1 - i] = hi_, lo_
    if L % 2:
        assert P[L // 2] % 2 == 0
        d[L // 2] = P[L // 2] // 2
    assert d[L - 1] > 0
    n = int(''.join(str(x) for x in d[::-1]))
    assert pairword(n) == P
    return V, a, rot, q, J, n, len(H) - 3 * 140


def validate(seed, R=12):
    V, a, rot, q, J, n, yU = genuine(seed)
    y = yU
    rows, As, Bs = background(V)
    Ps, ALs, HLs = [], [], []
    gam = []
    for s in range(T + 1):
        P = pairword(n)
        Ps.append(P)
        if s == T:
            break
        # folded law: carries of the addition sum P_i 10^i
        L = len(P)
        c = [0] * (L + 1)
        e = [0] * L
        for i in range(L):
            t = P[i] + c[i]
            e[i] = t % 10
            c[i + 1] = 1 if t >= 10 else 0
        g = c[L]
        gam.append(g)
        al = c[y - R]
        hl = e[L - 1 - (y - R - 1)]
        ALs.append(al)
        HLs.append(hl)
        # check the law on every column of the window against the next pair word
        m = n + int(str(n)[::-1])
        Pn = pairword(m)
        assert len(Pn) == L + g
        for i in range(L // 2):
            lo = (P[i] + c[i]) % 10
            hi = e[L - 1 - i]
            if g:
                val = lo + 1 if i == 0 else lo + e[L - i]
            else:
                val = lo + hi
            assert val == Pn[i], (s, i)
        n = m
    clock_ok = all(gam[s] == gamma(s) for s in range(T))
    print(f'validate seed={seed}: a={a} rot={rot} V={V} q={q} |J|={len(J)} y={y} clock_std={clock_ok}', flush=True)
    assert clock_ok
    N = R + W
    # the band right of the window edge is background at every time
    for s in range(T + 1):
        for c in range(N, N + 12):
            assert Ps[s][y - R + c] == rows[s][(c - R) % 3], ('bg', s, c)
    x0 = {c: Ps[0][y - R + c] for c in range(R)}
    assert x0[R - 1] != V[2]
    fix = {'x0': x0, 'al0': ALs, 'hl': HLs}
    S, X, NN, nv = build(V, R, foreign=True, solver='cadical195', fix=fix, final=False)
    t0 = time.time()
    r = S.solve()
    print(f'  genuine data, no final condition: {"SAT" if r else "UNSAT"} ({time.time()-t0:.0f}s, {nv} vars)', flush=True)
    assert r
    model = set(l for l in S.get_model() if l > 0)
    S.delete()
    mism = 0
    for s in range(T + 1):
        for c in range(NN):
            vs = [v for v in range(19) if X[s][c] + v in model]
            if vs != [Ps[s][y - R + c]]:
                mism += 1
    print(f'  model letters vs genuine letters at all (t,c): {mism} mismatches', flush=True)
    assert mism == 0
    # determinism: forbid the genuine letter at one final column
    rnd = random.Random(seed + 1000)
    c0 = rnd.randrange(N)
    v0 = Ps[T][y - R + c0]
    S2, X2, _, _ = build(V, R, foreign=True, solver='cadical195', fix=fix, final=False, forbid=(c0, v0))
    r2 = S2.solve()
    S2.delete()
    print(f'  forbid genuine letter at final column {c0}: {"SAT" if r2 else "UNSAT"}', flush=True)
    assert not r2
    # the band is NOT restored in the genuine orbit: first band-correct column at t = 120
    st = R
    for c in range(NN - 1, R - 1, -1):
        if Ps[T][y - R + c] != rows[T][(c - R) % 3]:
            st = c + 1
            break
    print(f'  genuine band start moved right by {st - R} columns in one epoch', flush=True)
    print('VALIDATE PASS', flush=True)


def plain(a, rot, R, g, nofor, solver):
    V = rotation(a, rot)
    t0 = time.time()
    S, X, N, nv = build(V, R, g=g, foreign=not nofor, solver=solver)
    tb = time.time() - t0
    r = S.solve()
    ans = 'SAT' if r else 'UNSAT'
    extra = ''
    if r:
        m = set(l for l in S.get_model() if l > 0)
        f = [v for v in range(19) if X[0][R - 1] + v in m]
        extra = f' letter_y-1={f}'
    S.delete()
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024 ** 3
    print(f'RESULT a={a} rot={rot} V={V} R={R} g={g} nofor={int(nofor)} solver={solver}: {ans}{extra} vars={nv} build={tb:.0f}s total={time.time()-t0:.0f}s rss={rss:.1f}GB', flush=True)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('mode')
    ap.add_argument('args', nargs='*', type=int)
    ap.add_argument('--g', type=int, default=0)
    ap.add_argument('--nofor', action='store_true')
    ap.add_argument('--solver', default='kissat404')
    A = ap.parse_args()
    if A.mode == 'cones':
        cones()
    elif A.mode == 'validate':
        validate(A.args[0])
    elif A.mode == 'plain':
        plain(A.args[0], A.args[1], A.args[2], A.g, A.nofor, A.solver)

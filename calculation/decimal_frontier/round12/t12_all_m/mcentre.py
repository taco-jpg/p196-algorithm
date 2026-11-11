#!/usr/bin/env python3
"""r12f: direct centre SAT for the m-period return (T = 120m steps), folded frame WITH the middle column, cone-trimmed.

Configuration U^inf C rev(U)^inf (U phase 0 at y = first column of C), |C| = L, palindromic, odd middle even.
Folded columns: band (.., y), C half [y, y+h), middle y+h if L odd.  Region at time t: [y - r_t - DELTA, n_t) with
n_t = number of folded columns (incl. middle); left of the region = exact band background (cone lemma, centre-side
front r_t of the band ending at y-1, mdefect.fronts).  Middle coupling (exact, from beta_x = c_(L-x)):
  odd L (middle mc = n-1): beta_n = alpha_(n-1);  even L: beta_n = alpha_n;
  gamma=0: P'_i = lo_i + hi_i (middle: 2 lo);  gamma=1: P'_i = lo_i + hi_(i-1), and if L was even a new middle
  P'_n = 2 hi_(n-1) (L odd -> even: the old middle becomes a regular column).
Target: P_T = configuration shifted right by S = 15m (band for i < y+S, P_T(y+S+j) = P_0(y+j)).
A witness of length L covers every length L-6j (U^j C rev(U)^j), so lengths Lmax-5..Lmax cover all |C| <= Lmax.

Modes
  sat --U u --L L --m m          : free C (palindromic), RESULT SAT (with C) / UNSAT.
  validate --U u --L L --m m --seed s : genuine big-integer orbit with a random C: region rows == genuine,
          genuine C fixed + genuine final -> SAT, changed final -> UNSAT, return with genuine C -> SAT iff it returns,
          positive control: free C with target = genuine image -> SAT and the found C reproduces the image.
"""
import sys, time, argparse, random
sys.path.insert(0, __file__.rsplit('/', 1)[0])
import mdefect as md
from mdefect import G, Enc, carry, digit, psum, equal, val, band_bg, fronts, bgfun, us


def step_mid(E, t, row, a0, a1, n, p, bg):
    bgP, bga, bgb = bg
    g = G(t)
    P = lambda i: row[i] if a0 <= i < n else bgP(t, i)
    assert a1 <= a0
    al = {a1: bga(t, a1)}
    for i in range(a1, n):
        al[i + 1] = carry(E, P(i), al[i])
    be = {n: al[n - 1] if p else al[n]}
    for x in range(n - 1, a1 - 1, -1):
        be[x] = carry(E, P(x), be[x + 1])
    lo = {i: digit(E, P(i), al[i]) for i in range(a1, n)}
    hi = {j: digit(E, P(j), be[j + 1]) for j in range(a1 - 1, n)}
    new = {}
    if not g:
        for i in range(a1, n):
            new[i] = psum(E, lo[i], hi[i])
        return new, n, p
    for i in range(a1, n):
        new[i] = psum(E, lo[i], hi[i - 1])
    if p == 0:
        new[n] = psum(E, hi[n - 1], hi[n - 1])
        return new, n + 1, 1
    return new, n, 0


def build(E, U, L, T, y=30000, Cfix=None, delta=md.DELTA):
    rows, alb, beb = band_bg(U, T); l, r = fronts(U, T, rows)
    bg = bgfun(U, y, rows, alb, beb)
    h = L // 2; p = L % 2
    a = [y - r[t] - delta for t in range(T + 1)]
    row = {}
    for i in range(a[0], y):
        row[i] = U[(i - y) % 3]
    Cv = []
    for j in range(h + p):
        v = E.onehot(19); row[y + j] = v; Cv.append(v)
    if p:
        for x in range(1, 19, 2):
            E.add([-Cv[h][x]])
    if Cfix is not None:
        for j in range(h + p):
            E.add([Cv[j][Cfix[j]]])
    n = y + h + p
    P0 = dict(row); hist_n = [n]
    for t in range(T):
        row, n, p = step_mid(E, t, row, a[t], a[t + 1], n, p, bg)
        hist_n.append(n)
    return P0, row, n, p, Cv, a, hist_n


def target_shift(E, PT, P0, U, y, aT, nT, S):
    for i in range(aT, nT):
        equal(E, PT[i], U[(i - y) % 3] if i - S < y else P0[i - S])


def sat(a):
    from pysat.solvers import Solver
    U = us()[a.U]; T = 120 * a.m; S = 15 * a.m; t0 = time.time()
    Sv = Solver(name=a.solver); E = Enc(Sv); y = 30000
    P0, PT, nT, pT, Cv, aa, hn = build(E, U, a.L, T, y=y, delta=a.delta)
    assert nT == y + a.L // 2 + a.L % 2 + S and pT == a.L % 2
    target_shift(E, PT, P0, U, y, aa[T], nT, S)
    print(f'mcentre U={a.U} {U} L={a.L} m={a.m} T={T} shift={S} region_T=[y-{y-aa[T]}, y+{nT-y}) vars={E.nv} clauses={E.ncl} '
          f'solver={a.solver} enc={time.time()-t0:.0f}s', flush=True)
    r = Sv.solve()
    if r:
        m = set(x for x in Sv.get_model() if x > 0)
        half = [val(m, v) for v in Cv]
        C = half[:a.L // 2] + ([half[-1]] if a.L % 2 else []) + half[:a.L // 2][::-1]
        print('RESULT SAT C=', C, f'{time.time()-t0:.0f}s', flush=True)
    else:
        print('RESULT UNSAT', f'{time.time()-t0:.0f}s', flush=True)


def validate(a):
    from pysat.solvers import Solver
    rnd = random.Random(a.seed); U = us()[a.U]; T = 120 * a.m; S = 15 * a.m; L = a.L
    q = 10 * a.m + 6; K = 100 * a.m + 100; Lj = 7
    J = [rnd.randrange(19) for _ in range(Lj)]
    h = [rnd.randrange(19) for _ in range(L // 2 + L % 2)]
    if L % 2:
        h[-1] &= ~1
    C = h[:L // 2] + ([h[-1]] if L % 2 else []) + h[:L // 2][::-1]
    y = 34 + 9 * q + Lj + 3 * K
    word = md.make_word(U, J, C, q, K)
    orb = md.orbit(md.realize(word), T, y + L // 2 + L % 2 + S + 2)
    assert all(orb[t]['g'] == G(t) for t in range(T))
    rows_bg, alb, beb = band_bg(U, T); l, r = fronts(U, T, rows_bg)
    out = {'U': U, 'C': C, 'm': a.m}
    # (i) build with genuine C, no final constraint; compare every region row with the genuine orbit (needs history)
    Sv = Solver(name=a.solver); E = Enc(Sv)
    bg = bgfun(U, y, rows_bg, alb, beb)
    hh = L // 2; p = L % 2; aa = [y - r[t] - a.delta for t in range(T + 1)]
    row = {i: U[(i - y) % 3] for i in range(aa[0], y)}
    for j in range(hh + p):
        v = E.onehot(19); row[y + j] = v; E.add([v[h[j] if j < hh else h[-1]]])
    n = y + hh + p; hist = [(row, n)]
    for t in range(T):
        row, n, p = step_mid(E, t, row, aa[t], aa[t + 1], n, p, bg)
        hist.append((row, n))
    out['i_sat'] = Sv.solve()
    mm = set(x for x in Sv.get_model() if x > 0)
    bad = []
    for t in range(T + 1):
        rw, nn = hist[t]
        Lt = orb[t]['L']
        if nn - y != (Lt + 1) // 2 - y:
            bad.append(('ncols', t, nn - y, (Lt + 1) // 2 - y)); break
        for i in range(aa[t], nn):
            if val(mm, rw[i]) != orb[t]['P'][i]:
                bad.append((t, i - y, val(mm, rw[i]), orb[t]['P'][i])); break
        for i in range(aa[t] - 40, aa[t]):
            if orb[t]['P'][i] != rows_bg[t][(i - y) % 3]:
                bad.append(('left', t, i - y)); break
        if bad:
            break
    out['i_rows_match_genuine'] = not bad
    if bad:
        out['i_first_bad'] = bad[0]
    Sv.delete()
    nT = hist[T][1]
    Cfix = h
    for test in ('ii', 'iii', 'iv', 'v'):
        Sv = Solver(name=a.solver); E = Enc(Sv)
        P0, PT, nT2, pT, Cv, aa2, hn = build(E, U, L, T, y=y, Cfix=(Cfix if test != 'v' else None), delta=a.delta)
        assert nT2 == nT
        if test in ('ii', 'v'):
            for i in range(aa2[T], nT):
                equal(E, PT[i], orb[T]['P'][i])
        elif test == 'iii':
            j = rnd.randrange(aa2[T], nT); w = (orb[T]['P'][j] + 1 + rnd.randrange(17)) % 19
            for i in range(aa2[T], nT):
                equal(E, PT[i], w if i == j else orb[T]['P'][i])
            out['iii_col'] = (j - y, orb[T]['P'][j], w)
        else:
            target_shift(E, PT, P0, U, y, aa2[T], nT, S)
        res = Sv.solve(); out[test] = res
        if test == 'v' and res:
            m = set(x for x in Sv.get_model() if x > 0)
            out['v_found_half'] = [val(m, v) for v in Cv]
        Sv.delete()
    out['genuine_returns'] = all(orb[T]['P'][i] == (U[(i - y) % 3] if i - S < y else orb[0]['P'][i - S]) for i in range(aa[T], nT))
    out['PASS'] = (out['i_sat'] and out['i_rows_match_genuine'] and out['ii'] and not out['iii'] and
                   out['iv'] == out['genuine_returns'] and out['v'])
    print(out, flush=True)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('mode')
    ap.add_argument('--U', type=int, default=0)
    ap.add_argument('--L', type=int, default=6)
    ap.add_argument('--m', type=int, default=2)
    ap.add_argument('--seed', type=int, default=1)
    ap.add_argument('--delta', type=int, default=md.DELTA)
    ap.add_argument('--solver', default='cadical195')
    a = ap.parse_args()
    {'sat': sat, 'validate': validate}[a.mode](a)

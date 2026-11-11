#!/usr/bin/env python3
"""r12f3 (exploratory): TRAVELLING-JUNCTION instance TW(U, m, a, LJ), standard clock, T = 120m.
Coordinates: y = 34 + 9q (q = 60, so W0 has phase 0 at y), free junction J on [y, y+LJ), V = U-word with phase 0 at
yU = y + LJ.  Left of y: exact reference W rows W_t (columns (x-34) mod 9), kept constant left of the region by the
W cone; right of the band front: exact U background (cones as in mdefect).  Target at t = T:
  columns < y + 9a: reference W_T (= W_0 since 12 | T);  columns [y+9a, y+9a+LJ): the initial J letters;
  columns >= y+9a+LJ: the U band (phase (i - yU) mod 3, the same phase since 3 | 9a).
SAT would mean: a junction J translating right by 9a columns per 120m steps with W0 filling behind (candidate cycle
P(q,k) -> P(q+a, k+5m-3a), still to be combined with a centre).  a = 0 is the frozen junction (expected UNSAT by
Theorem A).  Modes: search (default), --nofinal (drop the target: SAT control), --validate (genuine big-integer orbit
of B0 W0^60 J V^K C rev(.): J random, target = genuine row at t = T: SAT; one changed column: UNSAT).
"""
import sys, time, argparse, random
sys.path.insert(0, __file__.rsplit('/', 1)[0])
import mdefect as md
import wadvance as wa

DELTA = 3
MARGIN = 5
Q = 60


def setup(V, T, LJ):
    y = 34 + 9 * Q
    yU = y + LJ
    rowsW, alW, beW = wa.wbg(T)
    f = wa.wfront(T, 0, rowsW)                       # W cone from the foreign side at column y (phase 0)
    A = y - max(f) - MARGIN
    assert A >= 34 + 18, 'W window too close to the root'
    rowsU, alb, beb = md.band_bg(V, T)
    l, r = md.fronts(V, T, rowsU)
    b = [yU + l[t] + DELTA for t in range(T + 1)]

    def bgP(t, i):
        return rowsW[t][(i - 34) % 9] if i < A else rowsU[t][(i - yU) % 3]

    def bga(t, i):
        return alW[t][(i - 34) % 9]

    def bgb(t, x):
        return beb[t][(x - yU) % 3]
    return y, yU, A, b, (bgP, bga, bgb), rowsW, rowsU, l


def build(E, V, T, a, LJ, fixJ=None, target=None, final=True):
    y, yU, A, b, bg, rowsW, rowsU, l = setup(V, T, LJ)
    row = {}
    for i in range(A, b[0]):
        if i < y:
            row[i] = rowsW[0][(i - 34) % 9]
        elif i < yU:
            row[i] = E.onehot(19)
            if fixJ is not None:
                E.add([row[i][fixJ[i - y]]])
        else:
            row[i] = V[(i - yU) % 3]
    P0 = dict(row)
    for t in range(T):
        row, port = md.step(E, t, row, A, b[t], A, b[t + 1], bg, 'exact', 'exact')
    if final:
        for i in range(A, b[T]):
            if target is not None:
                md.equal(E, row[i], target[i])
            elif i < y + 9 * a:
                md.equal(E, row[i], rowsW[T][(i - 34) % 9])
            elif i < y + 9 * a + LJ:
                md.equal(E, row[i], P0[i - 9 * a])
            else:
                md.equal(E, row[i], V[(i - yU) % 3])
    return P0, row, (y, yU, A, b)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--U', type=int, default=0)
    ap.add_argument('--m', type=int, default=1)
    ap.add_argument('--a', type=int, default=1)
    ap.add_argument('--LJ', type=int, default=30)
    ap.add_argument('--solver', default='kissat404')
    ap.add_argument('--nofinal', action='store_true')
    ap.add_argument('--validate', action='store_true')
    ap.add_argument('--seed', type=int, default=1)
    a = ap.parse_args()
    from pysat.solvers import Solver
    V = md.us()[a.U]; T = 120 * a.m; t0 = time.time()
    if a.validate:
        rnd = random.Random(a.seed)
        J = [rnd.randrange(19) for _ in range(a.LJ)]
        h = [rnd.randrange(19) for _ in range(3)]; C = h + h[::-1]
        y, yU, A, b, bg, rowsW, rowsU, l = setup(V, T, a.LJ)
        K = 100 * a.m + 120
        orb = md.orbit(md.realize(md.make_word(V, J, C, Q, K)), T, b[T] + 10)
        assert all(orb[t]['g'] == (t % 4 == 0) for t in range(T)), 'clock'
        target = {i: orb[T]['P'][i] for i in range(A, b[T])}
        res = {}
        for test in ('genuine', 'changed'):
            S = Solver(name=a.solver); E = md.Enc(S)
            tg = dict(target)
            if test == 'changed':
                j = rnd.randrange(A, b[T]); tg[j] = (tg[j] + 1 + rnd.randrange(17)) % 19
            build(E, V, T, a.a, a.LJ, fixJ=J, target=tg)
            res[test] = S.solve(); S.delete()
        print('validate', 'U', a.U, 'm', a.m, 'LJ', a.LJ, 'seed', a.seed, res, 'PASS' if res['genuine'] and not res['changed'] else 'FAIL', flush=True)
        return
    S = Solver(name=a.solver); E = md.Enc(S)
    P0, row, (y, yU, A, b) = build(E, V, T, a.a, a.LJ, final=not a.nofinal)
    print(f'twjunction U={a.U} V={V} m={a.m} T={T} a={a.a} LJ={a.LJ} nofinal={a.nofinal} A=y-{y-A} b_T=yU+{b[T]-yU} vars={E.nv} clauses={E.ncl} '
          f'solver={a.solver} enc={time.time()-t0:.0f}s', flush=True)
    r = S.solve()
    if r:
        m = set(x for x in S.get_model() if x > 0)
        J = [md.val(m, P0[i]) for i in range(y, yU)]
        print('SAT J =', J, flush=True)
    print('RESULT', 'TW=[sat]' if r else 'TW=[]', 'NONEMPTY' if r else 'EMPTY', f'{time.time()-t0:.0f}s', flush=True)


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""r12f3: quantitative band erosion: instance B_1^+(V,R,g) = brestore.py group mode (mdefect encoding, one epoch T = 120,
standard clock), final condition weakened to "columns [y+g, inf) are again V^inf at t = 120".
Group form as in brestore.py (free [y-R,y) with (P_(y-3),P_(y-2),P_(y-1)) != (V0,V1,V2), V^inf on [y,inf), free left port
at y-R, exact right port).  UNSAT(g) => for the three rotations of the a of V, in every standard-clock epoch the
maximal band start advances by at least g+1 columns (y_(j+1) >= y_j + g + 1).  g = 0 is brestore.py group (= B_1).
Options: --nofor (drop the triple constraint, SAT control)."""
import sys, time, argparse
sys.path.insert(0, __file__.rsplit('/', 1)[0])
import mdefect as md


def build(E, V, R, g, y, delta):
    T = 120
    rows, alb, beb = md.band_bg(V, T); l, r = md.fronts(V, T, rows)
    assert tuple(rows[T]) == tuple(V)
    a = y - R; b = [y + l[t] + delta for t in range(T + 1)]
    bg = md.bgfun(V, y, rows, alb, beb)
    row = {i: (E.onehot(19) if i < y else V[(i - y) % 3]) for i in range(a, b[0])}
    P0 = dict(row)
    for t in range(T):
        row, port = md.step(E, t, row, a, b[t], a, b[t + 1], bg, 'free', 'exact')
    for i in range(y + g, b[T]):
        md.equal(E, row[i], V[(i - y) % 3])
    return P0, b, l


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--U', type=int, default=2)
    ap.add_argument('--r', type=int, default=3)
    ap.add_argument('--g', type=int, default=0)
    ap.add_argument('--delta', type=int, default=md.DELTA)
    ap.add_argument('--nofor', action='store_true')
    ap.add_argument('--solver', default='kissat404')
    a = ap.parse_args()
    from pysat.solvers import Solver
    V = md.us()[a.U]; R = a.r; y = 3000; t0 = time.time()
    S = Solver(name=a.solver); E = md.Enc(S)
    P0, b, l = build(E, V, R, a.g, y, a.delta)
    if not a.nofor:
        E.add([-P0[y - 3 + j][V[j]] for j in range(3)])
    print(f'brestg group U={a.U} V={V} R={R} g={a.g} nofor={a.nofor} l_T={l[120]} final window [y+{a.g}, y+{b[120]-y}) vars={E.nv} '
          f'clauses={E.ncl} solver={a.solver} enc={time.time()-t0:.0f}s', flush=True)
    res = S.solve()
    if res:
        m = set(x for x in S.get_model() if x > 0)
        print('SAT free columns', [md.val(m, P0[i]) for i in range(y - R, y)], flush=True)
    print('RESULT', 'Bg=[sat]' if res else 'Bg=[]', 'NONEMPTY' if res else 'EMPTY', f'{time.time()-t0:.0f}s', flush=True)


if __name__ == '__main__':
    main()

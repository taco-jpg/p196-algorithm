#!/usr/bin/env python3
"""r12f2: band-restoration instances B_n(V,R) for the all-m "maximal band start" argument (see NOTES r12f2, FINAL).

Same exact folded two-carry encoding as mdefect.py (imports its build blocks: cone-trimmed seam region, FREE left
port at y-R, exact background right of the junction-side front + DELTA, forced clock gamma_t=[t%4==0]).

B_n(V,R): columns [y-R,y-1) free, column y-1 = v != V[2], columns [y,inf) = V^inf at t=0 (V phase 0 at y); free left
port at y-R; NO return constraint on [y-R,y); constraint: at every epoch boundary t = 120e, e = 1..n, the columns
[y,inf) are again V^inf (U rows are 120-periodic, so the band background at t = 120e is V itself).

Modes
  defect --U u --r R --n n : enumerate the set B_n(V,R) of letters v (blocking clauses).
  group  --U u --r R --n n : free [y-R,y) with (P_(y-3),P_(y-2),P_(y-1)) != (V0,V1,V2); UNSAT => B_n(V,R) =
          B_n(V'',R-1) = B_n(V',R-2) = empty (V' = (V1,V2,V0) phase 0 at y-2, V'' = (V2,V0,V1) phase 0 at y-1).
  --full : additionally every column of [y-R,y) returns at t = 120n (then defect = D_R^(n)(V), group = uleft^(n);
           consistency check against mdefect.py / r12a).
  --nofor: drop the foreign-letter / triple constraint (positive control: the pure band is a solution, SAT).
"""
import sys, time, argparse
sys.path.insert(0, __file__.rsplit('/', 1)[0])
import mdefect as md


def build(E, V, R, n, y, delta, full):
    T = 120 * n
    rows, alb, beb = md.band_bg(V, T); l, r = md.fronts(V, T, rows)
    assert all(tuple(rows[120 * e]) == tuple(V) for e in range(n + 1)), 'band rows not 120-periodic'
    a = y - R; b = [y + l[t] + delta for t in range(T + 1)]
    bg = md.bgfun(V, y, rows, alb, beb)
    row = {}
    for i in range(a, b[0]):
        row[i] = E.onehot(19) if i < y else V[(i - y) % 3]
    P0 = dict(row); snaps = {0: row}
    for t in range(T):
        row, port = md.step(E, t, row, a, b[t], a, b[t + 1], bg, 'free', 'exact')
        if (t + 1) % 120 == 0:
            snaps[t + 1] = row
    for e in range(1, n + 1):
        tt = 120 * e
        for i in range(y, b[tt]):
            md.equal(E, snaps[tt][i], V[(i - y) % 3])
    if full:
        for i in range(a, y):
            md.equal(E, snaps[T][i], P0[i])
    return P0, snaps, b, l


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('mode', choices=['defect', 'group'])
    ap.add_argument('--U', type=int, default=0)
    ap.add_argument('--r', type=int, default=12)
    ap.add_argument('--n', type=int, default=1)
    ap.add_argument('--delta', type=int, default=md.DELTA)
    ap.add_argument('--full', action='store_true')
    ap.add_argument('--nofor', action='store_true')
    ap.add_argument('--solver', default='kissat404')
    a = ap.parse_args()
    from pysat.solvers import Solver
    V = md.us()[a.U]; R = a.r; y = 3000; t0 = time.time()
    assert a.mode == 'defect' or R >= 3

    def inst(blocked):
        S = Solver(name=a.solver); E = md.Enc(S)
        P0, snaps, b, l = build(E, V, R, a.n, y, a.delta, a.full)
        if not a.nofor:
            if a.mode == 'defect':
                E.add([-P0[y - 1][V[2]]])
            else:
                E.add([-P0[y - 3 + j][V[j]] for j in range(3)])
        for v in blocked:
            E.add([-P0[y - 1][v]])
        return S, E, P0, b, l

    S, E, P0, b, l = inst([])
    print(f'brestore {a.mode} U={a.U} V={V} R={R} n={a.n} T={120*a.n} full={a.full} nofor={a.nofor} front l_T={l[120*a.n]} '
          f'delta={a.delta} vars={E.nv} clauses={E.ncl} solver={a.solver} enc={time.time()-t0:.0f}s', flush=True)
    found = []
    while True:
        res = S.solve()
        if not res:
            break
        m = set(x for x in S.get_model() if x > 0)
        cols = [md.val(m, P0[i]) for i in range(y - R, y)]
        print('SAT free columns', cols, f'{time.time()-t0:.0f}s', flush=True)
        if a.mode == 'group' or a.nofor:
            found.append('sat'); break
        found.append(cols[-1]); S.delete()
        S, E, P0, b, l = inst(found)
    S.delete()
    tag = 'B' if not a.full else ('D' if a.mode == 'defect' else 'Ufull')
    print('RESULT', f'{tag}=' + str(sorted(found, key=str)), 'EMPTY' if not found else 'NONEMPTY', f'{time.time()-t0:.0f}s', flush=True)


if __name__ == '__main__':
    main()

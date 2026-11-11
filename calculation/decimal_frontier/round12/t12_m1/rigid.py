#!/usr/bin/env python3
"""r12a rigidity SAT: can a returning configuration end (or start) a bulk band
anywhere other than by continuing the band?

Exact folded two-carry encoding over 120 steps (same law as seamsat.py), but with
FREE carry ports on the open side, which over-approximates every possible context.

Uleft  --U i --r R : window [y-R, y+M).  Columns [y, y+M) = U^(M/3) (U phase 0 at y),
         columns [y-R, y) free in 0..18.  Left port at cut y-R is FREE: alpha_(y-R)(t)
         free bits, and at overflow steps the shifted high digit hi_(y-R-1)(t) free 0..9.
         Right port: beta at y+M = U background (M=171 > 152 junction cone).
         Every column of the window must return (P_120 = P_0).
         Constraint: (P_(y-3),P_(y-2),P_(y-1)) != U.   UNSAT => "U is left-rigid at depth R":
         in ANY returning configuration that equals U^inf from y on, the period
         before y is U as well.
Wright --j j --r R : rooted window [64, y+R) with y = 160+j (W phase j at y).  Left side
         exact rooted rows (as seamsat.py); columns [64,y) = B0 W0^14 ..., columns [y,y+R)
         free; right port beta_(y+R)(t) FREE.  All columns return.
         Constraint: P_y != W_j.   UNSAT => "W is right-rigid at depth R at phase j".
--noconstraint drops the rigidity constraint (positive control: must be SAT).
"""
import sys, time, argparse
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from seamsat import cone_rows, alpha_at, beta_at
from seam_check import B, W, J0, us


class Enc:
    def __init__(s, solver):
        s.S = solver; s.nv = 0; s.ncl = 0

    def add(s, c):
        s.S.add_clause(c); s.ncl += 1

    def new(s, k=1):
        r = list(range(s.nv + 1, s.nv + 1 + k)); s.nv += k; return r

    def one(s, vs):
        s.add(list(vs))
        for i in range(len(vs)):
            for j in range(i + 1, len(vs)):
                s.add([-vs[i], -vs[j]])

    def fix(s, var, b):
        s.add([var] if b else [-var])


def encode(E, x0, x1, init, left, right, steps=120):
    """left: None (free port) or rows (exact rooted rows: alpha_x0 and P_(x0-1) known).
    right: None (free beta at x1) or list of 120 bits.
    Returns P0 (initial one-hot), P (final one-hot), dict of port vars."""
    def onehots():
        r = {}
        for i in range(x0, x1):
            v = E.new(19); E.one(v); r[i] = v
        return r
    P = onehots(); P0 = P
    for i, v in init.items():
        E.fix(P[i][v], 1)
    ports = {'al0': [], 'hl': [], 'be1': []}
    for t in range(steps):
        g = (t % 4 == 0)
        al = E.new(x1 - x0 + 1); be = E.new(x1 - x0 + 1)
        if left is not None:
            E.fix(al[0], alpha_at(left[t], x0))
        ports['al0'].append(al[0])
        if right is not None:
            E.fix(be[-1], right[t])
        ports['be1'].append(be[-1])
        lo = {}; hi = {}
        for i in range(x0, x1):
            k = i - x0
            lo[i] = E.new(10); E.one(lo[i]); hi[i] = E.new(10); E.one(hi[i])
            for x in range(19):
                for b in (0, 1):
                    z = x + b
                    h = [-P[i][x], (-al[k] if b else al[k])]
                    E.add(h + [lo[i][z % 10]]); E.add(h + [al[k + 1] if z >= 10 else -al[k + 1]])
                    h = [-P[i][x], (-be[k + 1] if b else be[k + 1])]
                    E.add(h + [hi[i][z % 10]]); E.add(h + [be[k] if z >= 10 else -be[k]])
        Pn = onehots()
        hl = None
        if g:
            hl = E.new(10); E.one(hl)
            if left is not None:
                px = left[t][x0 - 1]
                for b in (0, 1):
                    E.add([(-be[0] if b else be[0]), hl[(px + b) % 10]])
            ports['hl'].append(hl)
        for i in range(x0, x1):
            H = (hi[i - 1] if i > x0 else hl) if g else hi[i]
            for a in range(10):
                for b in range(10):
                    E.add([-lo[i][a], -H[b], Pn[i][a + b]])
        P = Pn
    return P0, P, ports


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('mode')
    ap.add_argument('--U', type=int, default=0)
    ap.add_argument('--j', type=int, default=0)
    ap.add_argument('--r', type=int, default=6)
    ap.add_argument('--M', type=int, default=171)
    ap.add_argument('--noconstraint', action='store_true')
    ap.add_argument('--solver', default='cadical195')
    a = ap.parse_args()
    from pysat.solvers import Solver
    S = Solver(name=a.solver); E = Enc(S); t0 = time.time()
    if a.mode == 'Uleft':
        U = us()[a.U]; R = a.r; M = a.M - a.M % 3
        y = 1000; x0 = y - R; x1 = y + M
        # U background beta at x1 (period-3 rows, U phase 0 at y)
        rows = cone_rows(list(B) + list(W) * 14 + list(U) * 400)  # long pure U band after J0=160
        # column c of this prefix with c>=160 has U phase (c-160)%3; pick cb = x1 - y + 160 + 3*60
        cb = 160 + 3 * 60 + M
        right = [beta_at(rows[t], cb) for t in range(120)]
        init = {i: U[(i - y) % 3] for i in range(y, x1)}
        P0, P, ports = encode(E, x0, x1, init, None, right)
        for i in range(x0, x1):
            for v in range(19):
                E.add([-P0[i][v], P[i][v]])
        if not a.noconstraint:
            E.add([-P0[y - 3 + j][U[j]] for j in range(3)])
        print(f'Uleft U={U} R={R} M={M} vars={E.nv} clauses={E.ncl} enc={time.time()-t0:.0f}s', flush=True)
    elif a.mode == 'Wright':
        R = a.r; j = a.j; y = J0 + j; x0 = 64; x1 = y + R
        rows = cone_rows(list(B) + list(W) * 40)
        init = {i: rows[0][i] for i in range(x0, y)}
        P0, P, ports = encode(E, x0, x1, init, rows, None)
        for i in range(x0, x1):
            for v in range(19):
                E.add([-P0[i][v], P[i][v]])
        if not a.noconstraint:
            E.add([-P0[y][W[j % 9]]])
        print(f'Wright j={j} R={R} vars={E.nv} clauses={E.ncl} enc={time.time()-t0:.0f}s', flush=True)
    else:
        raise SystemExit('mode?')
    r = S.solve()
    print('RESULT', 'SAT' if r else 'UNSAT', f'{time.time()-t0:.0f}s', flush=True)
    if r:
        m = set(l for l in S.get_model() if l > 0)
        val = lambda vs: next(v for v in range(len(vs)) if vs[v] in m)
        if a.mode == 'Uleft':
            print('free columns', [val(P0[i]) for i in range(x0, y)], flush=True)
        else:
            print('free columns', [val(P0[i]) for i in range(y, x1)], flush=True)
        print('port al0', ''.join(str(int(v in m)) for v in ports['al0']), flush=True)
        print('port be1', ''.join(str(int(v in m)) for v in ports['be1']), flush=True)
        print('port hl', [val(h) for h in ports['hl']], flush=True)


if __name__ == '__main__':
    main()

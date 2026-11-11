#!/usr/bin/env python3
"""r12f3: "W-end advance" instance M(z,R): mirror of the band-restoration instance B_1, for the RIGHT end of the
reference-correct exterior prefix (exact folded law, forced STANDARD clock, T steps, default T = 120).

Reference word: Ref = B0 W0^inf (epoch boundaries t = 0 mod 12 carry exactly this row; W rows are 12-periodic).
M: at t = 0 the columns [left, z) carry Ref, column z carries a letter != Ref[z] ("foreign"), columns (z, z+R) are
free (R >= 1), the inlet beta_(z+R)(t) is FREE at every step (it summarises everything to the right).  Condition: at
t = T the columns [left, z] carry Ref again (the reference-correct prefix has grown by at least one column).
UNSAT => in a standard-clock orbit the length z_j of the prefix agreeing with Ref at the epoch boundaries t = 120j
cannot increase from one epoch to the next, whatever the columns to the right do.
Used for cycles P(q,k) -> P(q',k') with q' > q (the template prefix would have to advance from J0(q) to J0(q')).
Two sub-families:
 deep --phi f  (f = (z-34) mod 9): z deep in the W band; rectangle [z-L, z+R); LEFT side exact (reference rows
               W_t, periodic low carry entering column z-L, overflow-step high digit from the reference letter at
               z-L-1 and the computed beta); valid for z >= 35+L+9 since the two-inlet cone cannot reach z-L.
 root --z z    (0 <= z < 35+L+9): region [0, z+R) including the root rule (alpha_0 = 0, overflow: P'_0 = lo_0+1).
The clock is FORCED standard (the overflow computed from the window is not compared with it: a relaxation, sound for
UNSAT; in a genuine standard-clock orbit the computed overflow equals the forced one).
--nofor: drop the foreign-letter constraint (positive control: SAT, the reference itself).
"""
import sys, time, argparse
sys.path.insert(0, __file__.rsplit('/', 1)[0])
import mdefect as md

L_DEFAULT = 130


def wbg(T):
    """9-periodic reference rows W_t and periodic carries (al[t][j] entering column of phase j, be[t][j] = beta_x for
    x of phase j, i.e. carry passed from column x to column x-1), standard clock."""
    n = 9; rows = [tuple(md.W0)]; al = []; be = []
    for t in range(T):
        w = rows[-1]; a = [0] * n; b = [0] * n; c = 0
        for _ in range(3):
            for j in range(n):
                a[j] = c; c = md.Tc(w[j], c)
        c = 0
        for _ in range(3):
            for j in range(n - 1, -1, -1):
                c = md.Tc(w[j], c); b[j] = c
        lo = [(w[j] + a[j]) % 10 for j in range(n)]
        hi = [(w[j] + b[(j + 1) % n]) % 10 for j in range(n)]
        rows.append(tuple(lo[j] + (hi[(j - 1) % n] if md.G(t) else hi[j]) for j in range(n)))
        al.append(a); be.append(b)
    if T >= 12:
        assert rows[12] == rows[0], 'W rows not 12-periodic'
    return rows, al, be


def wfront(T, phi, rows):
    """exact two-sided retreat of the protected prefix end from z (phase phi of z, the first foreign column):
    f_(t+1) = f_t + 1 + [edge letter = 9] - gamma_t, edge column z-1-f_t."""
    f = 0; out = [0]
    for t in range(T):
        edge = (phi - 1 - f) % 9
        f += 1 + (1 if rows[t][edge] == 9 else 0) - md.G(t)
        out.append(f)
    return out


def ref(i):
    return md.B0[i] if i < 34 else md.W0[(i - 34) % 9]


def build_root(E, z, R, T, nofor):
    b = z + R
    row = {i: (ref(i) if i < z else E.onehot(19)) for i in range(b)}
    if not nofor:
        E.add([-row[z][ref(z)]])
    P0 = dict(row)
    for t in range(T):
        g = md.G(t)
        al = {0: 0}
        for i in range(b - 1):
            al[i + 1] = md.carry(E, row[i], al[i])
        bv = (E.new(),)
        be = {b: bv}
        for i in range(b - 1, 0, -1):
            be[i] = md.carry(E, row[i], be[i + 1])
        hi = {i: md.digit(E, row[i], be[i + 1]) for i in range(b)}
        new = {}
        for i in range(b):
            lo = md.digit(E, row[i], al[i])
            if g == 0:
                new[i] = md.psum(E, lo, hi[i])
            else:
                new[i] = md.psum(E, lo, 1 if i == 0 else hi[i - 1])
        row = new
    for i in range(z + 1):
        md.equal(E, row[i], ref(i))
    return P0, row


def build_deep(E, phi, L, R, T, nofor):
    rows, al_bg, be_bg = wbg(T)
    f = wfront(T, phi, rows)
    assert max(f) + 5 <= L, f'L = {L} too small for the front {max(f)}'
    z = 34 + 9 * 50 + phi; a = z - L; b = z + R
    P = lambda t, i: rows[t][(i - 34) % 9]
    row = {i: (P(0, i) if i < z else E.onehot(19)) for i in range(a, b)}
    if not nofor:
        E.add([-row[z][P(0, z)]])
    P0 = dict(row)
    for t in range(T):
        g = md.G(t)
        al = {a: al_bg[t][(a - 34) % 9]}
        for i in range(a, b - 1):
            al[i + 1] = md.carry(E, row[i], al[i])
        bv = (E.new(),)
        be = {b: bv}
        for x in range(b - 1, a - 1, -1):
            be[x] = md.carry(E, row[x], be[x + 1])
        hi = {i: md.digit(E, row[i], be[i + 1]) for i in range(a, b)}
        if g:
            hi[a - 1] = md.digit(E, P(t, a - 1), be[a])
        new = {}
        for i in range(a, b):
            lo = md.digit(E, row[i], al[i])
            new[i] = md.psum(E, lo, hi[i] if not g else hi[i - 1])
        row = new
    for i in range(a, z + 1):
        md.equal(E, row[i], P(T, i))
    return P0, row, max(f)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('mode', choices=['deep', 'root'])
    ap.add_argument('--phi', type=int, default=0)
    ap.add_argument('--z', type=int, default=0)
    ap.add_argument('--R', type=int, default=1)
    ap.add_argument('--T', type=int, default=120)
    ap.add_argument('--L', type=int, default=L_DEFAULT)
    ap.add_argument('--nofor', action='store_true')
    ap.add_argument('--solver', default='kissat404')
    a = ap.parse_args()
    from pysat.solvers import Solver
    t0 = time.time()
    S = Solver(name=a.solver); E = md.Enc(S)
    if a.mode == 'deep':
        P0, row, fmax = build_deep(E, a.phi, a.L, a.R, a.T, a.nofor)
        print(f'wadvance deep phi={a.phi} R={a.R} T={a.T} L={a.L} frontmax={fmax} nofor={a.nofor} vars={E.nv} clauses={E.ncl} '
              f'solver={a.solver} enc={time.time()-t0:.0f}s', flush=True)
    else:
        P0, row = build_root(E, a.z, a.R, a.T, a.nofor)
        print(f'wadvance root z={a.z} R={a.R} T={a.T} nofor={a.nofor} vars={E.nv} clauses={E.ncl} solver={a.solver} '
              f'enc={time.time()-t0:.0f}s', flush=True)
    r = S.solve()
    if r:
        m = set(x for x in S.get_model() if x > 0)
        keys = sorted(k for k, v in P0.items() if not isinstance(v, int))
        print('SAT free columns (t=0):', [(k, md.val(m, P0[k])) for k in keys], flush=True)
    print('RESULT', 'M=[sat]' if r else 'M=[]', 'NONEMPTY' if r else 'EMPTY', f'{time.time()-t0:.0f}s', flush=True)


if __name__ == '__main__':
    main()

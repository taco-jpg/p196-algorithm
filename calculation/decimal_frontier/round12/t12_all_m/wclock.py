#!/usr/bin/env python3
"""r12f2: CLOCK RIGIDITY of the returning rooted exterior (closes the small-q gap if UNSAT).

In any m-return Phi^(120m)(P(q,k)) = P(q,k+5m) the columns [0, J0) (J0 = 34+9q) carry B0 W0^q at t = 0 and again at
t = 120m, and their evolution depends on the rest of the number only through the high carry beta_(J0)(t) entering
column J0-1 (low carries start at the root, alpha_0 = 0; the overflow-step coupling hi_(i-1) is internal).
Instance W_m(q): window [0,J0), t = 0: B0 W0^q; inlet beta_(J0)(t) FREE for every t; the clock is COMPUTED from the
window: gamma_t = beta_0(t) = [P_0 + beta_1 >= 10]; exact folded law incl. the root rule (gamma=0: P'_0 = lo_0+hi_0,
P'_i = lo_i+hi_i; gamma=1: P'_0 = lo_0+1, P'_i = lo_i+hi_(i-1)); t = 120m: the window equals B0 W0^q again;
exactly 30m overflows in 120m steps (digit count of P(q,k+5m) minus P(q,k)); and gamma_t != [t%4==0] for SOME t.
UNSAT  =>  every m-return with this q has the standard clock (1000)^(30m) for all t < 120m.
Modes: rigid (the instance above); nodev (drop the deviation clause: positive control, SAT expected);
validate (genuine big-integer orbit of a T12 template: genuine inlet fixed -> genuine rows/clock reproduced, changed
final UNSAT).  Encoding helpers from mdefect.py (one-hot values/digits, carry bits, constant folding).
"""
import sys, time, argparse, random
sys.path.insert(0, __file__.rsplit('/', 1)[0])
import mdefect as md


def mux(E, g, h0, h1):
    """g: int 0/1 or 1-tuple var; h0 if g = 0 else h1 (digits: int or onehot10)."""
    if isinstance(g, int):
        return h1 if g else h0
    if isinstance(h0, int) and isinstance(h1, int) and h0 == h1:
        return h0
    hs = E.onehot(10)
    for d in range(10):
        for sign, h in ((1, h0), (-1, h1)):
            if isinstance(h, int):
                if h == d:
                    E.add([sign * g[0], hs[d]])
            else:
                E.add([sign * g[0], -h[d], hs[d]])
    return hs


def build(E, q, T, port=None, init=None):
    x1 = 34 + 9 * q
    row = {i: (md.B0[i] if i < 34 else md.W0[(i - 34) % 9]) for i in range(x1)} if init is None else dict(enumerate(init))
    P0 = dict(row); gams = []; rows = [row]
    for t in range(T):
        al = {0: 0}
        for i in range(x1 - 1):
            al[i + 1] = md.carry(E, row[i], al[i])
        bv = (E.new(),)
        if port is not None:
            E.add([md.lit(bv, port[t])])
        be = {x1: bv}
        for i in range(x1 - 1, -1, -1):
            be[i] = md.carry(E, row[i], be[i + 1])
        g = be[0]; gams.append(g)
        hi = {i: md.digit(E, row[i], be[i + 1]) for i in range(x1)}
        new = {}
        for i in range(x1):
            lo = md.digit(E, row[i], al[i])
            new[i] = md.psum(E, lo, mux(E, g, hi[i], 1 if i == 0 else hi[i - 1]))
        row = new; rows.append(row)
    return P0, rows, gams


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('mode', choices=['rigid', 'nodev', 'validate', 'refcheck'])
    ap.add_argument('--q', type=int, default=14)
    ap.add_argument('--m', type=int, default=2)
    ap.add_argument('--nocount', action='store_true')
    ap.add_argument('--seed', type=int, default=1)
    ap.add_argument('--perturb', type=int, default=0, help='validate: change this many random coefficients of the window (non-standard clocks)')
    ap.add_argument('--solver', default='kissat404')
    a = ap.parse_args()
    from pysat.solvers import Solver
    T = 120 * a.m; t0 = time.time(); x1 = 34 + 9 * a.q
    if a.mode == 'validate':
        rnd = random.Random(a.seed)
        U = md.us()[rnd.randrange(30)]; J = [rnd.randrange(19) for _ in range(rnd.randrange(1, 20))]
        h = [rnd.randrange(19) for _ in range(3)]; C = h + h[::-1]
        K = 120 * a.m + 50
        word = md.make_word(U, J, C, a.q, K); n = len(word)
        for _ in range(a.perturb):                     # symmetric change of one pair coefficient inside [1, x1)
            i = rnd.randrange(1, x1); word[i] = word[n - 1 - i] = rnd.randrange(19)
        init = word[:x1]
        orb = md.orbit(md.realize(word), T, x1 + 5)
        port = [orb[t]['c'][orb[t]['L'] - x1] for t in range(T)]
        gclock = [orb[t]['g'] for t in range(T)]
        out = {'q': a.q, 'm': a.m, 'U': U, 'J': J, 'nonstandard_steps': sum(gclock[t] != (t % 4 == 0) for t in range(T)),
               'genuine_window_returns': all(orb[T]['P'][i] == orb[0]['P'][i] for i in range(x1))}
        for test in ('ii', 'iii'):
            S = Solver(name=a.solver); E = md.Enc(S)
            P0, rows, gams = build(E, a.q, T, port=port, init=init)
            j = rnd.randrange(x1); v = (orb[T]['P'][j] + 1 + rnd.randrange(17)) % 19
            for i in range(x1):
                md.equal(E, rows[T][i], v if (test == 'iii' and i == j) else orb[T]['P'][i])
            out[test] = S.solve()
            if test == 'ii' and out[test]:
                mm = set(x for x in S.get_model() if x > 0)
                cl = [g if isinstance(g, int) else int(g[0] in mm) for g in gams]
                out['ii_clock_matches'] = (cl == gclock)
                out['ii_rows_match'] = all(md.val(mm, rows[t][i]) == orb[t]['P'][i] for t in range(0, T + 1, 7) for i in range(x1))
            S.delete()
        out['PASS'] = out['ii'] and not out['iii'] and out.get('ii_clock_matches') and out.get('ii_rows_match')
        print(out, flush=True); return
    port = None
    if a.mode == 'refcheck':
        # positive control: inlet fixed to the REFERENCE carries (genuine orbit of B0 W0^(q+10m+10) U^K, J empty: the
        # window [0,J0) is then deep inside the protected exterior and must return with the standard clock)
        U = md.us()[0]; qq = a.q + 10 * a.m + 10; K = 120 * a.m + 50
        orb = md.orbit(md.realize(md.make_word(U, [], [8, 8], qq, K)), T, x1 + 5)
        port = [orb[t]['c'][orb[t]['L'] - x1] for t in range(T)]
        assert all(orb[t]['g'] == (t % 4 == 0) for t in range(T))
    S = Solver(name=a.solver); E = md.Enc(S)
    P0, rows, gams = build(E, a.q, T, port=port)
    for i in range(x1):
        md.equal(E, rows[T][i], P0[i])
    const_ones = sum(1 for g in gams if isinstance(g, int) and g == 1)
    const_dev = [t for t, g in enumerate(gams) if isinstance(g, int) and g != (t % 4 == 0)]
    var_t = [t for t, g in enumerate(gams) if not isinstance(g, int)]
    if not a.nocount:
        from pysat.card import CardEnc, EncType
        bound = 30 * a.m - const_ones
        if var_t:
            cc = CardEnc.equals(lits=[gams[t][0] for t in var_t], bound=bound, top_id=E.nv, encoding=EncType.totalizer)
            for c in cc.clauses:
                E.add(c)
            E.nv = max(E.nv, cc.nv)
        elif bound != 0:
            E.add([E.new()]); E.add([-E.nv])
    if a.mode == 'rigid' and not const_dev:
        E.add([(-gams[t][0] if t % 4 == 0 else gams[t][0]) for t in var_t])
    print(f'wclock {a.mode} q={a.q} m={a.m} T={T} window=[0,{x1}) clock constant for t < {var_t[0] if var_t else T} '
          f'(constant deviations: {const_dev}) count={not a.nocount} vars={E.nv} clauses={E.ncl} solver={a.solver} enc={time.time()-t0:.0f}s', flush=True)
    r = S.solve()
    if r:
        mm = set(x for x in S.get_model() if x > 0)
        cl = ''.join(str(g if isinstance(g, int) else int(g[0] in mm)) for g in gams)
        print('SAT clock', cl, 'deviations at', [t for t in range(T) if int(cl[t]) != (t % 4 == 0)], flush=True)
    print('RESULT', 'W=[sat]' if r else 'W=[]', 'NONEMPTY' if r else 'EMPTY', f'{time.time()-t0:.0f}s', flush=True)


if __name__ == '__main__':
    main()

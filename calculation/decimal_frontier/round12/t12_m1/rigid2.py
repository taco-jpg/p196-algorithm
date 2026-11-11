#!/usr/bin/env python3
"""r12a rigidity SAT, part 2.  Uses the encoding of rigid.py UNCHANGED (import).

Modes
  validate --U i --Lj n --r R --seed s
      Soundness controls of the FREE-left-port encoding on GENUINE dynamics.
      Genuine rooted configuration B0 W0^14 J U^400 (J random, |J|=n), exact rooted rows
      (seamsat.cone_rows).  Window [y-R, y+M), y = 160+n = start of the U band.
        (0) beta at y+M in the genuine rows == U background beta used by Uleft (all 120 t)
        (a) init = genuine row 0, final = genuine row 120, left port FREE      -> must be SAT
        (b) as (a) with the port fixed to the genuine port values           -> must be SAT
        (c) as (b) with one final column changed                            -> must be UNSAT
        (d) as (a) with the R columns [y-R,y) FREE (only U part fixed)        -> must be SAT
  Uleft --U i --r R [--enum K]
      exactly rigid.py Uleft (all columns of [y-R, y+M) return, right port = U background,
      left port free, (P_{y-3},P_{y-2},P_{y-1}) != U).  --enum K: after each model, block the
      values of the last K free columns and continue (lists every possible K-suffix).
  Wright --j j --r R : exactly rigid.py Wright.
"""
import sys, time, argparse, random
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from seamsat import cone_rows, alpha_at, beta_at
from seam_check import B, W, J0, us
from rigid import Enc, encode


def u_background_right(U, M):
    rows = cone_rows(list(B) + list(W) * 14 + list(U) * 400)
    cb = 160 + 3 * 60 + M
    return [beta_at(rows[t], cb) for t in range(120)]


def validate(a):
    from pysat.solvers import Solver
    rnd = random.Random(a.seed)
    U = us()[a.U]; R = a.r; M = a.M - a.M % 3; n = a.Lj
    J = [rnd.randrange(19) for _ in range(n)]
    pref = list(B) + list(W) * 14 + J + list(U) * 400
    rows = cone_rows(pref)
    y = J0 + n; x0 = y - R; x1 = y + M
    assert x0 >= 64 and all(len(rows[t]) > x1 + 5 for t in range(121))
    right = [beta_at(rows[t], x1) for t in range(120)]
    bg = u_background_right(U, M)
    out = {'U': U, 'J': J, 'R': R, 'right==U_background': right == bg}
    port_al = [alpha_at(rows[t], x0) for t in range(120)]
    port_hl = [(rows[t][x0 - 1] + beta_at(rows[t], x0)) % 10 for t in range(0, 120, 4)]

    def build(fix_cols, fix_port, final_override=None):
        S = Solver(name=a.solver); E = Enc(S)
        init = {i: rows[0][i] for i in fix_cols}
        P0, P, ports = encode(E, x0, x1, init, None, right)
        fin = {i: rows[120][i] for i in range(x0, x1)}
        if final_override: fin.update(final_override)
        for i, v in fin.items():
            E.fix(P[i][v], 1)
        if fix_port:
            for t in range(120):
                E.fix(ports['al0'][t], port_al[t])
            for k, h in enumerate(ports['hl']):
                E.fix(h[port_hl[k]], 1)
        return S, P0, ports
    allc = list(range(x0, x1))
    # (a) [free port] and (d) [free columns] are relaxations of (b): (b) SAT implies both.
    t1 = time.time(); S, P0, ports = build(allc, True); r = S.solve(); out['b_fixed_port_SAT'] = r
    if r:   # the model must reproduce the genuine intermediate rows as well (determinism)
        m = set(l for l in S.get_model() if l > 0)
        out['b_al0_matches'] = all((ports['al0'][t] in m) == bool(port_al[t]) for t in range(120))
    S.delete(); out['b_s'] = round(time.time() - t1, 1)
    i = rnd.randrange(x0, x1); v = (rows[120][i] + 1 + rnd.randrange(17)) % 19
    t1 = time.time(); S, _, _ = build(allc, True, {i: v}); out['c_flipped_final_UNSAT'] = not S.solve(); S.delete()
    out['c_s'] = round(time.time() - t1, 1); out['c_col'] = (i - y, rows[120][i], v)
    # (e) return-version of (b): genuine J is not returning, so 'all columns return' + fixed genuine
    #     port must be UNSAT unless the genuine window happens to return.
    S = Solver(name=a.solver); E = Enc(S)
    P0e, Pe, pe = encode(E, x0, x1, {i: rows[0][i] for i in allc}, None, right)
    for i2 in allc:
        E.fix(Pe[i2][rows[0][i2]], 1)
    for t in range(120):
        E.fix(pe['al0'][t], port_al[t])
    for k, h in enumerate(pe['hl']):
        E.fix(h[port_hl[k]], 1)
    genuine_returns = all(rows[120][i2] == rows[0][i2] for i2 in allc)
    out['e_return_SAT'] = S.solve(); out['e_genuine_window_returns'] = genuine_returns; S.delete()
    ok = out['right==U_background'] and out['b_fixed_port_SAT'] and out.get('b_al0_matches') and \
        out['c_flipped_final_UNSAT'] and (out['e_return_SAT'] == genuine_returns)
    out['PASS'] = ok
    print(out, flush=True)


def uleft(a):
    from pysat.solvers import Solver
    S = Solver(name=a.solver); E = Enc(S); t0 = time.time()
    U = us()[a.U]; R = a.r; M = a.M - a.M % 3
    y = 1000; x0 = y - R; x1 = y + M
    right = u_background_right(U, M)
    init = {i: U[(i - y) % 3] for i in range(y, x1)}
    P0, P, ports = encode(E, x0, x1, init, None, right)
    for i in range(x0, x1):
        for v in range(19):
            E.add([-P0[i][v], P[i][v]])
    if not a.noconstraint:
        E.add([-P0[y - 3 + j][U[j]] for j in range(3)])
    print(f'Uleft U={U} R={R} M={M} vars={E.nv} clauses={E.ncl} solver={a.solver} enc={time.time()-t0:.0f}s', flush=True)
    val = lambda m, vs: next(v for v in range(len(vs)) if vs[v] in m)
    nsol = 0; sufs = []
    while True:
        r = S.solve()
        if not r:
            break
        m = set(l for l in S.get_model() if l > 0)
        cols = [val(m, P0[i]) for i in range(x0, y)]
        nsol += 1
        print('SOL', nsol, 'free columns', cols, f'{time.time()-t0:.0f}s', flush=True)
        if not a.enum:
            break
        K = a.enum
        sufs.append(tuple(cols[-K:]))
        E.add([-P0[y - K + j][cols[R - K + j]] for j in range(K)])
    if a.enum:
        print('RESULT', 'ENUM', nsol, 'suffixes', sorted(set(sufs)), f'{time.time()-t0:.0f}s', flush=True)
    else:
        print('RESULT', 'SAT' if nsol else 'UNSAT', f'{time.time()-t0:.0f}s', flush=True)


def wright(a):
    from pysat.solvers import Solver
    S = Solver(name=a.solver); E = Enc(S); t0 = time.time()
    R = a.r; j = a.j; y = J0 + j; x0 = 64; x1 = y + R
    rows = cone_rows(list(B) + list(W) * 40)
    init = {i: rows[0][i] for i in range(x0, y)}
    P0, P, ports = encode(E, x0, x1, init, rows, None)
    for i in range(x0, x1):
        for v in range(19):
            E.add([-P0[i][v], P[i][v]])
    if not a.noconstraint:
        E.add([-P0[y][W[j % 9]]])
    print(f'Wright j={j} R={R} vars={E.nv} clauses={E.ncl} solver={a.solver} enc={time.time()-t0:.0f}s', flush=True)
    r = S.solve()
    print('RESULT', 'SAT' if r else 'UNSAT', f'{time.time()-t0:.0f}s', flush=True)
    if r:
        m = set(l for l in S.get_model() if l > 0)
        print('free columns', [next(v for v in range(19) if P0[i][v] in m) for i in range(y, x1)], flush=True)




# ---------------------------------------------------------------------------------------------
# Centre-side (comoving) rigidity.  In the absolute left frame the centre region drifts right by
# exactly 15 columns per 120 steps (P(14,100) -> P(14,105): 15 more U columns before C).
# Window [x0, y+R): [x0,y) = U band (exact rooted rows, x0 deep inside the band, y-x0 = Mc >= 122+),
# [y, y+R) free, right port beta_(y+R)(t) FREE (sound while y+R <= middle, i.e. R <= floor(|C|/2)).
# Target: P_120(i) = U-continuation for i-15 < y, P_120(i) = P_0(i-15) otherwise.
# Constraint (P_y,P_(y+1),P_(y+2)) != (U0,U1,U2).
def ucentre(a):
    from pysat.solvers import Solver
    S = Solver(name=a.solver); E = Enc(S); t0 = time.time()
    U = us()[a.U]; R = a.r; Mc = a.Mc - a.Mc % 3; sh = a.shift
    rows = cone_rows(list(B) + list(W) * 14 + list(U) * 400)
    x0 = 160 + 300; y = x0 + Mc; x1 = y + R
    assert all(len(rows[t]) > y + 40 for t in range(121))
    init = {i: rows[0][i] for i in range(x0, y)}
    assert all(init[i] == U[(i - x0) % 3] for i in init)
    P0, P, ports = encode(E, x0, x1, init, rows, None)
    for i in range(x0, x1):
        if i - sh < y:
            E.fix(P[i][U[(i - x0) % 3]], 1)
        else:
            for v in range(19):
                E.add([-P0[i - sh][v], P[i][v]])
    if not a.noconstraint:
        E.add([-P0[y + j][U[j]] for j in range(min(3, R))])
    print(f'Ucentre U={U} R={R} Mc={Mc} shift={sh} vars={E.nv} clauses={E.ncl} solver={a.solver} enc={time.time()-t0:.0f}s', flush=True)
    r = S.solve()
    print('RESULT', 'SAT' if r else 'UNSAT', f'{time.time()-t0:.0f}s', flush=True)
    if r:
        m = set(l for l in S.get_model() if l > 0)
        print('free columns', [next(v for v in range(19) if P0[i][v] in m) for i in range(y, x1)], flush=True)
        print('port be1', ''.join(str(int(v in m)) for v in ports['be1']), flush=True)


# U-band inlet acceptance: [y, y+M) = U^(M/3) returning, free left port.  Enumerate accepted inlets
# (alpha_y(t) 120 bits, hi_(y-1)(t) 30 digits) different from U's own periodic inlet, up to --cap.
def uinlet(a):
    from pysat.solvers import Solver
    S = Solver(name=a.solver); E = Enc(S); t0 = time.time()
    U = us()[a.U]; M = a.M - a.M % 3
    rows = cone_rows(list(B) + list(W) * 14 + list(U) * 400)
    c = 160 + 300
    own_al = [alpha_at(rows[t], c) for t in range(120)]
    own_hl = [(rows[t][c - 1] + beta_at(rows[t], c)) % 10 for t in range(0, 120, 4)]
    y = 1000; x1 = y + M
    right = u_background_right(U, M)
    init = {i: U[(i - y) % 3] for i in range(y, x1)}
    P0, P, ports = encode(E, y, x1, init, None, right)
    for i in range(y, x1):
        E.fix(P[i][U[(i - y) % 3]], 1)
    # sanity: own inlet must be accepted
    ass = [ports['al0'][t] if own_al[t] else -ports['al0'][t] for t in range(120)] + \
          [ports['hl'][k][own_hl[k]] for k in range(30)]
    print(f'Uinlet U={U} M={M} own inlet accepted: {S.solve(assumptions=ass)}', flush=True)
    T = a.tmax   # only differences at times t < T count (T=120: any difference)
    E.add([(-ports['al0'][t] if own_al[t] else ports['al0'][t]) for t in range(T)] +
          [-ports['hl'][k][own_hl[k]] for k in range(30) if 4 * k < T])
    print('difference required at some t <', T, flush=True)
    n = 0
    while n < a.cap and S.solve():
        m = set(l for l in S.get_model() if l > 0)
        al = [int(ports['al0'][t] in m) for t in range(120)]
        hl = [next(v for v in range(10) if ports['hl'][k][v] in m) for k in range(30)]
        n += 1
        print('ACCEPT', n, 'al_diff', [t for t in range(120) if al[t] != own_al[t]],
              'hl_diff', [(4 * k, own_hl[k], hl[k]) for k in range(30) if hl[k] != own_hl[k]], f'{time.time()-t0:.0f}s', flush=True)
        E.add([(-ports['al0'][t] if al[t] else ports['al0'][t]) for t in range(120)] +
              [-ports['hl'][k][hl[k]] for k in range(30)])
    print('RESULT', 'INLETS_OTHER_THAN_OWN', n, 'exhausted' if n < a.cap else 'cap', f'{time.time()-t0:.0f}s', flush=True)


# Positive control for the free-port RETURN encoding on a GENUINE returning configuration with a
# non-trivial left context: B0 W0^inf returns (T12), and B's last 9 letters are not W.
# Window [34-R, 34+MW): [34, 34+MW) = W^(MW/9) (W phase 0 at 34), right port = genuine beta
# (rows of B W^60), [34-R, 34) free, left port FREE, all columns return,
# constraint (P_25..P_33) != W.  Must be SAT (B is a solution).  --pin: also pin the free
# columns to B (must be SAT).
def wleft(a):
    from pysat.solvers import Solver
    S = Solver(name=a.solver); E = Enc(S); t0 = time.time()
    R = a.r; MW = 270; y = 34; x0 = y - R; x1 = y + MW
    assert 9 <= R <= 34
    rows = cone_rows(list(B) + list(W) * 60)
    gen_ret = all(rows[120][i] == rows[0][i] for i in range(0, x1 + 1))
    right = [beta_at(rows[t], x1) for t in range(120)]
    init = {i: W[(i - 34) % 9] for i in range(y, x1)}
    if a.pin:
        init.update({i: B[i] for i in range(x0, y)})
    P0, P, ports = encode(E, x0, x1, init, None, right)
    for i in range(x0, x1):
        for v in range(19):
            E.add([-P0[i][v], P[i][v]])
    E.add([-P0[25 + j][W[j]] for j in range(9)])
    if a.genport:   # genuine port values at x0 (then (pin) is pure propagation of the genuine orbit)
        for t in range(120):
            E.fix(ports['al0'][t], alpha_at(rows[t], x0))
        for k, h in enumerate(ports['hl']):
            t = 4 * k
            E.fix(h[(rows[t][x0 - 1] + beta_at(rows[t], x0)) % 10], 1)
    print(f'Wleft R={R} pin={a.pin} genport={a.genport} genuine B W^inf returns on window: {gen_ret} vars={E.nv} clauses={E.ncl}', flush=True)
    r = S.solve()
    print('RESULT', 'SAT' if r else 'UNSAT', f'{time.time()-t0:.0f}s', flush=True)
    if r:
        m = set(l for l in S.get_model() if l > 0)
        print('free columns', [next(v for v in range(19) if P0[i][v] in m) for i in range(x0, y)], 'B suffix', list(B[x0:y]), flush=True)


# Defect sets.  D_R(V): letters v != V[2] that can stand directly before a MAXIMAL band V^inf
# (V phase 0 at y), with columns [y-R, y-1) free and the left port FREE at y-R, all columns of
# [y-R, y+M) returning, right port = V background beta.  D_R is non-increasing in R.
# Seam lemma (PAPER PROOF, see NOTES): if D_R(V) is empty for all three rotations V of (9,a,18-a)
# (for some R <= 90), no J of any length gives a seam return for any rotation of that a.
def defect(a):
    from pysat.solvers import Solver
    S = Solver(name=a.solver); E = Enc(S); t0 = time.time()
    U = us()[a.U]; R = a.r; M = a.M - a.M % 3
    assert R >= 1
    y = 1000; x0 = y - R; x1 = y + M
    right = u_background_right(U, M)
    init = {i: U[(i - y) % 3] for i in range(y, x1)}
    P0, P, ports = encode(E, x0, x1, init, None, right)
    for i in range(x0, x1):
        for v in range(19):
            E.add([-P0[i][v], P[i][v]])
    E.add([-P0[y - 1][U[2]]])
    print(f'defect U={U} R={R} M={M} vars={E.nv} clauses={E.ncl} solver={a.solver} enc={time.time()-t0:.0f}s', flush=True)
    D = []
    while S.solve():
        m = set(l for l in S.get_model() if l > 0)
        cols = [next(v for v in range(19) if P0[i][v] in m) for i in range(x0, y)]
        D.append(cols[-1])
        print('DEFECT', cols[-1], 'free columns', cols, f'{time.time()-t0:.0f}s', flush=True)
        E.add([-P0[y - 1][cols[-1]]])
    print('RESULT', 'D=' + str(sorted(D)), 'EMPTY' if not D else 'NONEMPTY', f'{time.time()-t0:.0f}s', flush=True)


# Centre-side defect sets (comoving).  E_R(V): letters v != V[0] that can stand at y right after a
# MAXIMAL band V^inf ending at y-1 (V phase 0 at x0 and at y, y-x0 = Mc >= 141 > 122), with
# columns (y, y+R) free and the right port beta_(y+R)(t) FREE (sound while y+R <= middle), left port
# = exact V background (rooted rows).  Target = comoving return: P_120(i) = P_0(i-15), where
# P_0(i-15) for i-15 < y is the band value.  E_R is non-increasing in R.
def cdefect(a):
    from pysat.solvers import Solver
    S = Solver(name=a.solver); E = Enc(S); t0 = time.time()
    U = us()[a.U]; R = a.r; Mc = a.Mc - a.Mc % 3; sh = a.shift
    rows = cone_rows(list(B) + list(W) * 14 + list(U) * 400)
    x0 = 160 + 300; y = x0 + Mc; x1 = y + R
    assert all(len(rows[t]) > y + 40 for t in range(121))
    init = {i: rows[0][i] for i in range(x0, y)}
    assert all(init[i] == U[(i - x0) % 3] for i in init)
    P0, P, ports = encode(E, x0, x1, init, rows, None)
    for i in range(x0, x1):
        if i - sh < y:
            E.fix(P[i][U[(i - x0) % 3]], 1)
        else:
            for v in range(19):
                E.add([-P0[i - sh][v], P[i][v]])
    E.add([-P0[y][U[0]]])
    print(f'cdefect U={U} R={R} Mc={Mc} shift={sh} vars={E.nv} clauses={E.ncl} solver={a.solver} enc={time.time()-t0:.0f}s', flush=True)
    D = []
    while S.solve():
        m = set(l for l in S.get_model() if l > 0)
        cols = [next(v for v in range(19) if P0[i][v] in m) for i in range(y, x1)]
        D.append(cols[0])
        print('DEFECT', cols[0], 'free columns', cols, 'port be1', ''.join(str(int(v in m)) for v in ports['be1']), f'{time.time()-t0:.0f}s', flush=True)
        E.add([-P0[y][cols[0]]])
    print('RESULT', 'E=' + str(sorted(D)), 'EMPTY' if not D else 'NONEMPTY', f'{time.time()-t0:.0f}s', flush=True)


# Validation of the centre-side encoding (exact left rows, FREE right port) on GENUINE dynamics:
# genuine U^k C rev(U)^k (with B W^14 J0 prefix) is not needed: we use the rooted configuration
# B W^14 U^400 itself (whose band is genuine) and a planted defect C-like block inside the rooted prefix:
# pref = B W^14 U^200 X U^200 (X random), rows exact; window [x0, y+R) with y = start of X;
# fix init = genuine, final = genuine row 120 (NOT shifted), right port fixed to genuine -> SAT;
# one final value changed -> UNSAT.
def cvalidate(a):
    from pysat.solvers import Solver
    rnd = random.Random(a.seed)
    U = us()[a.U]; R = a.r; Mc = a.Mc - a.Mc % 3
    X = [rnd.randrange(19) for _ in range(max(R, 3) + 5)]
    pref = list(B) + list(W) * 14 + list(U) * 200 + X + list(U) * 200
    rows = cone_rows(pref)
    y = 160 + 600; x0 = y - Mc; x1 = y + R
    assert all(len(rows[t]) > x1 + 5 for t in range(121))
    gen_be = [beta_at(rows[t], x1) for t in range(120)]
    out = {'U': U, 'X': X, 'R': R}
    for flip in (False, True):
        S = Solver(name=a.solver); E = Enc(S)
        P0, P, ports = encode(E, x0, x1, {i: rows[0][i] for i in range(x0, x1)}, rows, None)
        fin = {i: rows[120][i] for i in range(x0, x1)}
        if flip:
            i = rnd.randrange(x0, x1); fin[i] = (fin[i] + 1 + rnd.randrange(17)) % 19
        for i, v in fin.items():
            E.fix(P[i][v], 1)
        for t in range(120):
            E.fix(ports['be1'][t], gen_be[t])
        out['flip' if flip else 'genuine'] = S.solve(); S.delete()
    out['PASS'] = out['genuine'] and not out['flip']
    print(out, flush=True)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('mode')
    ap.add_argument('--U', type=int, default=0)
    ap.add_argument('--j', type=int, default=0)
    ap.add_argument('--r', type=int, default=3)
    ap.add_argument('--M', type=int, default=171)
    ap.add_argument('--Lj', type=int, default=12)
    ap.add_argument('--seed', type=int, default=1)
    ap.add_argument('--enum', type=int, default=0)
    ap.add_argument('--noconstraint', action='store_true')
    ap.add_argument('--solver', default='cadical195')
    ap.add_argument('--Mc', type=int, default=141)
    ap.add_argument('--shift', type=int, default=15)
    ap.add_argument('--cap', type=int, default=20)
    ap.add_argument('--pin', action='store_true')
    ap.add_argument('--genport', action='store_true')
    ap.add_argument('--tmax', type=int, default=120)
    a = ap.parse_args()
    {'validate': validate, 'Uleft': uleft, 'Wright': wright, 'Ucentre': ucentre, 'Uinlet': uinlet, 'Wleft': wleft, 'defect': defect, 'cdefect': cdefect, 'cvalidate': cvalidate}[a.mode](a)

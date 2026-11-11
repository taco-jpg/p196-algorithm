#!/usr/bin/env python3
"""r12f: m-period (T = 120m steps) defect sets for the T12 template, cone-trimmed exact folded two-carry encoding.

Generalises r12a rigid.py / rigid2.py to T = 120m steps.  Same clause structure as rigid.py (one-hot pair value
0..18, one-hot low/high digits 0..9, carry bits, translation-invariant bulk rule, forced clock gamma_t=[t%4==0]).
New: only the region that can differ from the periodic band background is encoded.  By the T12 carry-difference
cone lemma (exact front recurrences, cones_m.py) every column beyond the moving front of a pure band equals the
background row V_t, and every carry entering from there is the periodic background carry; such values enter the
clauses as constants.  The front used is the exact front + DELTA (default 3) extra columns.

Folded two-carry law: lo_i=(P_i+alpha_i)%10, hi_i=(P_i+beta_(i+1))%10, alpha_(i+1)=[P_i+alpha_i>=10],
beta_i=[P_i+beta_(i+1)>=10]; P'_i = lo_i+hi_i (gamma=0), lo_i+hi_(i-1) (gamma=1).

Modes
 defect  --U v --r R --m m : D_R^(m)(V).  Columns [y-R,y-1) free, column y-1 = v != V[2], [y,inf) = V^inf (V phase 0 at y),
          left port FREE at y-R (alpha bits, overflow-step high digit), right side exact background beyond the
          junction-side front, every column returns after 120m steps.  Enumerates D (blocking clauses).
 cdefect --U v --r R --m m : E_R^(m)(V) (comoving shift 15m).  (-inf,y) = V^inf (V phase 0 at y), column y = v != V[0],
          (y,y+R) free, right port beta_(y+R)(t) FREE, left side exact background beyond the centre-side front,
          target P_T(i) = band value if i-15m < y, P_0(i-15m) otherwise.
 uleft   --U v --r 3 --m m : depth-3 left rigidity (r12a rigid.py Uleft, m epochs): columns [y-3,y) free with
          (P_(y-3),P_(y-2),P_(y-1)) != (V0,V1,V2), [y,inf) = V^inf, left port FREE at y-3, every column returns.
          UNSAT => D_3(V) = D_2(V'') = D_1(V') = empty for the three rotations V, V'=(V1,V2,V0), V''=(V2,V0,V1)
          (r12a NOTES: case split on the first deviating position of the triple).
 validate  --U v --r R --m m --Lj n --seed s : seam-side encoding on a GENUINE big-integer orbit.
 cvalidate --U v --r R --m m --Lj n --seed s : centre-side encoding on a GENUINE big-integer orbit.
"""
import sys, time, argparse, random

sys.set_int_max_str_digits(10 ** 6)
B0 = (10, 4, 6, 6, 7, 12, 9, 16, 16, 13, 0, 2, 10, 17, 7, 0, 18, 6, 5, 18, 4, 18, 14, 9, 14, 8, 12, 17, 10, 4, 6, 4, 0, 5)
W0 = (5, 18, 4, 8, 1, 15, 4, 0, 5)
G = lambda t: 1 if t % 4 == 0 else 0
Tc = lambda x, c: 1 if x + c >= 10 else 0
DELTA = 3


def us():
    return [tuple((9, a, 18 - a)[r:] + (9, a, 18 - a)[:r]) for a in range(0, 19, 2) for r in range(3)]


def band_bg(V, T):
    """Cyclic band background.  rows[t] (3 letters by phase), al[t][ph] = periodic alpha entering a phase-ph column,
    be[t][ph] = periodic beta_x for x of phase ph (carry passed from column x to column x-1)."""
    rows = [tuple(V)]; al = []; be = []
    for t in range(T):
        w = rows[-1]; a = [0] * 3; b = [0] * 3; c = 0
        for _ in range(3):
            for j in range(3):
                a[j] = c; c = Tc(w[j], c)
        c = 0
        for _ in range(3):
            for j in (2, 1, 0):
                c = Tc(w[j], c); b[j] = c
        lo = [(w[j] + a[j]) % 10 for j in range(3)]
        hi = [(w[j] + b[(j + 1) % 3]) % 10 for j in range(3)]
        rows.append(tuple(lo[j] + (hi[(j - 1) % 3] if G(t) else hi[j]) for j in range(3)))
        al.append(a); be.append(b)
    return rows, al, be


def fronts(V, T, rows):
    """exact carry-difference fronts of a pure V band (V phase 0 at its first column / after its last column)."""
    l = [0]; r = [0]
    for t in range(T):
        w = rows[t]
        l.append(l[-1] + 1 + (w[l[-1] % 3] == 9))
        r.append(r[-1] + 1 + (w[(-r[-1] - 1) % 3] == 9) - G(t))
    return l, r


class Enc:
    def __init__(s, solver):
        s.S = solver; s.nv = 0; s.ncl = 0

    def add(s, c):
        s.S.add_clause(c); s.ncl += 1

    def new(s):
        s.nv += 1; return s.nv

    def onehot(s, k):
        vs = list(range(s.nv + 1, s.nv + 1 + k)); s.nv += k
        s.add(list(vs))
        for i in range(k):
            for j in range(i + 1, k):
                s.add([-vs[i], -vs[j]])
        return vs


# carries: constant = int 0/1, variable = 1-tuple (v,)   (never a bare int: var ids would look like constants)
def lit(c, b):            # literal "carry var c == b"
    return c[0] if b else -c[0]


def carry(E, P, c):       # T(P + c); P int|onehot19, c int|var
    if isinstance(P, int):
        return Tc(P, 0) if P != 9 else c
    o = (E.new(),)
    if isinstance(c, int):
        for x in range(19):
            E.add([-P[x], o[0] if Tc(x, c) else -o[0]])
    else:
        for x in range(19):
            for b in (0, 1):
                E.add([-P[x], -lit(c, b), o[0] if Tc(x, b) else -o[0]])
    return o


def digit(E, P, c):       # (P + c) % 10 ; int|onehot10
    if isinstance(P, int) and isinstance(c, int):
        return (P + c) % 10
    d = E.onehot(10)
    if isinstance(P, int):
        E.add([c[0], d[P % 10]]); E.add([-c[0], d[(P + 1) % 10]])
    elif isinstance(c, int):
        for x in range(19):
            E.add([-P[x], d[(x + c) % 10]])
    else:
        for x in range(19):
            for b in (0, 1):
                E.add([-P[x], -lit(c, b), d[(x + b) % 10]])
    return d


def psum(E, lo, hi):      # lo + hi ; int|onehot19
    if isinstance(lo, int) and isinstance(hi, int):
        return lo + hi
    v = E.onehot(19)
    if isinstance(lo, int):
        for b in range(10):
            E.add([-hi[b], v[lo + b]])
    elif isinstance(hi, int):
        for a in range(10):
            E.add([-lo[a], v[a + hi]])
    else:
        for a in range(10):
            for b in range(10):
                E.add([-lo[a], -hi[b], v[a + b]])
    return v


def equal(E, X, Y):
    if isinstance(X, int) and isinstance(Y, int):
        if X != Y:
            print('WARNING: constant mismatch in equal()', X, Y, flush=True)
            z = E.new(); E.add([z]); E.add([-z])
    elif isinstance(Y, int):
        E.add([X[Y]])
    elif isinstance(X, int):
        E.add([Y[X]])
    else:
        for v in range(19):
            E.add([-Y[v], X[v]])


def step(E, t, row, a0, b0, a1, b1, bg, left, right):
    """row: dict i -> value (int|onehot19) on [a0,b0) at time t.  Returns (new row on [a1,b1), port dict).
    bg = (bgP, bga, bgb): background value / alpha entering column i / beta_x at time t.
    left 'free' (a1 == a0; alpha_(a0) free bit, hi_(a0-1) free digit at overflow) or 'exact' (constant background left of the region);
    right 'free' (b1 == b0; beta_(b0) free bit) or 'exact' (constant background right of the region)."""
    bgP, bga, bgb = bg
    g = G(t)
    P = lambda i: row[i] if a0 <= i < b0 else bgP(t, i)
    port = {}
    if left == 'free':
        assert a1 == a0
        start = a0; al = {start: (E.new(),)}; port['al'] = al[start]
    else:
        start = min(a0, a1); al = {start: bga(t, start)}
    for i in range(start, b1 - 1):
        al[i + 1] = carry(E, P(i), al[i])
    if right == 'free':
        assert b1 == b0
        top = b0; be = {top: (E.new(),)}; port['be'] = be[top]
    else:
        top = max(b0, b1); be = {top: bgb(t, top)}
    lowx = a1 + 1 if not g else a1
    for x in range(top - 1, lowx - 1, -1):
        be[x] = carry(E, P(x), be[x + 1])
    hi_idx = range(a1, b1) if not g else range(a1 - 1, b1 - 1)
    hi = {}
    for j in hi_idx:
        if left == 'free' and j == a0 - 1:
            hi[j] = E.onehot(10); port['hl'] = hi[j]
        else:
            hi[j] = digit(E, P(j), be[j + 1])
    new = {}
    for i in range(a1, b1):
        lo = digit(E, P(i), al[i])
        new[i] = psum(E, lo, hi[i] if not g else hi[i - 1])
    port['be_out'] = be.get(a1 + 1 if not g else a1)
    return new, port


def bgfun(V, y, rows, alb, beb):
    return (lambda t, i: rows[t][(i - y) % 3], lambda t, i: alb[t][(i - y) % 3], lambda t, x: beb[t][(x - y) % 3])


def build_seam(E, V, R, T, y=3000, init=None, delta=DELTA):
    """seam-side region: [y-R, y+l_t+delta), left FREE, right exact.  init: optional dict col->value (genuine)."""
    rows, alb, beb = band_bg(V, T); l, r = fronts(V, T, rows)
    a = y - R; b = [y + l[t] + delta for t in range(T + 1)]
    bg = bgfun(V, y, rows, alb, beb)
    row = {}
    for i in range(a, b[0]):
        if init is not None and i in init:
            row[i] = E.onehot(19); E.add([row[i][init[i]]])
        elif i < y:
            row[i] = E.onehot(19)
        else:
            row[i] = V[(i - y) % 3]
    P0 = dict(row); ports = []
    for t in range(T):
        row, port = step(E, t, row, a, b[t], a, b[t + 1], bg, 'free', 'exact')
        ports.append(port)
    return P0, row, ports, (a, b, l, rows, alb, beb)


def build_centre(E, V, R, T, y=30000, init=None, delta=DELTA):
    """centre-side region: [y-r_t-delta, y+R), left exact, right FREE."""
    rows, alb, beb = band_bg(V, T); l, r = fronts(V, T, rows)
    b = y + R; a = [y - r[t] - delta for t in range(T + 1)]
    bg = bgfun(V, y, rows, alb, beb)
    row = {}
    for i in range(a[0], b):
        if init is not None and i in init:
            row[i] = E.onehot(19); E.add([row[i][init[i]]])
        elif i >= y:
            row[i] = E.onehot(19)
        else:
            row[i] = V[(i - y) % 3]
    P0 = dict(row); ports = []
    for t in range(T):
        row, port = step(E, t, row, a[t], b, a[t + 1], b, bg, 'exact', 'free')
        ports.append(port)
    return P0, row, ports, (a, b, r, rows, alb, beb)


def val(m, vs):
    return vs if isinstance(vs, int) else next(v for v in range(len(vs)) if vs[v] in m)


def defect(a):
    from pysat.solvers import Solver
    V = us()[a.U]; R = a.r; T = 120 * a.m; t0 = time.time()
    S = Solver(name=a.solver); E = Enc(S); y = 3000
    P0, PT, ports, (x0, b, l, *_ ) = build_seam(E, V, R, T, y=y, delta=a.delta)
    for i in range(x0, b[T]):
        equal(E, PT[i], P0[i] if i < b[0] else V[(i - y) % 3])
    excl = [V[2]] + [v for v in range(19) if a.only and v not in a.only and v != V[2]]
    for v in excl:
        E.add([-P0[y - 1][v]])
    print(f'mdefect only={a.only or "all"} U={a.U} V={V} R={R} m={a.m} T={T} front l_T={l[T]} delta={a.delta} region_T=[y-{R},y+{b[T]-y}) '
          f'vars={E.nv} clauses={E.ncl} solver={a.solver} enc={time.time()-t0:.0f}s', flush=True)
    D = []; blocked = []
    incremental = a.solver.startswith('cadical') or a.solver.startswith('glucose')
    while True:
        r = S.solve()
        if not r:
            break
        m = set(x for x in S.get_model() if x > 0)
        cols = [val(m, P0[i]) for i in range(x0, y)]
        D.append(cols[-1])
        print('DEFECT', cols[-1], 'free columns', cols, f'{time.time()-t0:.0f}s', flush=True)
        if a.firstonly:
            break
        blocked.append(cols[-1])
        if incremental:
            E.add([-P0[y - 1][cols[-1]]])
        else:
            S.delete(); S = Solver(name=a.solver); E = Enc(S)
            P0, PT, ports, (x0, b, l, *_ ) = build_seam(E, V, R, T, y=y, delta=a.delta)
            for i in range(x0, b[T]):
                equal(E, PT[i], P0[i] if i < b[0] else V[(i - y) % 3])
            for v in excl + blocked:
                E.add([-P0[y - 1][v]])
    print('RESULT', 'D=' + str(sorted(D)), 'EMPTY' if not D else ('NONEMPTY' if not a.firstonly else 'NONEMPTY(first only)'),
          f'{time.time()-t0:.0f}s', flush=True)


def uleft(a):
    from pysat.solvers import Solver
    V = us()[a.U]; R = a.r; T = 120 * a.m; t0 = time.time()
    assert R >= 3
    S = Solver(name=a.solver); E = Enc(S); y = 3000
    P0, PT, ports, (x0, b, l, *_ ) = build_seam(E, V, R, T, y=y, delta=a.delta)
    for i in range(x0, b[T]):
        equal(E, PT[i], P0[i] if i < b[0] else V[(i - y) % 3])
    E.add([-P0[y - 3 + j][V[j]] for j in range(3)])
    print(f'muleft U={a.U} V={V} R={R} m={a.m} T={T} front l_T={l[T]} delta={a.delta} vars={E.nv} clauses={E.ncl} '
          f'solver={a.solver} enc={time.time()-t0:.0f}s', flush=True)
    r = S.solve()
    if r:
        m = set(x for x in S.get_model() if x > 0)
        print('free columns', [val(m, P0[i]) for i in range(x0, y)], flush=True)
    print('RESULT', 'U=[sat]' if r else 'U=[]', 'NONEMPTY' if r else 'EMPTY', f'{time.time()-t0:.0f}s',
          '(SAT: not rigid)' if r else '(UNSAT: depth-3 left-rigid)', flush=True)


def centre_target(E, PT, P0, V, y, aT, b, S):
    for i in range(aT, b):
        equal(E, PT[i], V[(i - y) % 3] if i - S < y else P0[i - S])


def cdefect(a):
    from pysat.solvers import Solver
    V = us()[a.U]; R = a.r; T = 120 * a.m; Sh = 15 * a.m; t0 = time.time()
    S = Solver(name=a.solver); E = Enc(S); y = 30000

    def build(S, E):
        P0, PT, ports, (aa, b, r, *_ ) = build_centre(E, V, R, T, y=y, delta=a.delta)
        centre_target(E, PT, P0, V, y, aa[T], b, Sh)
        return P0, PT, ports, aa, r
    P0, PT, ports, aa, r = build(S, E)
    excl = [V[0]] + [v for v in range(19) if a.only and v not in a.only and v != V[0]]
    for v in excl:
        E.add([-P0[y][v]])
    print(f'mcdefect only={a.only or "all"} U={a.U} V={V} R={R} m={a.m} T={T} shift={Sh} front r_T={r[T]} delta={a.delta} region_T=[y-{y-aa[T]},y+{R}) '
          f'vars={E.nv} clauses={E.ncl} solver={a.solver} enc={time.time()-t0:.0f}s', flush=True)
    D = []
    incremental = a.solver.startswith('cadical') or a.solver.startswith('glucose')
    while True:
        res = S.solve()
        if not res:
            break
        m = set(x for x in S.get_model() if x > 0)
        cols = [val(m, P0[i]) for i in range(y, y + R)]
        D.append(cols[0])
        print('DEFECT', cols[0], 'free columns', cols, 'port be', ''.join(str(int(p['be'][0] in m)) for p in ports), f'{time.time()-t0:.0f}s', flush=True)
        if a.firstonly:
            break
        if incremental:
            E.add([-P0[y][cols[0]]])
        else:
            S.delete(); S = Solver(name=a.solver); E = Enc(S)
            P0, PT, ports, aa, r = build(S, E)
            for v in excl + D:
                E.add([-P0[y][v]])
    print('RESULT', 'E=' + str(sorted(D)), 'EMPTY' if not D else ('NONEMPTY' if not a.firstonly else 'NONEMPTY(first only)'),
          f'{time.time()-t0:.0f}s', flush=True)


# ------------------------------------------------------------------ genuine big-integer orbits
def realize(P):
    L = len(P); d = [0] * L
    for i in range(L // 2):
        d[i] = max(0, P[i] - 9); d[L - 1 - i] = P[i] - d[i]
    if L % 2:
        assert P[L // 2] % 2 == 0
        d[L // 2] = P[L // 2] // 2
    assert d[-1] > 0 and all(0 <= x <= 9 for x in d)
    return int(''.join(map(str, reversed(d))))


def orbit(N, T, ncols):
    """T genuine steps n -> n + reverse(n).  Returns per t: pair row (first ncols), low carries c_0..c_ncols,
    function beta(t, x) = c_(L-x), high digits e, gamma."""
    out = []
    for t in range(T + 1):
        s = str(N)[::-1]; dd = [int(ch) for ch in s]; L = len(dd)
        P = [dd[i] + dd[L - 1 - i] for i in range(L)]
        c = [0] * (L + 1); e = [0] * L
        for i in range(L):
            z = P[i] + c[i]; e[i] = z % 10; c[i + 1] = z // 10
        out.append({'P': P[:ncols], 'c': c, 'e': e, 'L': L, 'g': c[L]})
        if t < T:
            N2 = N + int(s)
            assert [int(ch) for ch in str(N2)[::-1]][:L] == e and (len(str(N2)) - L) == c[L]
            N = N2
    return out


def make_word(V, J, C, q, K):
    H = list(B0) + list(W0) * q + list(J) + list(V) * K
    return H + list(C) + H[::-1]


def validate(a):
    """seam side: P = B0 W0^q J V^K C rev(...), y = start of the V band, region as in defect mode.
    (i) genuine rows beyond the front == background and genuine beta at the region edge == background,
    (ii) genuine init + genuine ports + genuine final -> SAT and the model's port/edge carries == genuine,
    (iii) one changed final value -> UNSAT, (iv) return required with genuine init/ports -> SAT iff genuine window returns."""
    from pysat.solvers import Solver
    rnd = random.Random(a.seed); V = us()[a.U]; R = a.r; T = 120 * a.m
    q = 10 * a.m + 6; K = 100 * a.m + 100
    J = [rnd.randrange(19) for _ in range(a.Lj)]
    h = [rnd.randrange(19) for _ in range(3)]; C = h + h[::-1]
    y = 34 + 9 * q + a.Lj; x0 = y - R
    rows_bg, alb, beb = band_bg(V, T); l, r = fronts(V, T, rows_bg)
    b = [y + l[t] + a.delta for t in range(T + 1)]
    assert 3 * K > l[T] + r[T] + 80
    orb = orbit(realize(make_word(V, J, C, q, K)), T, b[T] + 60)
    assert all(orb[t]['g'] == G(t) for t in range(T)), 'clock'
    out = {'U': a.U, 'V': V, 'J': J, 'R': R, 'm': a.m}
    out['i_beyond_front_is_background'] = all(orb[t]['P'][i] == rows_bg[t][(i - y) % 3] for t in range(T + 1) for i in range(y + l[t], b[T] + 60))
    out['i_edge_beta_is_background'] = all(orb[t]['c'][orb[t]['L'] - b[t]] == beb[t][(b[t] - y) % 3] for t in range(T))
    out['i_front_tight_somewhere'] = any(orb[t]['P'][y + l[t] - 1] != rows_bg[t][(y + l[t] - 1 - y) % 3] for t in range(1, T + 1))
    init = {i: orb[0]['P'][i] for i in range(x0, b[0])}
    gal = [orb[t]['c'][x0] for t in range(T)]
    ghl = [orb[t]['e'][orb[t]['L'] - x0] for t in range(T)]          # hi_(x0-1) = e_(L-1-(x0-1))
    for test in ('ii', 'iii', 'iv'):
        S = Solver(name=a.solver); E = Enc(S)
        P0, PT, ports, _ = build_seam(E, V, R, T, y=y, init=init, delta=a.delta)
        for t in range(T):
            E.add([lit(ports[t]['al'], gal[t])])
            if 'hl' in ports[t]:
                E.add([ports[t]['hl'][ghl[t]]])
        if test == 'ii':
            for i in range(x0, b[T]):
                equal(E, PT[i], orb[T]['P'][i])
        elif test == 'iii':
            j = rnd.randrange(x0, b[T]); w = (orb[T]['P'][j] + 1 + rnd.randrange(17)) % 19
            out['iii_col'] = (j - y, orb[T]['P'][j], w)
            for i in range(x0, b[T]):
                equal(E, PT[i], w if i == j else orb[T]['P'][i])
        else:
            for i in range(x0, b[T]):
                equal(E, PT[i], orb[0]['P'][i])
        res = S.solve(); out[test] = res
        if test == 'ii' and res:
            m = set(x for x in S.get_model() if x > 0)
            ok = True
            for t in range(T):
                be = ports[t]['be_out']
                gv = orb[t]['c'][orb[t]['L'] - (x0 + 1 if not G(t) else x0)]
                if isinstance(be, int):
                    ok &= (be == gv)
                else:
                    ok &= ((be[0] in m) == bool(gv))
            out['ii_port_beta_matches'] = ok
        S.delete()
    out['genuine_window_returns'] = all(orb[T]['P'][i] == orb[0]['P'][i] for i in range(x0, b[T]))
    out['PASS'] = (out['i_beyond_front_is_background'] and out['i_edge_beta_is_background'] and out['ii'] and
                   out.get('ii_port_beta_matches', False) and not out['iii'] and out['iv'] == out['genuine_window_returns'])
    print(out, flush=True)


def cvalidate(a):
    """centre side: P = B0 W0^q J V^K C rev(...), y = first column of C (V phase 0), region as in cdefect mode.
    (i) genuine rows left of the region == background, genuine alpha at the region edge == background,
    (ii) genuine init + genuine right port + genuine (unshifted) final -> SAT, (iii) one changed final value -> UNSAT,
    (iv) comoving target with genuine init/port -> SAT iff the genuine window satisfies it."""
    from pysat.solvers import Solver
    rnd = random.Random(a.seed); V = us()[a.U]; R = a.r; T = 120 * a.m; Sh = 15 * a.m
    q = 10 * a.m + 6; K = 100 * a.m + 100
    J = [rnd.randrange(19) for _ in range(a.Lj)]
    hlen = R + 8; h = [rnd.randrange(19) for _ in range(hlen)]; C = h + h[::-1]
    y = 34 + 9 * q + a.Lj + 3 * K
    rows_bg, alb, beb = band_bg(V, T); l, r = fronts(V, T, rows_bg)
    aa = [y - r[t] - a.delta for t in range(T + 1)]; b = y + R
    orb = orbit(realize(make_word(V, J, C, q, K)), T, b + 10)
    assert all(orb[t]['g'] == G(t) for t in range(T)), 'clock'
    assert all(b + 2 < orb[t]['L'] // 2 for t in range(T + 1))
    out = {'U': a.U, 'V': V, 'C': C, 'R': R, 'm': a.m}
    out['i_left_is_background'] = all(orb[t]['P'][i] == rows_bg[t][(i - y) % 3] for t in range(T + 1) for i in range(aa[t] - 60, y - r[t]))
    out['i_edge_alpha_is_background'] = all(orb[t]['c'][aa[t + 1]] == alb[t][(aa[t + 1] - y) % 3] for t in range(T))
    init = {i: orb[0]['P'][i] for i in range(aa[0], b)}
    gbe = [orb[t]['c'][orb[t]['L'] - b] for t in range(T)]
    for test in ('ii', 'iii', 'iv'):
        S = Solver(name=a.solver); E = Enc(S)
        P0, PT, ports, _ = build_centre(E, V, R, T, y=y, init=init, delta=a.delta)
        for t in range(T):
            E.add([lit(ports[t]['be'], gbe[t])])
        if test == 'ii':
            for i in range(aa[T], b):
                equal(E, PT[i], orb[T]['P'][i])
        elif test == 'iii':
            j = rnd.randrange(aa[T], b); w = (orb[T]['P'][j] + 1 + rnd.randrange(17)) % 19
            out['iii_col'] = (j - y, orb[T]['P'][j], w)
            for i in range(aa[T], b):
                equal(E, PT[i], w if i == j else orb[T]['P'][i])
        else:
            for i in range(aa[T], b):
                equal(E, PT[i], V[(i - y) % 3] if i - Sh < y else init[i - Sh])
        out[test] = S.solve(); S.delete()
    out['genuine_comoving'] = all(orb[T]['P'][i] == (V[(i - y) % 3] if i - Sh < y else orb[0]['P'][i - Sh]) for i in range(aa[T], b))
    out['PASS'] = (out['i_left_is_background'] and out['i_edge_alpha_is_background'] and out['ii'] and not out['iii']
                   and out['iv'] == out['genuine_comoving'])
    print(out, flush=True)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('mode')
    ap.add_argument('--U', type=int, default=0)
    ap.add_argument('--r', type=int, default=12)
    ap.add_argument('--m', type=int, default=2)
    ap.add_argument('--Lj', type=int, default=12)
    ap.add_argument('--seed', type=int, default=1)
    ap.add_argument('--delta', type=int, default=DELTA)
    ap.add_argument('--firstonly', action='store_true')
    ap.add_argument('--only', default='', help='comma list: restrict the defect letter to these values (split runs)')
    ap.add_argument('--solver', default='cadical195')
    a = ap.parse_args()
    a.only = [int(x) for x in a.only.split(',')] if a.only else []
    {'defect': defect, 'cdefect': cdefect, 'uleft': uleft, 'validate': validate, 'cvalidate': cvalidate}[a.mode](a)

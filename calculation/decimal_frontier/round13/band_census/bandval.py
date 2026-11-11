#!/usr/bin/env python3
"""r13a: genuine big-integer validation of the L and R encodings of bandsat.py (any base).
Usage: bandval.py SEED [--b 10] [--T 40] [--R 12] [--n 3] [--notrim] [--solver cadical195]
Builds n with pair word  A J V^K C rev(V)^K rev(J) rev(A)  (random A, J, centre C), runs the genuine orbit
n -> n + rev(n) for T steps (ANY clock: the genuine overflow sequence is fed to the encoder),
checks (a) the folded law on every column, (b) the cone recurrences for the pure band,
(c) L encoding with genuine left port: model letters == genuine letters at all (t,c), forbidding a final letter UNSAT,
(d) R encoding with genuine right port (beta_(z+R)(t) from the genuine carries): same.
Also runs with the first-order background rows computed by rowstep under the genuine clock."""
import sys, random, argparse, time
import bandsat as BS
import bandsat2 as BS2
ENC=1
def build_L(*a,**k):
    return BS.build_L(*a,**k) if ENC==1 else BS2.build_L2(*a,**k)
def build_R(*a,**k):
    return BS.build_R(*a,**k) if ENC==1 else BS2.build_R2(*a,**k)


def digits(n, b):
    d = []
    while n:
        d.append(n % b)
        n //= b
    return d or [0]


def val(d, b):
    n = 0
    for x in reversed(d):
        n = n * b + x
    return n


def pair(n, b):
    d = digits(n, b)
    L = len(d)
    return [d[i] + d[L - 1 - i] for i in range(L)]


def add_rev(n, b):
    d = digits(n, b)
    return n + val(d[::-1], b)


def make_number(P, b, rnd):
    L = len(P)
    d = [0] * L
    for i in range(L // 2):
        p = P[i]
        # choose a valid split d[i]+d[L-1-i] = p, both digits in 0..b-1
        lo = max(0, p - (b - 1))
        hi = min(p, b - 1)
        x = rnd.randint(lo, hi)
        d[i] = x
        d[L - 1 - i] = p - x
    if L % 2:
        assert P[L // 2] % 2 == 0
        d[L // 2] = P[L // 2] // 2
    if d[L - 1] == 0:
        # P[0] >= 1 is required; move a digit
        d[L - 1], d[0] = d[0], d[L - 1]
    assert d[L - 1] >= 1
    n = val(d, b)
    assert pair(n, b) == P
    return n


def orbit(n, b, T):
    Ps, gam = [], []
    for t in range(T + 1):
        P = pair(n, b)
        Ps.append(P)
        if t == T:
            break
        m = add_rev(n, b)
        Pn = pair(m, b)
        g = len(Pn) - len(P)
        assert g in (0, 1)
        gam.append(g)
        # law check on all columns of the left half
        L = len(P)
        alpha = [0] * (L + 1)
        e = [0] * L
        for i in range(L):
            z = P[i] + alpha[i]
            e[i] = z % b
            alpha[i + 1] = 1 if z >= b else 0
        for i in range(L // 2):
            lo = e[i]
            if g:
                hi = e[L - i] if i > 0 else 1
            else:
                hi = e[L - 1 - i]
            assert lo + hi == Pn[i], (t, i)
        n = m
    return Ps, gam, n


def carries(P, b):
    """alpha[i] for i = 0..L and hi-digit list e (digit of the sum at position i)."""
    L = len(P)
    alpha = [0] * (L + 1)
    e = [0] * L
    for i in range(L):
        z = P[i] + alpha[i]
        e[i] = z % b
        alpha[i + 1] = 1 if z >= b else 0
    return alpha, e


def run(seed, b=10, T=40, R=12, n=3, trim=True, solver='cadical195', RW=8):
    rnd = random.Random(seed)
    NL = 2 * b - 1
    while True:
        V = [rnd.randrange(NL) for _ in range(n)]
        if any(v != b - 1 for v in V):
            break
    # a random prefix: length 25..45 columns, first letter >= 1
    A = [rnd.randrange(1, NL)] + [rnd.randrange(NL) for _ in range(rnd.randrange(24, 45))]
    J = [rnd.randrange(NL) for _ in range(rnd.randrange(0, 8))]
    # foreign letter just before the band: force A+J last letter != V[-1]
    Js = A + J
    while Js[-1] == V[-1]:
        Js[-1] = rnd.randrange(NL)
    Kw = 2 * (3 * T + 40) // len(V) + 4  # band long enough on both sides
    # random centre with foreign first letter, long enough for the R window
    c_half = RW + 6
    Ch = [rnd.randrange(NL) for _ in range(c_half)]
    while Ch[0] == V[0]:
        Ch[0] = rnd.randrange(NL)
    if rnd.random() < 0.5:
        C = Ch + Ch[::-1]
    else:
        m = rnd.randrange(0, NL, 2)
        C = Ch + [m] + Ch[::-1]
    P0 = Js + V * Kw + C + (V[::-1]) * Kw + Js[::-1]
    # (V[::-1] mirror of V: the mirror image of the band)
    y = len(Js)
    z = len(Js) + n * Kw
    n0 = make_number(P0, b, rnd)
    Ps, gam, _ = orbit(n0, b, T)
    print(f'seed={seed} b={b} n={n} V={V} T={T} L0={len(P0)} y={y} z={z} overflows={sum(gam)}', flush=True)
    # background under genuine clock
    rows_bg = BS.background(V, gam, b)
    rows, As, Bs, Ls, Hs = rows_bg
    lf = BS.left_fronts(rows, b, gam)
    rf = BS.right_fronts(rows, b, gam)
    # cone check on genuine orbit
    bad = 0
    for t in range(T + 1):
        P = Ps[t]
        for c in range(y + lf[t], z - rf[t]):
            if P[c] != rows[t][(c - y) % n]:
                bad += 1
    print(f'  cone check on genuine orbit: {bad} mismatches (fronts l_T={lf[T]} r_T={rf[T]})', flush=True)
    assert bad == 0
    # L encoding with genuine left port
    t0 = time.time()
    E, X, AL, BE, HL, info = build_L(b, V, gam, R, foreign=False, g_final=None, trim=trim, solver=solver, rows_bg=rows_bg, require_period=False)
    N = info['N']
    # fix free columns at t=0
    for c in range(R):
        E.add([X[0][c][Ps[0][y - R + c]]])
    for s in range(T):
        P = Ps[s]
        alpha, e = carries(P, b)
        L = len(P)
        E.add([AL[s][0] if alpha[y - R] else -AL[s][0]])
        if gam[s]:
            # hi_(y-R-1) = digit of the sum at mirror position L-1-(y-R-1) (y-R-1 >= 0 here)
            hd = e[L - 1 - (y - R - 1)]
            E.add([HL[s][hd]])
    r, m = BS.solve_and_report(E, f'L-validate seed={seed} trim={trim}', t0)
    assert r
    mism = 0
    for s in range(T + 1):
        for c in range(N):
            vs = BS.letter_of(m, X[s][c])
            if vs != [Ps[s][y - R + c]]:
                mism += 1
    print(f'  L: model letters vs genuine letters: {mism} mismatches over {(T+1)*N} (t,c)', flush=True)
    assert mism == 0
    E.S.delete() if E.S else None
    # determinism: forbid the genuine letter at a random final column (inside variable region)
    E2, X2, AL2, BE2, HL2, info2 = build_L(b, V, gam, R, foreign=False, g_final=None, trim=trim, solver=solver, rows_bg=rows_bg, require_period=False)
    for c in range(R):
        E2.add([X2[0][c][Ps[0][y - R + c]]])
    for s in range(T):
        P = Ps[s]
        alpha, e = carries(P, b)
        L = len(P)
        E2.add([AL2[s][0] if alpha[y - R] else -AL2[s][0]])
        if gam[s]:
            hd = e[L - 1 - (y - R - 1)]
            E2.add([HL2[s][hd]])
    c0 = rnd.randrange(0, R + lf[T])
    E2.add([-X2[T][c0][Ps[T][y - R + c0]]])
    r2 = E2.S.solve()
    print(f'  L: forbid genuine final letter at column {c0}: {"SAT" if r2 else "UNSAT"}', flush=True)
    assert not r2
    E2.S.delete()
    # R encoding with genuine right port
    t0 = time.time()
    V_r = V  # phase 0 at z: need rotation of V with V_r[0] = letter that would continue at z
    # the band ends at z; band coordinate of column z (in phase 0 at y) is (z-y)%n = 0 since z = y + n*Kw, so V phase 0 at z
    E3, X3, AL3, BE3, HL3, info3 = build_R(b, V, gam, Rfree=RW, delta=None, foreign=False, trim=trim, solver=solver, rows_bg=rows_bg, require_period=False)
    Z = info3['Z']; N3 = info3['N']
    # absolute column of window c: z - Z + c
    for c in range(RW):
        E3.add([X3[0][Z + c][Ps[0][z + c]]])
    for s in range(T):
        P = Ps[s]
        alpha, e = carries(P, b)
        L = len(P)
        # beta_x = alpha_(L-x) with x = z + RW (window right edge)
        x = z + RW
        assert x < L // 2 - 1, (x, L)
        E3.add([BE3[s][N3] if alpha[L - x] else -BE3[s][N3]])
    r3, m3 = BS.solve_and_report(E3, f'R-validate seed={seed} trim={trim}', t0)
    assert r3
    mism3 = 0
    for s in range(T + 1):
        for c in range(N3):
            vs = BS.letter_of(m3, X3[s][c])
            if vs != [Ps[s][z - Z + c]]:
                mism3 += 1
    print(f'  R: model letters vs genuine letters: {mism3} mismatches over {(T+1)*N3} (t,c)', flush=True)
    assert mism3 == 0
    E3.S.delete() if E3.S else None
    E4, X4, AL4, BE4, HL4, info4 = build_R(b, V, gam, Rfree=RW, delta=None, foreign=False, trim=trim, solver=solver, rows_bg=rows_bg, require_period=False)
    for c in range(RW):
        E4.add([X4[0][Z + c][Ps[0][z + c]]])
    for s in range(T):
        P = Ps[s]
        alpha, e = carries(P, b)
        L = len(P)
        x = z + RW
        E4.add([BE4[s][N3] if alpha[L - x] else -BE4[s][N3]])
    c0 = rnd.randrange(Z - rf[T], N3)
    E4.add([-X4[T][c0][Ps[T][z - Z + c0]]])
    r4 = E4.S.solve()
    print(f'  R: forbid genuine final letter at column {c0}: {"SAT" if r4 else "UNSAT"}', flush=True)
    assert not r4
    E4.S.delete()
    print('VALIDATE PASS', flush=True)


if __name__ == '__main__':
    global_ENC = None
    ap = argparse.ArgumentParser()
    ap.add_argument('seed', type=int)
    ap.add_argument('--b', type=int, default=10)
    ap.add_argument('--T', type=int, default=40)
    ap.add_argument('--R', type=int, default=12)
    ap.add_argument('--n', type=int, default=3)
    ap.add_argument('--notrim', action='store_true')
    ap.add_argument('--enc', type=int, default=1)
    ap.add_argument('--solver', default='cadical195')
    a = ap.parse_args()
    import builtins
    globals()['ENC'] = a.enc
    run(a.seed, b=a.b, T=a.T, R=a.R, n=a.n, trim=not a.notrim, solver=a.solver)

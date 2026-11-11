#!/usr/bin/env python3
"""r13a: genuine big-integer validation of the seam encoding of seamgen.py (two-sided background window, exact left E rows, exact right V rows).
Builds P = B0 W0^q J V^k C mirror (clock forced to 1000 by the T12 exterior for N <= 12q+40 steps), runs the genuine orbit for N steps,
and checks: the encoder of seamgen (same strip, E rows = W0 rows, V rows under the genuine clock) with the genuine J, without return condition,
reproduces the genuine letters at every (t, c) of the window; and forbidding one genuine final letter is UNSAT.
usage: seamval.py SEED [--N 24] [--Lj 6] [--s 3]"""
import sys, random, argparse, time
import bandsat as BS

B0 = [10, 4, 6, 6, 7, 12, 9, 16, 16, 13, 0, 2, 10, 17, 7, 0, 18, 6, 5, 18, 4, 18, 14, 9, 14, 8, 12, 17, 10, 4, 6, 4, 0, 5]
W0 = [5, 18, 4, 8, 1, 15, 4, 0, 5]


def digits(n, b=10):
    d = []
    while n:
        d.append(n % b)
        n //= b
    return d or [0]


def val(d, b=10):
    n = 0
    for x in reversed(d):
        n = n * b + x
    return n


def pair(n):
    d = digits(n)
    L = len(d)
    return [d[i] + d[L - 1 - i] for i in range(L)]


def make_number(P, rnd):
    L = len(P)
    d = [0] * L
    for i in range(L // 2):
        p = P[i]
        lo = max(0, p - 9)
        hi = min(p, 9)
        x = rnd.randint(lo, hi)
        d[i] = x
        d[L - 1 - i] = p - x
    if L % 2:
        assert P[L // 2] % 2 == 0
        d[L // 2] = P[L // 2] // 2
    if d[L - 1] == 0:
        d[L - 1], d[0] = d[0], d[L - 1]
    n = val(d)
    assert pair(n) == P
    return n


def run(seed, N, Lj, sV):
    rnd = random.Random(seed)
    while True:
        V = [rnd.randrange(19) for _ in range(sV)]
        if any(v != 9 for v in V):
            break
    J = [rnd.randrange(19) for _ in range(Lj)]
    clock0 = [1 if t % 4 == 0 else 0 for t in range(N)]
    Erows0, _, _, _, _ = BS.background(W0, clock0, 10)
    rf0 = BS.right_fronts(Erows0, 10, clock0)
    q = max(N // 12 + 3, (rf0[N] + 30) // 9 + 2)
    k = (3 * N + 60) // sV + 4
    h = [rnd.randrange(19) for _ in range(5)]
    C = h + h[::-1]
    H = B0 + W0 * q + J + V * k
    cJ_abs = len(B0) + 9 * q  # first column of J
    z_abs = cJ_abs + Lj + sV * k
    P0 = H + C + H[::-1]
    n = make_number(P0, rnd)
    Ps = [P0]
    gam = []
    m = n
    for t in range(N):
        m2 = m + val(digits(m)[::-1])
        Pn = pair(m2)
        g = len(Pn) - len(Ps[-1])
        gam.append(g)
        Ps.append(Pn)
        m = m2
    assert gam == [1 if t % 4 == 0 else 0 for t in range(N)], 'clock not 1000: exterior did not force it (N too large for q?)'
    # backgrounds under the genuine clock
    Erows, EAs, EBs, ELs, EHs = BS.background(W0, gam, 10)
    Vrows, VAs, VBs, VLs, VHs = BS.background(V, gam, 10)
    rfE = BS.right_fronts(Erows, 10, gam)
    lfV = BS.left_fronts(Vrows, 10, gam)
    Delta = max(9, sV) + 3
    cJ = rfE[N] + Delta + 2 * 9 + 3
    Nw = cJ + Lj + lfV[N] + Delta + 2 * sV + 3

    def bgl(s, c):
        if c < cJ:
            return Erows[s][(c - cJ) % 9]
        if c >= cJ + Lj:
            return Vrows[s][(c - cJ - Lj) % sV]
        return 0

    def bga(s, c):
        if c < cJ:
            return EAs[s][(c - cJ) % 9]
        if c >= cJ + Lj:
            return VAs[s][(c - cJ - Lj) % sV]
        return 0

    def bgb(s, c):
        if c < cJ:
            return EBs[s][(c - cJ) % 9]
        if c >= cJ + Lj:
            return VBs[s][(c - cJ - Lj) % sV]
        return 0

    A = [max(0, cJ - rfE[s] - Delta) for s in range(N + 1)]
    H_ = [min(Nw, cJ + Lj + lfV[s] + Delta) for s in range(N + 1)]
    # window column c <-> absolute column cJ_abs - cJ + c
    off = cJ_abs - cJ
    # check the genuine columns outside the variable region equal the backgrounds (cone protection)
    bad = 0
    for s in range(N + 1):
        P = Ps[s]
        for c in range(0, Nw):
            if c < A[s] or c >= H_[s]:
                if P[off + c] != bgl(s, c):
                    bad += 1
    print(f'seed={seed} N={N} Lj={Lj} s={sV} V={V} q={q} k={k}: columns outside variable region vs background: {bad} mismatches (rfE={rfE[N]}, lfV={lfV[N]}, window {Nw})', flush=True)
    assert bad == 0
    E = BS.Enc('cadical195')
    X, AL, BE, HL = BS.encode_strip(E, 10, gam, Nw, A, H_, bgl, bga, bgb, left_free=False, right_free=False)
    # initial letters: all variable-region letters fixed to genuine
    for c in range(A[0], H_[0]):
        E.add([X[0][c][Ps[0][off + c]]])
    r = E.S.solve()
    print('  encoding with genuine initial data:', 'SAT' if r else 'UNSAT', f'vars={E.nv} clauses={E.nc}', flush=True)
    assert r
    m3 = set(l for l in E.S.get_model() if l > 0)
    mism = 0
    for s in range(N + 1):
        for c in range(Nw):
            vs = BS.letter_of(m3, X[s][c])
            if vs != [Ps[s][off + c]]:
                mism += 1
    print(f'  model letters vs genuine letters at all (t,c): {mism} mismatches', flush=True)
    assert mism == 0
    # forbid one final letter
    E2 = BS.Enc('cadical195')
    X2, _, _, _ = BS.encode_strip(E2, 10, gam, Nw, A, H_, bgl, bga, bgb, left_free=False, right_free=False)
    for c in range(A[0], H_[0]):
        E2.add([X2[0][c][Ps[0][off + c]]])
    c0 = rnd.randrange(A[N], H_[N])
    E2.add([-X2[N][c0][Ps[N][off + c0]]])
    r2 = E2.S.solve()
    print(f'  forbid genuine letter at final column {c0}: {"SAT" if r2 else "UNSAT"}', flush=True)
    assert not r2
    print('SEAMVAL PASS', flush=True)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('seed', type=int)
    ap.add_argument('--N', type=int, default=24)
    ap.add_argument('--Lj', type=int, default=6)
    ap.add_argument('--s', type=int, default=3)
    a = ap.parse_args()
    run(a.seed, a.N, a.Lj, a.s)

#!/usr/bin/env python3
"""Random test: the cyclic row map phi (used by latenum.cpp / sat_path.py) vs REAL big-integer reverse-and-add on the interior.
For a random palindromic periodic row r (period m, axis alpha): number with n-1 = alpha (mod m) digits, pair word P_i = r[i mod m];
actual step N -> N + rev N, actual overflow gam in {0,1}; interior pair word of the result must equal phi(r, gam)[i mod m]."""
import random, sys
sys.path.insert(0, '.')
from sat_path import phi_rows
from check_lattice_bigint import pairs, tonum, rev_add
def one(b, m, rng, n0=300, margin=70):
    alpha = rng.randrange(m)
    half = (m // 2) + 2
    r = [rng.randrange(0, 2 * b - 1) for _ in range(m)]
    # make palindromic about alpha: r[i] = r[(alpha - i) % m]
    for i in range(m): r[(alpha - i) % m] = r[i]
    if all(v == b - 1 for v in r): return None
    n = n0
    while (n - 1) % m != alpha: n += 1
    P = [r[i % m] for i in range(n)]
    if any(P[i] != P[n - 1 - i] for i in range(n)): return "notpal"
    D = [0] * n
    for i in range(n // 2 + 1):
        j = n - 1 - i
        if i == j:
            if P[i] % 2: return None
            D[i] = P[i] // 2
        else:
            D[i] = P[i] // 2; D[j] = P[i] - P[i] // 2
    if D[-1] == 0: D[-1] = 0
    if any(d >= b or d < 0 for d in D) or D[-1] == 0: return None
    N = tonum(D, b); M = rev_add(N, b)
    n2 = 0; X = M
    while X: n2 += 1; X //= b
    gam = n2 - n
    if gam not in (0, 1): return "gam?"
    pw, nn = pairs(M, b)
    out = phi_rows(r, gam, b)
    if out is None: return None
    pred = out[0]
    bad = sum(1 for i in range(margin, nn - margin) if pw[i] != pred[i % m])
    return bad
rng = random.Random(7)
tot = 0; badtot = 0; byb = {}
for b in (9, 10, 13):
    for _ in range(1500):
        m = rng.choice([1, 2, 3, 4, 5, 6, 8])
        res = one(b, m, rng)
        if res is None: continue
        tot += 1
        if res != 0: badtot += 1; print("BAD", b, m, res)
    print("base", b, "tested so far", tot, "bad", badtot)

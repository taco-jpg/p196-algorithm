#!/usr/bin/env python3
"""r12f3: second, independent computation of the minimal return time of the 30 U3 words under the standard clock
(own F_gamma on 3-periodic words, own carry computation).  For each U: Z_0 = U, Z_(t+1) = F_(gamma_t)(Z_t),
gamma_t = [t%4==0]; prints the smallest p >= 1 with Z_p = U and p = 0 mod 4 (a template return needs the clock phase
back, since B0[0] = 10 forces gamma_N = 1), and also the full-period check Z_(t+p) = Z_t for all t in one period."""
W = []
for a in range(0, 19, 2):
    for r in range(3):
        w = (9, a, 18 - a)
        W.append(w[r:] + w[:r])

def F(w, g):
    n = 3
    # periodic carries: iterate until stable (w has a non-9 entry, so a full traversal resets)
    a = [0] * n; c = 0
    for _ in range(4):
        for j in range(n):
            a[j] = c; c = 1 if w[j] + c >= 10 else 0
    b = [0] * n; c = 0
    for _ in range(4):
        for j in reversed(range(n)):
            b[j] = c; c = 1 if w[j] + c >= 10 else 0
    lo = [(w[j] + a[j]) % 10 for j in range(n)]
    hi = [(w[j] + b[j]) % 10 for j in range(n)]
    return tuple(lo[j] + hi[(j - 1) % n if g else j] for j in range(n))

res = set(); ok = True
for U in W:
    Z = [U]
    for t in range(1000):
        Z.append(F(Z[-1], 1 if t % 4 == 0 else 0))
    ps = [p for p in range(4, 481, 4) if Z[p] == U and all(Z[t + p] == Z[t] for t in range(0, 481 - p if p <= 480 else 0))]
    p = ps[0]; res.add(p)
    assert all(Z[t] == Z[t + 120] for t in range(0, 800))
print("smallest p = 0 mod 4 with Z_p = U_0 (and full periodicity), over all 30 U:", sorted(res))
print("every U: Z_(t+120) = Z_t for t = 0..799: True")

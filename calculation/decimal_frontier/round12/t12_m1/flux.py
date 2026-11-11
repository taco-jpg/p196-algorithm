#!/usr/bin/env python3
"""r12a: linear carry-flux (mod 9 / mod 11) bookkeeping for the folded two-carry law.

Folded column i, row P_t.  alpha_x = low carry entering column x from x-1,
beta_x = high carry entering column x-1 from x, hi_i = (P_i+beta_(i+1)) % 10.
Identity (exact telescoping, 10 = 1 mod 9):
  S_[a,b)(t+1) = 2 S_[a,b)(t) + phi_t(a) - phi_t(b)            (mod 9),
  phi_t(x) = alpha_x - beta_x + gamma_t * hi_(x-1).
Mod 11 with weights (-1)^i:
  gamma=0: Q' = 2Q + psi(a) - psi(b), psi(x) = (-1)^x (alpha_x + beta_x)
  gamma=1: Q' =      psi(a) - psi(b), psi(x) = (-1)^x (alpha_x + P_(x-1) + beta_(x-1))
This script (1) checks both identities on genuine big-integer orbits, (2) computes
the 120-step flux l(x) = sum_t 2^(119-t) phi_t(x) mod 9 for the cyclic W band and
for each of the 30 U3 backgrounds (cut x taken modulo the period).
"""
import sys, random
sys.path.insert(0, __file__.rsplit('/', 1)[0])
sys.set_int_max_str_digits(100000)
from seam_check import B, W, J0, us


def pairs_of(n):
    s = str(n)[::-1]
    d = [int(c) for c in s]
    return [x + y for x, y in zip(d, d[::-1])]


def carries(P, gamma):
    """full (unfolded) symmetric pairword P of length L -> folded alpha, beta, hi."""
    L = len(P)
    c = [0] * (L + 1)
    for i in range(L):
        c[i + 1] = (P[i] + c[i]) // 10
    assert c[L] == gamma
    alpha = c                                   # alpha_x = c_x
    beta = [c[L - x] for x in range(L + 1)]     # beta_x = c_(L-x)
    hi = [(P[i] + beta[i + 1]) % 10 for i in range(L)]
    return alpha, beta, hi


def check_identities(trials=40, seed=3):
    rnd = random.Random(seed)
    bad = cnt = 0
    for tr in range(trials):
        L = rnd.randrange(80, 300)
        n = int("".join(str(rnd.randrange(1 if i == 0 else 0, 10)) for i in range(L)))
        for t in range(30):
            P = pairs_of(n)
            m = n + int(str(n)[::-1])
            g = len(str(m)) - len(str(n))
            al, be, hi = carries(P, g)
            Pn = pairs_of(m)
            h = len(P) // 2
            for _ in range(5):
                a = rnd.randrange(1, h - 2)
                b = rnd.randrange(a + 1, h)
                S0 = sum(P[a:b]); S1 = sum(Pn[a:b])
                phi = lambda x: al[x] - be[x] + (hi[x - 1] if g else 0)
                if (S1 - 2 * S0 - phi(a) + phi(b)) % 9:
                    bad += 1
                Q0 = sum((-1) ** i * P[i] for i in range(a, b))
                Q1 = sum((-1) ** i * Pn[i] for i in range(a, b))
                if g:
                    psi = lambda x: (-1) ** x * (al[x] + P[x - 1] + be[x - 1])
                    if (Q1 - psi(a) + psi(b)) % 11:
                        bad += 1
                else:
                    psi = lambda x: (-1) ** x * (al[x] + be[x])
                    if (Q1 - 2 * Q0 - psi(a) + psi(b)) % 11:
                        bad += 1
                cnt += 1
            n = m
    print("identity checks", cnt, "bad", bad, flush=True)
    return bad == 0


def cyc_rows(U, clock):
    """cyclic background rows; per t: (row, a, bb, hi) with a[i]=alpha_i, bb[i]=beta_(i+1)."""
    V = list(U)
    out = []
    p = len(V)
    for g in clock:
        a = [0] * p
        c = 0
        for _ in range(3):
            for i in range(p):
                a[i] = c
                c = (V[i] + c) // 10
        bb = [0] * p
        cc = 0
        for _ in range(3):
            for i in reversed(range(p)):
                bb[i] = cc
                cc = (V[i] + cc) // 10
        hi = [(V[i] + bb[i]) % 10 for i in range(p)]
        lo = [(V[i] + a[i]) % 10 for i in range(p)]
        out.append((list(V), a, bb, hi))
        V = [lo[i] + (hi[i - 1] if g else hi[i]) for i in range(p)]
    return out, V


def flux_cyclic(U, clock):
    rows, Vend = cyc_rows(U, clock)
    p = len(U)
    res = []
    for x in range(p):  # cut x: between column x-1 and x
        l9 = 0
        for t, g in enumerate(clock):
            V, a, bb, hi = rows[t]
            alpha = a[x % p]
            beta = bb[(x - 1) % p]  # beta_x = carry entering column x-1 from x
            phi = alpha - beta + (hi[(x - 1) % p] if g else 0)
            l9 = (2 * l9 + phi) % 9
        res.append(l9)
    return res, Vend == list(U)


if __name__ == "__main__":
    ok = check_identities()
    clock = [1, 0, 0, 0] * 30
    print("W cyclic flux l9 per cut (x mod 9), returns:", flux_cyclic(W, clock))
    for i, U in enumerate(us()):
        print("U", i, U, "l9 per cut (x mod 3), returns:", flux_cyclic(U, clock))

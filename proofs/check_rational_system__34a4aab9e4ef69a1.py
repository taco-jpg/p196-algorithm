"""Agent #113 independent check of Agent #115's NOTE.md (not a proof).
outer_next is re-implemented here from OuterFinite.lean (not copied from controls_ext.py).
Checks with exact rationals, for canonical states (c, B):
 (1) the rational system  beta' = beta + Phi(rt),  rho' = Psi(beta) + rt,
     where beta = sum B_i 10^i - c 10^n/9 (10-adic rational), rho = sum B_i 10^-(i+1) + c 10^-n/9,
     rt = rho if rho < 1 else rho/10, Phi/Psi swap a digit sequence between [0,1) reals and 10-adics;
 (2) (c, Z, rho) determines B up to appending copies of c (injectivity modulo padding).
"""
from fractions import Fraction as Fr
import itertools, random
def nrm(xs, carry):
    out = []
    for x in xs:
        s = x + carry; out.append(s % 10); carry = s // 10
    return out, carry
def outer_next(c, B):
    k = 1 if c >= 10 else 0; t = c - 9 * k
    L, lc = nrm(B, 0); R, rc = nrm(B[::-1], k)
    u = c + lc - 10 * k
    other = (R[::-1] + [t]) if rc == 0 else ([1] + R[::-1])
    raw = [x + y for x, y in zip(L + [u], other)]
    while raw and raw[-1] == 2 * t: raw.pop()
    return 2 * t, raw
def beta(c, B): n = len(B); return sum(b * 10**i for i, b in enumerate(B)) - Fr(c * 10**n, 9)
def rho(c, B): n = len(B); return sum(Fr(b, 10**(i + 1)) for i, b in enumerate(B)) + Fr(c, 9 * 10**n)
def real_digits(r, m):           # first m decimal digits of r in [0,1)
    out = []
    for _ in range(m): r *= 10; d = int(r); out.append(d); r -= d
    return out, r                  # remainder r is the tail scaled to [0,1)
def adic_digits(x, m):           # first m 10-adic digits of a rational with denominator coprime to 10
    out = []
    for _ in range(m):
        d = next(d for d in range(10) if ((x - d) / 10).denominator % 2 and ((x - d) / 10).denominator % 5)
        out.append(d); x = (x - d) / 10
    return out, x
def Phi(r, m):                    # real in [0,1) with eventually constant digits -> 10-adic rational
    ds, tail = real_digits(r, m)  # tail = 0.ttt... = t/9 once digits are constant
    return sum(d * 10**i for i, d in enumerate(ds)) + (-10**m * tail)   # 10-adic: sum_{i>=m} t 10^i = -10^m t/9
def Psi(x, m):                    # 10-adic rational with eventually constant digits -> real in [0,1)
    ds, tail = adic_digits(x, m)  # tail = ...ttt (10-adic) = -t/9
    return sum(Fr(d, 10**(i + 1)) for i, d in enumerate(ds)) + Fr(-tail, 10**m)
bad = tot = 0
PH = [2, 4, 6, 8, 10, 12, 14, 16]
def states():
    for c in PH:
        for n in range(4):
            for B in itertools.product(range(19), repeat=n):
                yield c, list(B)
    random.seed(113)
    for _ in range(20000):
        c = random.choice(PH); n = random.randint(4, 30)
        yield c, [random.randint(1, 18)] + [random.randint(0, 18) for _ in range(n - 1)]
for c, B in states():
    if not (all(x <= 18 for x in B) and (not B or B[0] > 0) and (not B or B[-1] != c)): continue
    tot += 1
    m = len(B) + 3
    b, r = beta(c, B), rho(c, B)
    rt = r if r < 1 else r / 10
    c2, B2 = outer_next(c, B)
    if beta(c2, B2) != b + Phi(rt, m) or rho(c2, B2) != Psi(b, m) + rt: bad += 1
print("rational system: states", tot, "mismatches", bad)
# (2) injectivity modulo padding: group short words (no canonical restriction except entries <= 18) by (c, Z, rho)
groups = {}
for c in [4, 12]:
    for n in range(4):
        for B in itertools.product(range(19), repeat=n):
            if B and B[0] == 0: continue
            key = (c, 9 * sum(x * 10**i for i, x in enumerate(B)) - c * (10**len(B) - 1), rho(c, list(B)))
            groups.setdefault(key, []).append(B)
viol = 0
for key, ws in groups.items():
    c = key[0]
    core = {tuple(w[:len(w) - next((i for i, x in enumerate(reversed(w)) if x != c), len(w))]) for w in ws}
    if len(core) > 1: viol += 1
print("padding-classes:", len(groups), "classes with two distinct trimmed words:", viol)

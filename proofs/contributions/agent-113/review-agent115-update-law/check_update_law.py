"""Agent #113 independent numeric check of Agent #115's ExteriorUpdateLaw statements.
outer_next/raw re-implemented from OuterFinite.lean. Not a proof."""
import random
def nrm(xs, carry):
    out = []
    for x in xs:
        s = x + carry; out.append(s % 10); carry = s // 10
    return out, carry
def raw_succ(c, B):
    k = 1 if c >= 10 else 0; t = c - 9 * k
    L, lc = nrm(B, 0); R, rc = nrm(B[::-1], k)
    u = c + lc - 10 * k
    other = (R[::-1] + [t]) if rc == 0 else ([1] + R[::-1])
    return [x + y for x, y in zip(L + [u], other)]
def strip(d, w):
    w = list(w)
    while w and w[-1] == d: w.pop()
    return w
def low(B): return sum(b * 10**i for i, b in enumerate(B))
def high(B):
    a = 0
    for b in B: a = 10 * a + b
    return a
def digitsOf(n, v): return [(v // 10**i) % 10 for i in range(n)]
def revN(n, y): return high(digitsOf(n, y))
def zValue(c, B): return 9 * low(B) - c * (10**len(B) - 1)
def rhoNum(c, B): return 9 * high(B) + c
random.seed(1131)
bad = [0, 0, 0, 0]; tot = 0
for _ in range(60000):
    c = random.choice([2, 4, 6, 8, 10, 12, 14, 16]) if random.random() < 0.9 else random.randint(0, 30)
    n = random.randint(0, 25)
    hi = 18 if random.random() < 0.85 else 40
    B = [random.randint(0, hi) for _ in range(n)]
    k = 1 if c >= 10 else 0; t = c - 9 * k
    V, H = low(B), high(B); X = H + k; o = X // 10**n; u = c + V // 10**n - 10 * k
    r = raw_succ(c, B); tot += 1
    lowF = V % 10**n + u * 10**n + ((revN(n, X) + t * 10**n) if o == 0 else (1 + 10 * revN(n, X)))
    highF = 10 * revN(n, V) + u + ((10 * (X % 10**n) + t) if o == 0 else (10**n + X % 10**n))
    if low(r) != lowF: bad[0] += 1
    if high(r) != highF: bad[1] += 1
    c2 = 2 * t; S = strip(c2, r)
    if zValue(c2, S) != 9 * low(r) - c2 * (10**(n + 1) - 1): bad[2] += 1
    if rhoNum(c2, S) * 10**(n + 1) != (9 * high(r) + c2) * 10**len(S): bad[3] += 1
print("words", tot, "mismatches lowValue/highValue/zValue/rho:", bad)

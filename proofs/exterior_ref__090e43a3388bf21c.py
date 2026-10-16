#!/usr/bin/env python3
"""Agent #103 independent exterior map, written from METHOD_AND_PROOF.md (3),(4),(6),(7)
and the suffix trimming of section 6, plus a literal integer validation."""
import random, sys

def N(W, e):
    """Normalize coefficient block W (low to high) with incoming carry e."""
    D = []
    for w in W:
        s = w + e
        D.append(s % 10); e = s // 10
    return D, e

def exterior(c, B):
    k = 1 if c >= 10 else 0
    t = c - 9 * k
    cp = 2 * t
    DB, e0 = N(B, 0)
    u0 = c + e0 - 10 * k
    DRB, gamma = N(B[::-1], k)
    left = DB + [u0]
    right = (DRB[::-1] + [t]) if gamma == 0 else ([1] + DRB[::-1])
    Br = [x + y for x, y in zip(left, right)]
    assert len(Br) == len(B) + 1
    while Br and Br[-1] == cp:
        Br.pop()
    return cp, tuple(Br), gamma

# ---------- literal integer validation ----------
def pairword(n):
    d = [int(x) for x in str(n)[::-1]]  # least significant first
    L = len(d)
    return [d[i] + d[L - 1 - i] for i in range(L)]

def realize(q):
    """Canonical integer with mirrored-sum word q (q symmetric, positive exterior, even middle)."""
    L = len(q); d = [0] * L
    for i in range((L + 1) // 2):
        j = L - 1 - i
        if i == j:
            assert q[i] % 2 == 0; d[i] = q[i] // 2
        else:
            hi = min(9, q[i]); lo = q[i] - hi
            d[j] = hi; d[i] = lo          # most significant digit takes the larger part (positive)
    assert d[-1] > 0
    n = int(''.join(str(x) for x in reversed(d)))
    assert pairword(n) == q, (q, pairword(n))
    return n

def template(c, B, A, C, g, h):
    d = 18 - c
    return list(B) + [c] * g + list(A) + [d] * h + list(C) + [d] * h + list(A)[::-1] + [c] * g + list(B)[::-1]

def random_block(m, first_positive=False):
    b = [random.randint(0, 18) for _ in range(m)]
    if first_positive and m: b[0] = random.randint(1, 18)
    return b

def validate(trials, seed=1):
    random.seed(seed)
    phases = [x for x in range(1, 18) if x != 9]
    for _ in range(trials):
        c = random.choice(phases)
        m = random.randint(0, 7)
        B = random_block(m, True)
        while B and B[-1] == c:   # trimmed source (our domain); keep a positive exterior
            B[-1] = random.randint(1 if len(B) == 1 else 0, 18)
        A = random_block(random.randint(0, 4))
        hc = random.randint(0, 3); Ch = random_block(hc)
        mid = [] if random.random() < 0.5 else [2 * random.randint(0, 9)]
        C = Ch + mid + Ch[::-1]
        g = random.randint(5, 9); h = random.randint(5, 9)
        q = template(c, B, A, C, g, h)
        n = realize(q)
        q2 = pairword(n + int(str(n)[::-1]))
        cp, Bp, gamma = exterior(c, B)
        # the new word must start with B' followed by at least one c' (band survives since g>=5)
        assert q2[:len(Bp)] == list(Bp), (c, B, q2[:12], Bp)
        assert q2[len(Bp)] == cp, (c, B, q2[:12], Bp, cp)
        assert len(q2) == len(q) + gamma
    return trials

if __name__ == '__main__':
    print('validated', validate(int(sys.argv[1]) if len(sys.argv) > 1 else 20000))

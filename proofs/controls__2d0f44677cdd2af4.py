#!/usr/bin/env python3
"""Agent #109 literal-integer controls for identities (5)/(8) of the
complementary-bulk quotient (independent of the Lean source).

For each random template q = Q(c;B,A,C;g,h) with C symmetric (even middle),
coefficients <= 18 and positive exterior, build an ordinary integer n whose
mirrored pair word is q, compute T(n) = n + int(str(n)[::-1]) with Python big
integers, and compare its mirrored pair word with the returned template computed
from formulas (3),(4),(6),(7). Also checks the palindrome criterion.
"""
import json, random, sys

def pair_word(n):
    d = [int(ch) for ch in str(n)[::-1]]          # least significant first
    return [a + b for a, b in zip(d, d[::-1])]

def realize(q):
    """An integer n with pair_word(n) == q (q symmetric, canonical)."""
    L = len(q); d = [0] * L
    for i in range((L + 1) // 2):
        j = L - 1 - i
        if i == j:
            d[i] = q[i] // 2
        else:
            hi = min(9, q[i]); lo = q[i] - hi      # leading digit hi >= 1
            d[j], d[i] = hi, lo                   # d[L-1] is most significant
    n = int(''.join(str(x) for x in reversed(d)))
    assert pair_word(n) == q, (q, n)
    return n

def norm(w, e):
    out = []
    for x in w:
        out.append((x + e) % 10); e = (x + e) // 10
    return out, e

def template(c, B, A, C, g, h):
    d = 18 - c
    return B + [c]*g + A + [d]*h + C + [d]*h + A[::-1] + [c]*g + B[::-1]

def k(x): return 1 if x >= 10 else 0
def t(x): return x - 9*k(x)
def zadd(a, b):
    assert len(a) == len(b); return [x + y for x, y in zip(a, b)]
def pair(w): return zadd(w, w[::-1])

def predicted(c, B, A, C, g, h):
    d = 18 - c
    DB, e0 = norm(B, 0); DA, e1 = norm(A, k(c)); DC, e2 = norm(C, k(d))
    DRA, e3 = norm(A[::-1], k(d)); DRB, gam = norm(B[::-1], k(c))
    u0 = c + e0 - 10*k(c); u1 = d + e1 - 10*k(d)
    u2 = d + e2 - 10*k(d); u3 = c + e3 - 10*k(c)
    digit = (DB + [u0] + [t(c)]*(g-1) + DA + [u1] + [t(d)]*(h-1) + DC + [u2]
             + [t(d)]*(h-1) + DRA + [u3] + [t(c)]*(g-1) + DRB + ([1] if gam else []))
    if gam == 0:
        Br = zadd(DB + [u0], DRB[::-1] + [t(c)])
        Ar = zadd([t(c)] + DA + [u1], [u3] + DRA[::-1] + [t(d)])
        Cr = pair([t(d)] + DC + [u2])
    else:
        Br = zadd(DB + [u0], [1] + DRB[::-1])
        Ar = zadd(DA + [u1], [u3] + DRA[::-1])
        Cr = pair(DC + [u2])
    return digit, template(2*t(c), Br, Ar, Cr, g - 2 + gam, h - 2 + gam), gam

def rand_block(rng, L): return [rng.randint(0, 18) for _ in range(L)]

def rand_sym(rng, L):
    half = [rng.randint(0, 18) for _ in range(L // 2)]
    mid = [2*rng.randint(0, 9)] if L % 2 else []
    return half + mid + half[::-1]

def main(trials=20000, seed=109):
    rng = random.Random(seed)
    phases = [c for c in range(1, 18) if c != 9]
    stats = {"trials": 0, "overflow": 0, "palindromic_next": 0}
    for _ in range(trials):
        c = rng.choice(phases)
        B = rand_block(rng, rng.randint(0, 4))
        if B: B[0] = rng.randint(1, 18)
        A = rand_block(rng, rng.randint(0, 4)); C = rand_sym(rng, rng.randint(0, 5))
        g = rng.randint(2, 7); h = rng.randint(2, 7)
        q = template(c, B, A, C, g, h)
        n = realize(q)
        m = n + int(str(n)[::-1])
        digit, ret, gam = predicted(c, B, A, C, g, h)
        assert [int(ch) for ch in str(m)[::-1]] == digit, ("(5)", c, B, A, C, g, h)
        assert pair_word(m) == ret, ("(8)", c, B, A, C, g, h)
        assert (str(m) == str(m)[::-1]) == (digit == digit[::-1])
        stats["trials"] += 1; stats["overflow"] += gam
        stats["palindromic_next"] += (str(m) == str(m)[::-1])
    stats["seed"] = seed; stats["result"] = "PASS"
    print(json.dumps(stats))

if __name__ == "__main__":
    main(*(int(a) for a in sys.argv[1:]))

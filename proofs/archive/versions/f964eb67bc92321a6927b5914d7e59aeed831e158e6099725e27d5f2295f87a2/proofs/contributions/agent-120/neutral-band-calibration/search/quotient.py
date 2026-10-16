#!/usr/bin/env python3
"""Exact neutral one-band template quotient in base b (exploratory reference implementation).

Pair words are least significant first.  The template is
    Q(B, C, g) = B ++ [n]*g ++ C ++ [n]*g ++ reverse(B),   n = b - 1,
with B the exterior block (B[0] > 0 when nonempty, B[-1] != n after trimming)
and C a symmetric nonempty center (odd length -> even middle, C[0] != n).
`qstep` implements the one-step transition derived in NOTES.md; it returns None
whenever the template hypotheses fail (equal band carries, or a degenerate center).
`validate` compares the formula with literal integer reverse-and-add.
"""
import random, sys

def norm(b, word, c):
    out = []
    for v in word:
        s = v + c
        out.append(s % b)
        c = s // b
    return out, c

def template(b, B, C, g):
    n = b - 1
    return list(B) + [n] * g + list(C) + [n] * g + list(reversed(B))

def qstep(b, B, C):
    """Return (B2, C2, gamma, u, v) with Q(B,C,g) -> Q(B2, C2, g - gamma + u + v), or None."""
    n = b - 1
    B = list(B); C = list(C); s = len(B); m = len(C)
    if m == 0:
        return None
    DB, e1 = norm(b, B, 0)
    x = n * (1 - e1)
    DC, e2 = norm(b, C, e1)
    if e2 == e1:
        return None
    y = n * (1 - e2)
    DR, gam = norm(b, list(reversed(B)), e2)
    if gam == 0:
        Bp = [DB[i] + DR[s - 1 - i] for i in range(s)]
        Cp = [DC[i] + DC[m - 1 - i] for i in range(m)]
    else:
        low = DB + [x]; high = [1] + DR[::-1]
        Bp = [low[i] + high[i] for i in range(s + 1)]
        lowc = DC + [y]; highc = [y] + DC[::-1]
        Cp = [lowc[i] + highc[i] for i in range(m + 1)]
    u = 0
    while Bp and Bp[-1] == n:
        Bp.pop(); u += 1
    if all(c == n for c in Cp):
        return None
    v = 0
    while Cp[0] == n:
        Cp = Cp[1:-1]; v += 1
    return tuple(Bp), tuple(Cp), gam, u, v

def value(b, word):
    v = 0
    for d in reversed(word):
        v = v * b + d
    return v

def digits(b, N):
    out = []
    while N:
        out.append(N % b); N //= b
    return out

def pairs(D):
    return [a + c for a, c in zip(D, reversed(D))]

def literal_next(b, q):
    """Pair word of the integer value(q) (= reverse-and-add of any realization of q)."""
    return pairs(digits(b, value(b, q)))

def is_pal_next(b, q):
    D = digits(b, value(b, q))
    return D == D[::-1]

def validate(b, trials, rng):
    n = b - 1; ok = bad = skipped = 0
    for _ in range(trials):
        s = rng.randint(0, 4); m = rng.randint(1, 6)
        B = [rng.randint(0, 2 * n) for _ in range(s)]
        if s:
            B[0] = rng.randint(1, 2 * n)
            if B[-1] == n:
                continue
        half = [rng.randint(0, 2 * n) for _ in range((m + 1) // 2)]
        C = half + half[: m // 2][::-1]
        if m % 2 and C[m // 2] % 2:
            C[m // 2] -= 1
        if C[0] == n:
            continue
        g = rng.randint(2, 9)
        res = qstep(b, B, C)
        if res is None:
            skipped += 1
            continue
        B2, C2, gam, u, v = res
        q = template(b, B, C, g)
        lit = literal_next(b, q)
        g2 = g - gam + u + v
        if lit == template(b, B2, C2, g2) and not is_pal_next(b, q):
            ok += 1
        else:
            bad += 1
            print('MISMATCH', b, B, C, g, res, lit)
    return ok, bad, skipped

if __name__ == '__main__':
    rng = random.Random(20261015)
    total = [0, 0, 0]
    for b in list(range(2, 21)) + [26, 32]:
        r = validate(b, 3000, rng)
        print('base', b, 'ok', r[0], 'bad', r[1], 'skipped(template breaks)', r[2])
        for i in range(3): total[i] += r[i]
    print('TOTAL ok', total[0], 'bad', total[1], 'skipped', total[2])
    sys.exit(1 if total[1] else 0)

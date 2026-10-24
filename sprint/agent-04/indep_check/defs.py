"""Literal Python transcriptions of the Lean definitions (ActualPrefix.lean, PrefixInverse.lean)."""


# ---- ActualPrefix.lean ----
def lowDigits(s, x):
    if not s:
        return []
    a = s[0]
    return [(a + x) % 10] + lowDigits(s[1:], (a + x) // 10)


def highDigits(s, e):
    if not s:
        return (e, [])
    a = s[0]
    t1, t2 = highDigits(s[1:], e)
    return ((a + t1) // 10, [(a + t1) % 10] + t2)


def zipWith_add(xs, ys):
    return [x + y for x, y in zip(xs, ys)]  # Lean zipWith truncates to shorter


def forwardPrefix(s, e):
    lo = lowDigits(s, 0)
    hi = highDigits(s, e)
    if hi[0] == 0:
        return zipWith_add(lo, hi[1])
    else:
        return zipWith_add(lo, [1] + hi[1])


# ---- PrefixInverse.lean ----
def carry(a, x):
    return (a + x) // 10


def lowDigit(a, x):
    return (a + x) % 10


def noOverflowPred(p, x, y):
    if not p:
        return [[]]
    v, rest = p[0], p[1:]
    out = []
    for a in range(19):
        for z in range(2):
            if carry(a, z) == y and v == lowDigit(a, x) + lowDigit(a, z):
                out += [[a] + t for t in noOverflowPred(rest, carry(a, x), z)]
    return out


def overflowTailPred(p, a, x, y):
    if not p:
        return [[]] if any(carry(a, z) == y for z in range(2)) else []
    v, rest = p[0], p[1:]
    prev = a
    out = []
    for a2 in range(19):
        for z in range(2):
            if carry(prev, z) == y and v == lowDigit(a2, x) + lowDigit(prev, z):
                out += [[a2] + t for t in overflowTailPred(rest, a2, carry(a2, x), z)]
    return out


def overflowFirst(v):
    return v + 9 if v <= 9 else 9


def overflowPred(p):
    if not p:
        return []
    v, rest = p[0], p[1:]
    if 0 < v and v <= 10:
        a = overflowFirst(v)
        return [[a] + t for t in overflowTailPred(rest, a, carry(a, 0), 1)]
    return []


def prefixPredecessors(p):
    return [s for s in noOverflowPred(p, 0, 0) if (s[0] if s else 0) > 0] + overflowPred(p)

"""Reference (slow, literal) Python translations of the Lean definitions used by
the forward abstraction.  Used only to cross-check the fast C implementation.

Lean sources translated here:
  forwardPrefix, lowDigits, highDigits   lean/P196/Agent104P620Witness/ActualPrefix.lean
  noOverflowPred, overflowTailPred,
  overflowFirst, overflowPred,
  prefixPredecessors                      lean/P196/Agent104P620Witness/PrefixInverse.lean
  wordCode                                lean/P196/Agent104P620Witness/PrefixCertificate.lean
"""


def low_digits(s, x):
    out = []
    for a in s:
        out.append((a + x) % 10)
        x = (a + x) // 10
    return out


def high_digits(s, e):
    if not s:
        return (e, [])
    c, tail = high_digits(s[1:], e)
    a = s[0]
    return ((a + c) // 10, [(a + c) % 10] + tail)


def forward_prefix(s, e):
    lo = low_digits(s, 0)
    c, hi = high_digits(s, e)
    if c == 0:
        return [x + y for x, y in zip(lo, hi)]
    return [x + y for x, y in zip(lo, [1] + hi)]


def _carry(a, x):
    return (a + x) // 10


def _low(a, x):
    return (a + x) % 10


def no_overflow_pred(p, x, y):
    if not p:
        return [[]]
    v, rest = p[0], p[1:]
    out = []
    for a in range(19):
        for z in range(2):
            if _carry(a, z) == y and v == _low(a, x) + _low(a, z):
                out += [[a] + t for t in no_overflow_pred(rest, _carry(a, x), z)]
    return out


def overflow_tail_pred(p, a, x, y):
    if not p:
        return [[]] if any(_carry(a, z) == y for z in range(2)) else []
    v, rest = p[0], p[1:]
    out = []
    for a2 in range(19):
        for z in range(2):
            if _carry(a, z) == y and v == _low(a2, x) + _low(a, z):
                out += [[a2] + t for t in overflow_tail_pred(rest, a2, _carry(a2, x), z)]
    return out


def overflow_first(v):
    return v + 9 if v <= 9 else 9


def overflow_pred(p):
    if not p:
        return []
    v, rest = p[0], p[1:]
    if 0 < v <= 10:
        a = overflow_first(v)
        return [[a] + t for t in overflow_tail_pred(rest, a, _carry(a, 0), 1)]
    return []


def prefix_predecessors(p):
    return [s for s in no_overflow_pred(p, 0, 0) if (s[0] if s else 0) > 0] + overflow_pred(p)


def word_code(w):
    c = 1
    for d in w:
        c = 19 * c + d
    return c


def reverse_add(n):
    return n + int(str(n)[::-1])


def orbit(n, t):
    for _ in range(t):
        n = reverse_add(n)
    return n


def column_word(n, k):
    """First k column sums q_0..q_{k-1} (units end) of n."""
    d = [int(c) for c in str(n)[::-1]]
    L = len(d)
    return [d[i] + d[L - 1 - i] for i in range(min(k, L))]

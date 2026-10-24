#!/usr/bin/env python3
"""Reference (slow, literal) implementation of the k-column prefix abstraction.

Mirrors, line by line:
  SevenColumnProjection.lowDigits / highDigits / forwardPrefix   (Agent104P620Witness/ActualPrefix.lean)
  SevenColumn.noOverflowPred / overflowTailPred / overflowPred /
  prefixPredecessors                                           (Agent104P620Witness/PrefixInverse.lean)
  Agent117.unpackWord / unpack                                   (Agent117RemainingCycles/PrefixCycle.lean)

Words are lists of column sums q_0..q_{k-1} (outermost column first), entries 0..18.
"""


def carry(a, x):
    return (a + x) // 10


def low_digit(a, x):
    return (a + x) % 10


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
    return ((s[0] + c) // 10, [(s[0] + c) % 10] + tail)


def forward_prefix(s, e):
    lo = low_digits(s, 0)
    c, hi = high_digits(s, e)
    if c == 0:
        return [a + b for a, b in zip(lo, hi)]
    return [a + b for a, b in zip(lo, [1] + hi)]


def no_overflow_pred(p, x, y):
    if not p:
        return [[]]
    v, rest = p[0], p[1:]
    out = []
    for a in range(19):
        for z in range(2):
            if carry(a, z) == y and v == low_digit(a, x) + low_digit(a, z):
                out += [[a] + t for t in no_overflow_pred(rest, carry(a, x), z)]
    return out


def overflow_tail_pred(p, prev, x, y):
    if not p:
        return [[]] if any(carry(prev, z) == y for z in range(2)) else []
    v, rest = p[0], p[1:]
    out = []
    for a in range(19):
        for z in range(2):
            if carry(prev, z) == y and v == low_digit(a, x) + low_digit(prev, z):
                out += [[a] + t for t in overflow_tail_pred(rest, a, carry(a, x), z)]
    return out


def overflow_first(v):
    return v + 9 if v <= 9 else 9


def overflow_pred(p):
    if not p:
        return []
    v, rest = p[0], p[1:]
    if 0 < v <= 10:
        a = overflow_first(v)
        return [[a] + t for t in overflow_tail_pred(rest, a, carry(a, 0), 1)]
    return []


def prefix_predecessors(p):
    return [s for s in no_overflow_pred(p, 0, 0) if (s[0] if s else 0) > 0] + overflow_pred(p)


def unpack_word(k, m):
    out = []
    for _ in range(k):
        out.append(m % 19)
        m //= 19
    return out


def unpack(k, n):
    return unpack_word(k, n // 2), n % 2


def code(w):
    """Little-endian base-19 code (q_0 is the lowest base-19 digit), same as unpackWord."""
    c = 0
    for a in reversed(w):
        c = 19 * c + a
    return c

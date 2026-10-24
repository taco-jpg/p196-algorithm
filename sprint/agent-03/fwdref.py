#!/usr/bin/env python3
"""Reference (slow, literal) implementation of the k-column prefix abstraction.

Mirrors the Lean definitions:
  SevenColumnProjection.lowDigits / highDigits / forwardPrefix
      (lean/P196/Agent104P620Witness/ActualPrefix.lean)
  SevenColumn.noOverflowPred / overflowTailPred / overflowPred / prefixPredecessors
      (lean/P196/Agent104P620Witness/PrefixInverse.lean)

Self-tests (run `python3 fwdref.py`):
  1. forward relation == converse of the repo's backward relation, exhaustively at k = 2, 3
     over all sources with entries < 19 and positive head;
  2. soundness against actual integers: for random n (lengths k..60) the k-column
     projection of step(n) equals forwardPrefix(projection(n), actual carry c_{L-k}).
"""
import random
import sys


# ---------------------------------------------------------------- forward (ActualPrefix.lean)
def low_digits(s, x):
    out = []
    for a in s:
        out.append((a + x) % 10)
        x = (a + x) // 10
    return out


def high_digits(s, e):
    # carry passed from the end of the list toward its head
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


def overflow_bit(s, e):
    return high_digits(s, e)[0]


# ---------------------------------------------------------------- backward (PrefixInverse.lean)
def carry(a, x):
    return (a + x) // 10


def low_digit(a, x):
    return (a + x) % 10


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


# ---------------------------------------------------------------- actual integers
def digits_lsb(n):
    return [int(ch) for ch in reversed(str(n))]


def project(n, k):
    d = digits_lsb(n)
    L = len(d)
    return [d[i] + d[L - 1 - i] for i in range(min(k, L))]


def inner_carry(n, k):
    """Actual carry into column L-k of n + rev(n) (DecimalDigits.carry q (L-k))."""
    d = digits_lsb(n)
    L = len(d)
    q = [d[i] + d[L - 1 - i] for i in range(L)]
    c = 0
    for i in range(L - k):
        c = (q[i] + c) // 10
    return c


def step(n):
    return n + int(str(n)[::-1])


def words(k):
    """All length-k words with entries < 19 and positive head."""
    if k == 0:
        yield []
        return
    def rec(prefix, m):
        if m == 0:
            yield list(prefix)
            return
        for a in range(19):
            prefix.append(a)
            yield from rec(prefix, m - 1)
            prefix.pop()
    for h in range(1, 19):
        yield from rec([h], k - 1)


def selftest():
    # 1. forward == converse of backward
    for k in (2, 3):
        fwd = set()
        for s in words(k):
            for e in (0, 1):
                fwd.add((tuple(s), tuple(forward_prefix(s, e))))
        bwd = set()
        targets = {p for (_, p) in fwd}
        # every word with entries <= 19 could be a target; enumerate all length-k words with entries < 19
        def all_words(m):
            if m == 0:
                yield []
                return
            for a in range(19):
                for t in all_words(m - 1):
                    yield [a] + t
        for p in all_words(k):
            for s in prefix_predecessors(p):
                bwd.add((tuple(s), tuple(p)))
        assert fwd == bwd, (k, len(fwd), len(bwd), list(fwd - bwd)[:5], list(bwd - fwd)[:5])
        print(f"k={k}: forward relation == converse of prefixPredecessors ({len(fwd)} edges)")
    # 2. soundness against actual integers
    rng = random.Random(196)
    checked = 0
    for _ in range(20000):
        L = rng.randint(2, 60)
        n = rng.randint(10 ** (L - 1), 10 ** L - 1)
        m = step(n)
        for k in range(1, min(L, 12) + 1):
            w = project(n, k)
            e = inner_carry(n, k)
            assert forward_prefix(w, e) == project(m, k), (n, k)
            assert overflow_bit(w, e) == (len(str(m)) - len(str(n))), (n, k)
            checked += 1
    print(f"actual-integer soundness: {checked} (n,k) pairs OK")


if __name__ == "__main__":
    selftest()

#!/usr/bin/env python3
"""Exact ancestry depth of decimal palindromes on full pair-sum words (diagnostic, not a proof).

Pair-sum word of an n-digit integer X (digits a_0..a_{n-1}, units first): s_i = a_i + a_{n-1-i}.
F(s) = pair-sum word of T(X) = X + rev(X); it depends only on s (the seven-column note, eq. (1)).
For a palindrome P whose leading digit is >= 2, every predecessor has pair-sum word equal to the
digit word of P (PalindromeBridge.canonical_last_step), so
    H(P) = 0                      if digits(P) is not an admissible pair word, else
    H(P) = 1 + D(digits(P)),       D(w) = 0 if w has no F-preimage, else 1 + max D(v) over preimages v.
Preimages are found exactly by an outside-in carry transducer for both widths (same width, and one
shorter with an overflow), and every candidate is re-checked by the forward map F.
"""
import sys
from functools import lru_cache
from itertools import product

sys.setrecursionlimit(100000)


def normalize(s):
    out, c = [], 0
    for u in s:
        c, d = divmod(u + c, 10)
        out.append(d)
    if c:
        out.append(c)
    return tuple(out)


def F(s):
    d = normalize(s)
    return tuple(x + y for x, y in zip(d, d[::-1]))


def admissible(s):
    n = len(s)
    return (n > 0 and s[0] > 0 and all(0 <= u <= 18 for u in s) and s == s[::-1]
            and (n % 2 == 0 or s[n // 2] % 2 == 0))


def _preimages_same_width(w):
    """Sources of width len(w) without final overflow. Outside-in over mirror pairs.
    State: (half, x, y): x = carry into the next low position, y = required carry out of the
    next high position."""
    n = len(w)
    m = n // 2
    states = [((), 0, 0)]
    for j in range(m):
        p = w[j]
        if w[n - 1 - j] != p:
            return []
        nxt = []
        for half, x, y in states:
            for s in range(0 if half else 1, 19):
                xx = (s + x) // 10              # carry out of low position j
                for yy in (0, 1):               # carry into high position n-1-j
                    if (s + yy) // 10 != y:
                        continue
                    if (s + x) % 10 + (s + yy) % 10 != p:
                        continue
                    nxt.append((half + (s,), xx, yy))
        states = nxt
    out = []
    for half, x, y in states:
        if n % 2 == 0:
            if x == y:
                out.append(half + half[::-1])
        else:
            for s in range(0, 19, 2):           # even center
                if (s + x) // 10 == y and 2 * ((s + x) % 10) == w[m]:
                    if half or s > 0:
                        out.append(half + (s,) + half[::-1])
    return out


def _preimages_overflow_fast(w):
    """Sources of width L = len(w) - 1 whose addition overflows (c_L = 1, output digit d_L = 1).
    Output pair k = (k, L - k) couples source low position k (value s_k, carry in c_k) with
    source high position L - k (value s_{k-1} by symmetry, carry in c_{L-k}).
    State after step k: (s_0..s_k, x = c_{k+1}, y = c_{L-1-k})."""
    n = len(w)
    L = n - 1
    if L < 1 or w != w[::-1]:
        return []
    if L <= 2:
        return [v for v in _brute_preimages(w) if len(v) == L]
    m = L // 2
    states = []
    for s0 in range(1, 19):                     # output pair 0: d_0 + d_L = s_0 % 10 + 1
        if s0 % 10 + 1 != w[0]:
            continue
        for y in (0, 1):                        # c_{L-1}; position L-1 holds s_0, must emit c_L = 1
            if (s0 + y) // 10 == 1:
                states.append(((s0,), s0 // 10, y))
    for k in range(1, m):
        nxt = []
        for half, x, y in states:
            dhi = (half[k - 1] + y) % 10        # output digit at position L - k
            for sk in range(19):
                if (sk + x) % 10 + dhi != w[k]:
                    continue
                for yy in (0, 1):               # c_{L-1-k}; position L-1-k holds s_k
                    if (sk + yy) // 10 == y:
                        nxt.append((half + (sk,), (sk + x) // 10, yy))
        states = nxt
    out = []
    for half, x, y in states:
        if L % 2 == 0:                          # output middle digit d_m, d_m = (s_{m-1} + c_m) % 10
            if x == y and 2 * ((half[m - 1] + x) % 10) == w[m]:
                out.append(half + half[::-1])
        else:                                   # source center s_m even, output pair (m, m+1)
            for sm in range(0, 19, 2):
                if (sm + x) // 10 == y and (sm + x) % 10 + (half[m - 1] + y) % 10 == w[m]:
                    out.append(half + (sm,) + half[::-1])
    return sorted(set(v for v in out if admissible(v) and F(v) == w))


def preimages(w):
    w = tuple(w)
    out = [v for v in _preimages_same_width(w) if admissible(v) and F(v) == w]
    out += _preimages_overflow_fast(w)
    return sorted(set(out))


@lru_cache(maxsize=None)
def depth(w):
    ps = preimages(w)
    return 0 if not ps else 1 + max(depth(v) for v in ps)


def palindrome_H(digits):
    w = tuple(digits)
    if not admissible(w):
        return 0
    return 1 + depth(w)


def _brute_preimages(w):
    L = len(w)
    out = []
    for n in (L, L - 1):
        if n < 1:
            continue
        for half in product(range(19), repeat=(n + 1) // 2):
            s = half + (half[::-1][1:] if n % 2 else half[::-1])
            if admissible(s) and F(s) == w:
                out.append(s)
    return sorted(set(out))


if __name__ == '__main__':
    import random
    random.seed(1)
    # completeness/soundness test of the transducers against brute force on small widths
    tested = 0
    for n in range(1, 8):
        words = set()
        for half in product(range(19), repeat=(n + 1) // 2):
            s = half + (half[::-1][1:] if n % 2 else half[::-1])
            if admissible(s):
                words.add(F(s))
        words = sorted(words)
        random.shuffle(words)
        for w in words[:400]:
            assert preimages(w) == _brute_preimages(w), (w, preimages(w), _brute_preimages(w))
            tested += 1
    print('transducer == brute force on', tested, 'image words of widths up to 8')

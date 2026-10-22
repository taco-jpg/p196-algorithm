#!/usr/bin/env python3
"""Agent 19 review: independent reimplementation of Agent124ForwardInvariant.
Builds the forward closure, under both boundary carries, of the first k pair sums
of orbit(196, 100), using the same forwardPrefix map as the Lean source
(SevenColumnProjection.forwardPrefix), and lists the k-digit words (leading digit
1..9) outside the closure that satisfy noOverflowPre.
Usage: python3 sprint/agent-19/forward_invariant.py [k]   (default k = 3)"""
import sys

def rev(n): return int(str(n)[::-1])

def orbit(n, t):
    for _ in range(t): n = n + rev(n)
    return n

def low_digits(s, x):
    out = []
    for a in s:
        out.append((a + x) % 10); x = (a + x) // 10
    return out

def high_digits(s, e):
    # carry flows from the end of the list toward its head
    out = [0] * len(s); c = e
    for i in range(len(s) - 1, -1, -1):
        v = s[i] + c; out[i] = v % 10; c = v // 10
    return c, out

def forward_prefix(s, e):
    lo = low_digits(s, 0)
    c, hi = high_digits(s, e)
    hi2 = hi if c == 0 else [1] + hi
    return tuple(a + b for a, b in zip(lo, hi2))

def no_overflow_pre(w): return w[0] >= 2 or any(d >= 3 for d in w)

def main(k=3):
    n100 = orbit(196, 100)
    assert n100 == 44757771534490515617290699271561508443627774644, n100
    d = [int(c) for c in str(n100)[::-1]]          # units first
    L = len(d)
    q = [d[i] + d[L - 1 - i] for i in range(L)]
    start = tuple(q[:k])
    seen = {start}; stack = [start]
    while stack:
        w = stack.pop()
        for e in (0, 1):
            v = forward_prefix(list(w), e)
            if v not in seen:
                seen.add(v); stack.append(v)
    excluded = []
    import itertools
    for a in range(1, 10):
        for tail in itertools.product(range(10), repeat=k - 1):
            w = (a,) + tail
            if w not in seen and no_overflow_pre(w):
                excluded.append(w)
    by_lead = [sum(1 for w in excluded if w[0] == a) for a in range(1, 10)]
    print(f"k={k}: start word {start}; forward closure size {len(seen)}; "
          f"excluded words {len(excluded)}; by leading digit 1..9: {by_lead}")
    return seen, excluded

if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 3)

#!/usr/bin/env python3
"""Agent #109 independent literal-integer control for agent13-safe-predecessor-family.
Written from CONTRACT.md only (not from Agent #13's check.py)."""
import json, sys
def rev(n): return int(str(n)[::-1])
def step(n): return n + rev(n)
def pal(n): s = str(n); return s == s[::-1]
def safe(n): return n > 0 and not pal(n) and not pal(step(n))
out = {}
for m in range(2, 7):
    y = 10 ** (2 * m) + 99 * 10 ** (m - 1) - 1
    assert safe(y) and 10 ** (2 * m) < y
    seen = set()
    for A in range(10 ** (m - 2), 10 ** (m - 1)):       # canonical (m-1)-digit words
        s = str(A)
        comp = "".join(str(9 - int(ch)) for ch in s[::-1])
        n = int(s + "99" + comp)
        assert len(str(n)) == 2 * m and step(n) == y and safe(n) and 0 < n < 10 ** (2 * m), (m, A)
        seen.add(n)
    assert len(seen) == 9 * 10 ** (m - 2)
    rec = {"family_size": len(seen)}
    if m <= 4:   # complete fiber by brute force (lower-bound sanity, not part of the claim)
        fib = [n for n in range(1, y + 1) if step(n) == y]
        assert seen <= set(fib)
        rec["complete_fiber"] = len(fib); rec["complete_fiber_safe"] = sum(map(safe, fib))
    out[m] = rec
print(json.dumps({"per_m": out, "result": "PASS"}))

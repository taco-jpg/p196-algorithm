#!/usr/bin/env python3
"""Agent #109 independent control for agent13-folded-binary-family (from CONTRACT.md):
for r=0..5, k=1..5 and every binary word of length r, build the reflected even pair word
of H=(5,M1..Mr,14,18^k), realize it by random canonical decimals, apply n -> n+reverse(n)
with Python integers, and check the next pair word is the reflection of
R=(11,9^(4r+1),18^k), with n, T(n), T(T(n)) nonpalindromic and 2^r distinct words."""
import itertools, json, random
rng = random.Random(109)
def pal(n): s = str(n); return s == s[::-1]
def T(n): return n + int(str(n)[::-1])
def pairword(n):
    d = [int(c) for c in str(n)[::-1]]; L = len(d)
    return [d[i] + d[L - 1 - i] for i in range(L)]
def realize(q):
    L = len(q); d = [0] * L
    for i in range(L // 2):
        j = L - 1 - i
        lo, hi = max(0, q[i] - 9), min(9, q[i])
        a = rng.randint(max(lo, 1) if i == 0 else lo, hi)   # leading digit d[j] > 0
        d[j], d[i] = a, q[i] - a
    n = int("".join(map(str, reversed(d)))); assert pairword(n) == q; return n
cases = 0
for r in range(0, 6):
    for k in range(1, 6):
        words = set()
        for e in itertools.product([False, True], repeat=r):
            H = [5] + sum(([14, 14, 4, 4] if b else [9, 9, 9, 9] for b in e), []) + [14] + [18] * k
            R = [11] + [9] * (4 * r + 1) + [18] * k
            q = H + H[::-1]; target = R + R[::-1]
            words.add(tuple(q))
            for _ in range(3):
                n = realize(q); m = T(n)
                assert len(str(m)) == len(str(n)), "no overflow expected"
                assert pairword(m) == target
                assert not pal(n) and not pal(m) and not pal(T(m))
                cases += 1
        assert len(words) == 2 ** r
print(json.dumps({"realizations_checked": cases, "r_range": [0, 5], "k_range": [1, 5], "result": "PASS"}))

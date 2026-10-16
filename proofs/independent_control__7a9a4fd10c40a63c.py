#!/usr/bin/env python3
"""Agent #109 independent control for agent11-general-base-first-hit (written from
FIRST_HIT_CONTRACT.md only): for bases b=3..16, random canonical base-b numerals
whose pair coefficients q_i = d_i + d_{L-1-i} satisfy b-1 <= q_i <= b+floor((b-1)/2)-1
and q_0 >= b, compute the actual base-b reverse-and-add orbit with Python integers and
check: first positive palindrome time is 1 iff all q_i = b+1, otherwise 2."""
import json, random
def digits(n, b):
    d = []
    while n: d.append(n % b); n //= b
    return d                    # least significant first
def val(d, b): return sum(x * b**i for i, x in enumerate(d))
def rev(n, b): return val(digits(n, b)[::-1], b)
def pal(n, b): d = digits(n, b); return d == d[::-1]
rng = random.Random(109); stats = {}
for b in range(3, 17):
    h = (b - 1) // 2; lo, hi = b - 1, b + h - 1
    cnt = ones = 0; tries = 0
    while cnt < 400 and tries < 200000:
        tries += 1
        L = rng.randint(1, 12)
        half = (L + 1) // 2
        q = [rng.randint(lo, hi) for _ in range(half)]
        if b + 1 <= hi and rng.random() < 0.15: q = [b + 1] * half
        if q[0] < b: continue
        if L % 2 and q[-1] % 2: continue          # odd width: centre pair 2*d is even
        d = [0] * L; ok = True
        for i in range(half):
            j = L - 1 - i
            if i == j: d[i] = q[i] // 2; continue
            a = rng.randint(max(0, q[i] - (b - 1)), min(b - 1, q[i]))
            d[i], d[j] = q[i] - a, a
        if d[-1] == 0: continue                    # canonical: positive leading digit
        n = val(d, b)
        qq = [d[i] + d[L - 1 - i] for i in range(L)]
        assert all(lo <= x <= hi for x in qq) and qq[0] >= b
        m, t = n, 0
        while True:
            m = m + rev(m, b); t += 1
            if pal(m, b): break
            assert t < 50
        expect = 1 if all(x == b + 1 for x in qq) else 2
        assert t == expect, (b, d, t, expect)
        cnt += 1; ones += (t == 1)
    stats[b] = {"numerals": cnt, "first_hit_1": ones}
print(json.dumps({"per_base": stats, "result": "PASS"}))

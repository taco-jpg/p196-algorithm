#!/usr/bin/env python3
"""Agent #109 literal-integer control for template-step-safety: random admissible
complementary templates with bands g,h >= 2k+2 are realized by canonical integers;
the orbit n -> n + reverse(n) is checked to have no palindrome at times 1..k+1.
Also records how soon a palindrome appears afterwards (observation only)."""
import json, random
rng = random.Random(1090)
def pal(n): s = str(n); return s == s[::-1]
def T(n): return n + int(str(n)[::-1])
def template(c, B, A, C, g, h):
    d = 18 - c
    return B + [c]*g + A + [d]*h + C + [d]*h + A[::-1] + [c]*g + B[::-1]
def realize(q):
    L = len(q); dg = [0]*L
    for i in range((L+1)//2):
        j = L-1-i
        if i == j: dg[i] = q[i]//2; continue
        lo, hi = max(0, q[i]-9), min(9, q[i])
        a = rng.randint(max(lo, 1) if i == 0 else lo, hi)
        dg[j], dg[i] = a, q[i]-a
    return int("".join(map(str, reversed(dg))))
phases = [c for c in range(1, 18) if c != 9]
n_checked = steps_checked = 0; later_hits = 0
for _ in range(3000):
    c = rng.choice(phases)
    B = [rng.randint(0, 18) for _ in range(rng.randint(0, 4))]
    if B: B[0] = rng.randint(1, 18)
    A = [rng.randint(0, 18) for _ in range(rng.randint(0, 4))]
    hh = [rng.randint(0, 18) for _ in range(rng.randint(0, 3))]
    C = hh + ([2*rng.randint(0, 9)] if rng.random() < .5 else []) + hh[::-1]
    k = rng.randint(0, 10)
    g = 2*k + 2 + rng.randint(0, 3); h = 2*k + 2 + rng.randint(0, 3)
    m = realize(template(c, B, A, C, g, h))
    for i in range(1, k + 2):
        m = T(m); assert not pal(m), (c, B, A, C, g, h, k, i)
        steps_checked += 1
    for _ in range(30):
        m = T(m)
        if pal(m): later_hits += 1; break
    n_checked += 1
print(json.dumps({"templates": n_checked, "safe_steps_checked": steps_checked,
                  "later_palindrome_within_30_more_steps": later_hits, "result": "PASS"}))

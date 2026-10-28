#!/usr/bin/env python3
"""abs1.py -- variant test: ONE absorbing outer band.  P = B ++ a^g ++ rev B  (a absorbing, a != 9) in base 10.
Plain big-int reverse-and-add, no model assumptions.  Report which (B,a) keep the template form (|B_t|<=LB, a_t^g_t band) for >=S steps."""
import sys, itertools, collections
LB = int(sys.argv[1]); maxlenB = int(sys.argv[2]); S = int(sys.argv[3]); G0 = int(sys.argv[4])
LOOPVALS = [0, 18, 6, 12, 2, 4, 8, 16, 14, 10]
def pairs_of(n):
    s = str(n)[::-1]
    d = [int(ch) for ch in s]
    L = len(d)
    return [d[i] + d[L - 1 - i] for i in range(L)]
def parse(P):
    n = len(P); m = P[n // 2]
    i = n // 2
    while i > 0 and P[i - 1] == m: i -= 1
    s = i
    if s > LB: return None
    # band must cover P[s:n-s]
    if any(P[j] != m for j in range(s, n - s)): return None
    return s, m, n - 2 * s
def val(P):
    x = 0
    for v in reversed(P): x = x * 10 + v
    return x
best = collections.Counter()
for lb in range(1, maxlenB + 1):
    for B in itertools.product(range(19), repeat=lb):
        if B[0] == 0: continue
        for a in LOOPVALS:
            P = list(B) + [a] * G0 + list(B)[::-1]
            X = val(P); steps = 0
            while steps < S:
                P2 = pairs_of(X)
                r = parse(P2)
                if r is None: break
                steps += 1
                X = val(P2)
            best[(B, a)] = steps
            if steps >= S: print('SURVIVOR', B, a, steps, flush=True)
mx = sorted(best.items(), key=lambda kv: -kv[1])[:10]
print('top survivors', mx)

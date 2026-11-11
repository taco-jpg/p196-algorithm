#!/usr/bin/env python3
"""r12f3: independent checks of the column-0 clock lemma (rootcycles.py part 1).
(1) GENUINE ARITHMETIC: for random positive integers n (length 2..400) compute with Python big integers
    P0 = first digit + last digit, b = carry into the top digit column of n + reverse(n) (schoolbook, LSD first),
    gamma = [len(n + reverse(n)) > len(n)], and P0' of n + reverse(n); compare with the table
    gamma = [P0 + b >= 10], P0' = 2*P0 + b (gamma = 0), P0' = (P0 mod 10) + 1 (gamma = 1).
    Also every (P0, b) pair with P0 in 1..18 is hit by construction (targeted numbers).
(2) POTENTIAL: pi(P) = 3 - floor(log2 P); check 4*gamma - 1 >= pi(P') - pi(P) for all 36 (P0, b) with P0 in 1..18,
    and list the tight pairs.
(3) DP (finite consistency check, not needed by the proof): for every N = 4..2400 (N = 0 mod 4) the number of state
    sequences 10 -> ... -> 10 of length N in the column-0 automaton with exactly N/4 overflows is 1 (the standard
    one) and none has fewer than N/4 overflows."""
import random
random.seed(20261108)


def table(P, b):
    g = 1 if P + b >= 10 else 0
    return ((P % 10) + 1 if g else (P % 10) + ((P + b) % 10)), g


def genuine(n):
    s = str(n); L = len(s); d = [int(ch) for ch in reversed(s)]          # LSD first
    P = [d[i] + d[L - 1 - i] for i in range(L)]
    c = 0
    for i in range(L - 1):                                               # carries up to the top column
        c = (P[i] + c) // 10
    b = c                                                                # carry INTO column L-1
    m = n + int(s[::-1]); t = str(m)
    g = len(t) - L
    P0n = int(t[0]) + int(t[-1])
    return d[0] + d[L - 1], b, g, P0n


bad = 0; hits = set(); N = 0
for _ in range(200000):
    L = random.randint(2, 400)
    n = random.randint(10 ** (L - 1), 10 ** L - 1)
    P0, b, g, P0n = genuine(n)
    hits.add((P0, b)); N += 1
    if (P0n, g) != table(P0, b):
        bad += 1
# targeted: every (P0, b), P0 = 1..18: leading digit a, trailing e with a+e = P0; second pair forces the carry b
for P0 in range(1, 19):
    for b in (0, 1):
        for a in range(1, 10):
            e = P0 - a
            if not 0 <= e <= 9:
                continue
            for _ in range(20):
                L = random.randint(4, 60)
                mid = [random.randint(0, 9) for _ in range(L - 4)]
                # digits MSD first: a, x, mid..., y, e ; pair 1 = x + y; carry into the top column comes from column L-2
                # (pair x+y plus the carry from below): choose x + y = 9 + b + 10*0 extremes to force it
                if b == 1:
                    x, y = 9, 9
                else:
                    x, y = 0, 0
                n = int(''.join(map(str, [a, x] + mid + [y, e])))
                P0g, bg, g, P0n = genuine(n)
                if bg != b:
                    continue
                hits.add((P0g, bg)); N += 1
                if (P0n, g) != table(P0g, bg):
                    bad += 1
print(f"(1) genuine checks: {N} integers, mismatches {bad}, (P0,b) pairs hit {len(hits)} of 36:",
      sorted(set((P, b) for P in range(1, 19) for b in (0, 1)) - hits) or "all")
pi = lambda P: 3 - (P.bit_length() - 1)
viol = []; tight = []
for P in range(1, 19):
    for b in (0, 1):
        Q, g = table(P, b)
        assert 1 <= Q <= 18
        w = 4 * g - 1
        if w < pi(Q) - pi(P):
            viol.append((P, b))
        if w == pi(Q) - pi(P):
            tight.append((P, b, Q, g))
print("(2) potential violations:", viol, "; tight (P,b,P',gamma):", tight)
ok_tight = all(g == 0 for (P, b, Q, g) in tight if P != 10) and (10, 0, 1, 1) in tight
print("    tight overflow edges only from P=10 (10->1):", ok_tight)
from collections import defaultdict
dp = {(10, 0): 1}; res = []
for t in range(1, 2401):
    nd = defaultdict(int)
    for (P, c), v in dp.items():
        for Q, g in set(table(P, b) for b in (0, 1)):
            nd[(Q, c + g)] += v
    dp = nd
    if t % 4 == 0:
        k = t // 4
        fewer = sum(v for (P, c), v in dp.items() if P == 10 and c < k)
        exact = dp.get((10, k), 0)
        res.append((t, exact, fewer))
badN = [r for r in res if r[1] != 1 or r[2] != 0]
print(f"(3) DP N = 4..2400: walks 10->10 with exactly N/4 overflows always 1 and none with fewer: {not badN}", badN[:5])
print("PASS" if bad == 0 and not viol and ok_tight and not badN and len(hits) == 36 else "FAIL")

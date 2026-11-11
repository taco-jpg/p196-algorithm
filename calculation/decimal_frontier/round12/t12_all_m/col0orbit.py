#!/usr/bin/env python3
"""r12f3: orbit-level check of Lemma K on GENUINE reverse-and-add orbits with NON-standard clocks (consistency check).
Templates P(q,k) with small q (q = 0..3, so the root is disturbed after 12q+40 steps and the clock deviates), random
U, J, C; 1500 steps of n -> n + reverse(n) with Python big integers.  At every time N with P_0(N) = 10 (first+last
digit = 10) check: overflows in [0,N) >= N/4, with equality iff the clock was (1000)^(N/4) on [0,N)."""
import sys, random
sys.path.insert(0, __file__.rsplit('/', 1)[0])
import mdefect as md
rnd = random.Random(7); WORDS = md.us(); checks = 0; eq = 0; bad = 0; nonstd = 0
for trial in range(40):
    q = rnd.randrange(0, 4); U = WORDS[rnd.randrange(30)]
    J = [rnd.randrange(19) for _ in range(rnd.randrange(0, 20))]
    h = [rnd.randrange(19) for _ in range(rnd.randrange(1, 4))]; C = h + h[::-1]
    H = list(md.B0) + list(md.W0) * q + J + list(U) * 60
    n = md.realize(H + C + H[::-1]); L = len(str(n)); cnt = 0; std = True
    for t in range(1500):
        s = str(n)
        if t > 0 and int(s[0]) + int(s[-1]) == 10:
            checks += 1
            if 4 * cnt < t: bad += 1
            if 4 * cnt == t:
                eq += 1
                if not std: bad += 1
            elif std and t % 4 == 0: bad += 1      # standard clock so far and t = 0 mod 4 must give equality
        m = n + int(s[::-1]); g = len(str(m)) - L
        if g != (1 if t % 4 == 0 else 0): std = False
        cnt += g; L += g; n = m
    nonstd += (not std)
print(f"orbits 40 (q = 0..3), orbits with a non-standard clock: {nonstd}, times with P0 = 10 checked: {checks}, "
      f"equality cases {eq}, violations {bad}:", "PASS" if bad == 0 else "FAIL")

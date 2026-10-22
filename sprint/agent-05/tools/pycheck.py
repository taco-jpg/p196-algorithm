"""Independent brute-force check (Python big ints, no class reduction, no memo).
For every seed 1..N-1: iterate while the iterate has <= D digits; record every
palindrome hit at t >= 1; output per-4-digit-prefix max t with smallest seed."""
import sys
N, D = int(sys.argv[1]), int(sys.argv[2])
best = {}
for A in range(1, N):
    x = A; t = 0
    while True:
        x = x + int(str(x)[::-1]); t += 1
        s = str(x)
        if len(s) > D: break
        if s == s[::-1] and len(s) >= 4:
            p = s[:4]
            if t > best.get(p, (-1,))[0]: best[p] = (t, A)
for p in sorted(best): print(p, best[p][0], best[p][1])

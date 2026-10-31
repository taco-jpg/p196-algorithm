#!/usr/bin/env python3
"""Big-integer replay of a claimed periodic centre (exact cycle reported by kink6).
usage: replay_kink.py lat K t j par w0 w1 ... w{K-1} [periods]
Builds a genuine decimal number whose lower-half pair word is exterior+lattice below c and the window [c, c+K) on top
(h = c+K, n parity = par, lattice row = t), runs plain N -> N + reverse(N) with Python integers, and checks at every step
that (i) the number is not a palindrome, (ii) the lattice below h-K is intact, (iii) the top-K window returns."""
import sys
from klib import *

def digits_from_pair(P):
    n = len(P); d = [0] * n
    for i in range(n // 2):
        x = P[i]; d[i] = min(x, 9); d[n - 1 - i] = x - d[i]
    if n % 2:
        assert P[n // 2] % 2 == 0, 'middle cell must be even'
        d[n // 2] = P[n // 2] // 2
    return d

name = sys.argv[1]; K = int(sys.argv[2]); t0, j, par = map(int, sys.argv[3:6])
win = list(map(int, sys.argv[6:6 + K])); periods = int(sys.argv[6 + K]) if len(sys.argv) > 6 + K else 5
lat = load(name)
c = lat.nB + 5 * lat.m + j + 10 * lat.m
h = c + K; n = 2 * h - par
P = full_from_lower(lat.row(t0, c) + win, n)
d = digits_from_pair(P)
if d[-1] == 0: print('leading digit 0 in this realisation; adjust'); sys.exit(1)
N = int(''.join(map(str, d[::-1])))
start = None; seen = {}
T = 72 * 40 if lat.p == 12 else 80 * 40
for s in range(T * 0 + 4000):
    st = str(N)
    if st == st[::-1]: print('PALINDROME at step', s); sys.exit(1)
    dig = [int(ch) for ch in st[::-1]]; n = len(dig); h = (n + 1) // 2
    Pw = [dig[i] + dig[n - 1 - i] for i in range(n)]
    t = (t0 + s) % lat.p
    low_ok = all(Pw[x] == lat.cell(t, x) for x in range(h - K))
    if not low_ok: print('lattice broken at step', s); sys.exit(1)
    key = (t, (h - K - lat.nB) % lat.m, n % 2, tuple(Pw[h - K:h]))
    if key in seen:
        print(f'window returned: step {s} equals step {seen[key]} (period {s - seen[key]}); all checks passed so far')
        break
    seen[key] = s
    N = N + int(st[::-1])
else:
    print('no return within horizon')

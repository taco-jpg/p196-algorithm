#!/usr/bin/env python3
"""Independent check of a self-mirror lattice against REAL big-integer reverse-and-add.
Build N_0 with pair word P_i = rows[0][i mod m] (palindromic: need n-1 = alpha mod m), run p steps of N -> N + rev(N),
and compare the interior pair word with rows[t][(i) mod m] (positions anchored at the low end)."""
import sys, json
def pairs(N, b):
    ds = []
    while N: ds.append(N % b); N //= b
    n = len(ds); return [ds[i] + ds[n - 1 - i] for i in range(n)], n
def tonum(ds, b):
    v = 0
    for d in reversed(ds): v = v * b + d
    return v
def rev_add(N, b):
    ds = []; M = N
    while M: ds.append(M % b); M //= b
    R = tonum(list(reversed(ds)), b)  # reverse digits
    return N + R
def check(b, g, rows, alpha, n0=400, margin=60):
    p = len(rows); m = len(rows[0])
    # n0 with (n-1) % m == alpha
    n = n0
    while (n - 1) % m != alpha % m: n += 1
    P = [rows[0][i % m] for i in range(n)]
    for i in range(n): assert P[i] == P[n - 1 - i], "not palindromic at %d" % i
    D = [0] * n
    for i in range(n // 2 + 1):
        j = n - 1 - i
        if i == j: assert P[i] % 2 == 0 or P[i] <= 9; D[i] = P[i] // 2 if P[i] % 2 == 0 else P[i] // 2  # middle: 2*D = P
        else:
            D[i] = P[i] // 2; D[j] = P[i] - P[i] // 2
    assert all(0 <= d < b for d in D) and D[-1] > 0
    N = tonum(D, b); bad = 0
    for t in range(p):
        pw, nn = pairs(N, b)
        # compare interior with rows[t]
        lo, hi = margin, nn - margin
        for i in range(lo, hi):
            if pw[i] != rows[t][i % m]: bad += 1
        # check the overflow stream
        N = rev_add(N, b)
        n2 = 0; M = N
        while M: n2 += 1; M //= b
        if n2 - nn != g[t]: return ("gam mismatch at t=%d" % t, bad)
    return ("OK", bad)
if __name__ == "__main__":
    b = int(sys.argv[1]); g = [int(c) for c in sys.argv[2]]; rows = json.loads(sys.argv[3]); alpha = int(sys.argv[4])
    print(check(b, g, rows, alpha))

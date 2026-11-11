#!/usr/bin/env python3
"""Depth 0 check by plain big-number addition: can the all-lattice word (no defect at all, lattice right up to the
middle) be an orbit?  For every phase (t,j,par) build the pair word L(t,x), x<h, with h = nB + j + 6m, n = 2h-par, add
the reversal with genuine integer arithmetic and test whether the result is again the all-lattice word of the next
phase.  A depth-0 centre would need this to hold at all phases of one phase orbit."""
import sys

def load(fn):
    tk = open(fn).read().split()
    b, tp, nB, m = map(int, tk[:4])
    clk = list(map(int, tk[4:4 + tp]))
    v = list(map(int, tk[4 + tp:]))
    Bt = [v[t * nB:(t + 1) * nB] for t in range(tp)]
    v = v[tp * nB:]
    W = [v[t * m:(t + 1) * m] for t in range(tp)]
    return b, tp, nB, m, clk, Bt, W

for name in sys.argv[1:]:
    b, tp, nB, m, clk, Bt, W = load(name)
    L = lambda t, x: Bt[t][x] if x < nB else W[t][(x - nB) % m]
    oks = {}
    odd_top = 0
    for t in range(tp):
        for j in range(m):
            for par in range(2):
                h = nB + j + 6 * m
                n = 2 * h - par
                P = [L(t, x) for x in range(h)]
                if par == 1 and P[h - 1] % 2:
                    oks[(t, j, par)] = False  # the middle cell of an odd word is even: not a word at all
                    odd_top += 1
                    continue
                d = [0] * n
                for x in range(h - par):
                    v = min(P[x], b - 1)
                    d[x] = v
                    d[n - 1 - x] = P[x] - v
                if par == 1:
                    d[h - 1] = P[h - 1] // 2
                res = []
                c = 0
                for i in range(n):
                    s = d[i] + d[n - 1 - i] + c
                    res.append(s % b)
                    c = int(s >= b)
                if c:
                    res.append(c)
                n2 = len(res)
                h2 = (n2 + 1) // 2
                Q = [res[x] + res[n2 - 1 - x] for x in range(h2)]
                t2 = (t + 1) % tp
                oks[(t, j, par)] = (c == clk[t]) and all(Q[x] == L(t2, x) for x in range(h2))
    # phase orbits
    seen = set()
    print(name, 'phases', len(oks), 'phases with odd middle cell', odd_top, 'phases where the all-lattice word maps to all-lattice:', sum(oks.values()))
    for (t, j, par) in sorted(oks):
        if (t, j, par) in seen:
            continue
        cur = (t, j, par)
        good = tot = 0
        while cur not in seen:
            seen.add(cur)
            tot += 1
            good += oks[cur]
            tt, jj, pp = cur
            g = clk[tt]
            dh = int(g == 1 and pp == 0)
            cur = ((tt + 1) % tp, (jj + dh) % m, (pp + g) % 2)
        print('  orbit from', (t, j, par), 'length', tot, 'good steps', good, '=> depth-0 centre possible' if good == tot else '=> no depth-0 centre')

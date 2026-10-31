#!/usr/bin/env python3
"""Exact centre window (top cell = middle of the number) restricted to the relaxation's cyclic set.
Every kink whose lattice reaches up to h-K at all times is an exact periodic orbit of the K-window at the top;
its states lie in Cyc(K) of the relaxation (frame c = h-K), so cycles of the exact (deterministic) map inside
Cyc(K) are all such kinks.
usage: exact_small.py lat cycfile K [validate N]"""
import sys, random
from klib import *

def exact_inputs(lat, t, c, n, win):
    K = len(win)
    a = [bulk_up_carry(lat, t, c)]
    for v in win: a.append((v + a[-1]) // 10)
    Din = a[K] if n % 2 == 0 else a[K - 1]
    ghost = (win[K - 1] + Din) % 10
    return Din, ghost

def exact_step(lat, t, c, n, win):
    Din, ghost = exact_inputs(lat, t, c, n, win)
    return window_step(lat, t, c, n, win, Din, ghost)

if __name__ == '__main__':
    name, fn, K = sys.argv[1], sys.argv[2], int(sys.argv[3])
    lat = load(name); base = lat.nB + 5 * lat.m
    if len(sys.argv) > 4 and sys.argv[4] == 'validate':
        N = int(sys.argv[5]); rng = random.Random(3); bad = 0; cnt = 0; okc = 0
        for _ in range(N):
            t = rng.randrange(lat.p); j = rng.randrange(lat.m); par = rng.randrange(2)
            c = base + j + lat.m * rng.randrange(1, 4); h = c + K; n = 2 * h - par
            win = [lat.cell(t, c + i) if rng.random() < 0.5 else rng.randrange(19) for i in range(K)]
            if n % 2 == 1 and win[-1] % 2: win[-1] -= 1
            low = lat.row(t, c) + win
            Pf = full_from_lower(low, n)
            P2, gam = pairword_step(Pf)
            if gam != lat.g[t]: continue
            new, ok = exact_step(lat, t, c, n, win)
            dh = (len(P2) + 1) // 2 - h
            real = P2[c + dh:c + dh + K]
            real_ok = all(P2[x] == lat.cell(t + 1, x) for x in range(c + dh))
            cnt += 1; okc += ok
            if new != real or ok != real_ok: bad += 1
        print(f'exact centre window vs genuine: {cnt} cases, {bad} mismatches, lattice-intact {okc}')
        sys.exit()
    S = set()
    for line in open(fn):
        a = list(map(int, line.split())); S.add(((a[1], a[2], a[3]), tuple(a[4:])))
    succ = {}
    for (ph, w) in S:
        t, j, par = ph; c = base + j; n = 2 * (c + K) - par
        new, ok = exact_step(lat, t, c, n, list(w))
        g = lat.g[t]; dh = 1 if (g == 1 and par == 0) else 0
        ph2 = ((t + 1) % lat.p, (j + dh) % lat.m, (par + g) % 2)
        v2 = (ph2, tuple(new))
        if ok and v2 in S: succ[(ph, w)] = v2
    # cycles of the functional graph
    color = {}; cycles = []
    for v in succ:
        if v in color: continue
        path = []; x = v
        while x in succ and x not in color:
            color[x] = 'grey'; path.append(x); x = succ[x]
        if x in color and color[x] == 'grey':
            cycles.append(path[path.index(x):])
        for y in path: color[y] = 'black'
    print(f'{name} K={K}: |Cyc|={len(S)}, exact successors inside Cyc: {len(succ)}, exact cycles: {len(cycles)}')
    for cyc in cycles[:5]:
        alllat = all(w == tuple(lat.cell(ph[0], base + ph[1] + i) for i in range(K)) for ph, w in cyc)
        print('  cycle length', len(cyc), 'all-lattice' if alllat else 'NON-LATTICE', cyc[0])

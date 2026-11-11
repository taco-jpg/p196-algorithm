#!/usr/bin/env python3
"""r12g2 symcheck2.py -- plain-integer (Python big int) checks of the structural facts used by the kfwd scope argument:
 (1) bulk complement identity W[t+tau][j+sig] == 18 - W[t][j] and the clock under t -> t+tau;
 (2) rec1 bulk == rec0 bulk shifted by (dt, dj), same exterior length, same clock;
 (3) phase orbits and how Phi permutes them;
 (4) fold map by PLAIN INTEGERS (M = sum P_x 10^x, digits of M, new pair word) on random states:
     F(Phi s) == Phi F(s) (complement) and F_rec1(s) == F_rec0(shifted s) (isomorphism).
usage: symcheck2.py ROWSDIR nsamp seed"""
import sys, random
D, NS, SEED = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
def load(fn):
    tok = open(fn).read().split(); it = iter(tok)
    p, nB, m = int(next(it)), int(next(it)), int(next(it)); g = [int(next(it)) for _ in range(p)]
    B = [[int(next(it)) for _ in range(nB)] for _ in range(p)]; W = [[int(next(it)) for _ in range(m)] for _ in range(p)]
    return dict(p=p, nB=nB, m=m, g=g, B=B, W=W)
def cell(L, t, x):
    t %= L['p']; return L['B'][t][x] if x < L['nB'] else L['W'][t][(x - L['nB']) % L['m']]
def nextph(L, t, j, par):
    g = L['g'][t]; dh = 1 if (g == 1 and par == 0) else 0
    return (t + 1) % L['p'], (j + dh) % L['m'], (par + g) % 2
def orbits(L):
    seen = {}; orbs = []
    for t in range(L['p']):
        for j in range(L['m']):
            for par in range(2):
                if (t, j, par) in seen: continue
                o = []; s = (t, j, par)
                while s not in seen: seen[s] = len(orbs); o.append(s); s = nextph(L, *s)
                orbs.append(o)
    return orbs, seen
def fold_int(L, t, j, par, w, q=3):
    """exact fold step by plain integers; returns new state or None (lattice broken / clock violated)"""
    K = len(w); c = L['nB'] + j + q * L['m']; h = c + K; n = 2 * h - par
    low = [cell(L, t, x) for x in range(c)] + list(w)
    P = low + low[:n - h][::-1]
    M = sum(v * 10 ** x for x, v in enumerate(P))          # = N_t + rev(N_t)
    s = str(M)[::-1]; n2 = len(s)
    if n2 - n != L['g'][t]: return None
    d = [int(ch) for ch in s]; h2 = (n2 + 1) // 2; c2 = h2 - K
    P2 = [d[x] + d[n2 - 1 - x] for x in range(h2)]
    t1 = (t + 1) % L['p']
    if any(P2[x] != cell(L, t1, x) for x in range(c2)): return None
    t2, j2, p2 = nextph(L, t, j, par)
    assert c2 == c + (1 if (L['g'][t] == 1 and par == 0) else 0)
    return (t2, j2, p2, tuple(P2[c2:c2 + K]))
R = random.Random(SEED)
L0, L1, L2 = load(f'{D}/rec0.rows'), load(f'{D}/rec1.rows'), load(f'{D}/rec2.rows')
for name, L, syms in (('rec0', L0, [(2, 5), (6, 15)]), ('rec1', L1, [(2, 5), (6, 15)]), ('rec2', L2, [(4, 24)])):
    p, m = L['p'], L['m']
    for tau, sig in syms:
        bad = sum(1 for t in range(p) for j in range(m) if L['W'][(t + tau) % p][(j + sig) % m] != 18 - L['W'][t][j])
        badg = sum(1 for t in range(p) if L['g'][(t + tau) % p] != L['g'][t])
        print(f'(1) {name}: bulk complement identity (tau,sigma)=({tau},{sig}): mismatches {bad}, clock mismatches {badg}')
for dt, dj in ((6, 5), (2, 15)):
    bad = sum(1 for t in range(8) for j in range(20) if L1['W'][t][j] != L0['W'][(t + dt) % 8][(j + dj) % 20])
    print(f'(2) rec1 bulk == rec0 bulk shifted by ({dt},{dj}): mismatches {bad}; nB {L0["nB"]} {L1["nB"]}; clock equal {L0["g"] == L1["g"]}')
for name, L, (tau, sig), reps in (('rec0', L0, (2, 5), [(1, 5, 1)]), ('rec1', L1, (2, 5), []), ('rec2', L2, (4, 24), [(5, 18, 1), (7, 18, 1)])):
    orbs, idx = orbits(L)
    perm = [idx[((o[0][0] + tau) % L['p'], (o[0][1] + sig) % L['m'], o[0][2])] for o in orbs]
    ok = all(idx[((s[0] + tau) % L['p'], (s[1] + sig) % L['m'], s[2])] == perm[i] for i, o in enumerate(orbs) for s in o)
    covered = set()
    for r in reps:
        k = idx[r]
        for _ in range(4): covered.add(k); k = perm[k]
    print(f'(3) {name}: {len(orbs)} phase orbits of lengths {[len(o) for o in orbs]}; Phi maps orbit i -> {perm} (orbit-wise consistent: {ok});'
          f' orbits reached from the start phases {reps} under Phi^k: {sorted(covered)}')
for name, L, (tau, sig) in (('rec0', L0, (2, 5)), ('rec2', L2, (4, 24))):
    nb = na = 0
    for _ in range(NS):
        K = R.randint(6, 26); t = R.randrange(L['p']); j = R.randrange(L['m']); par = R.randrange(2)
        c = L['nB'] + j + 3 * L['m']
        w = [R.randrange(19) if R.random() < 0.3 else cell(L, t, c + i) for i in range(K)]
        if par == 1 and w[-1] % 2: w[-1] ^= 1
        a = fold_int(L, t, j, par, w); b = fold_int(L, (t + tau) % L['p'], (j + sig) % L['m'], par, [18 - v for v in w])
        if (a is None) != (b is None): nb += 1; continue
        if a is None: continue
        na += 1
        if b != ((a[0] + tau) % L['p'], (a[1] + sig) % L['m'], a[2], tuple(18 - v for v in a[3])): nb += 1
    print(f'(4a) {name}: plain-integer fold map commutes with Phi=({tau},{sig},18-w): {NS} samples ({na} alive), mismatches {nb}')
nb = na = 0
for _ in range(NS):
    K = R.randint(6, 26); t = R.randrange(8); j = R.randrange(20); par = R.randrange(2)
    c = L1['nB'] + j + 3 * L1['m']
    w = [R.randrange(19) if R.random() < 0.3 else cell(L1, t, c + i) for i in range(K)]
    if par == 1 and w[-1] % 2: w[-1] ^= 1
    a = fold_int(L1, t, j, par, w); b = fold_int(L0, (t + 6) % 8, (j + 5) % 20, par, w)
    if (a is None) != (b is None): nb += 1; continue
    if a is None: continue
    na += 1
    if b != ((a[0] + 6) % 8, (a[1] + 5) % 20, a[2], a[3]): nb += 1
print(f'(4b) plain-integer fold map: rec1 state (t,j) behaves exactly as rec0 state (t+6,j+5): {NS} samples ({na} alive), mismatches {nb}')

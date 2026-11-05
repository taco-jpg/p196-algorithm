"""Check: the K-head transition trans(x,h) of khead4.cpp / repo py/khead_family.py is the restriction of the exact
exterior map Phi (mirror1000.step = neutral_band_search.nextB with e2 = 1-e1, trimmed) to the lowest K coefficients,
with h = the backward carry arriving at position K-1 from above, after padding B with 9s (neutral band) to width > K."""
import random
from mirror1000 import step, N12_0
import neutral_band_search as nb
b = 10
def trans(x, h):
    K = len(x); H = [0]*(K+1); H[K] = h
    for i in range(K-1, -1, -1): H[i] = (x[i]+H[i+1])//b
    g = H[0]; L = [0]*(K+1)
    for i in range(K): L[i+1] = (x[i]+L[i])//b
    y = []
    for i in range(K):
        part = (1 if i == 0 else (x[i-1]+H[i]) % b) if g else (x[i]+H[i+1]) % b
        y.append((x[i]+L[i]) % b + part)
    return y, g
def backcarry(B, K):
    """backward carry d_K arriving at position K-1 (Lemma 1: d_n = 1-e1, d_i = floor((B_i + d_{i+1})/b))"""
    d = 1 - nb.e1(b, B)
    for i in range(len(B)-1, K-1, -1): d = (B[i]+d)//b
    return d
bad = 0; tot = 0
W = [[int(v) for v in l.split(',')] for l in open('n12_wit.txt')]
samples = list(W)
for _ in range(30000):
    n = random.randint(2, 30); B = [random.randint(1, 18)] + [random.randint(0, 18) for _ in range(n-1)]
    while len(B) > 1 and B[-1] == 9: B.pop()
    samples.append(B)
for B in samples:
    B2, g, _ = step(B)
    for K in range(1, len(B)+1):
        y, gg = trans(B[:K], backcarry(B, K))
        Bp = B2 + [9]*(K+2)
        tot += 1
        if gg != g or y != Bp[:K]: bad += 1
print('K-head trans vs exact map: checked', tot, 'mismatches', bad)
# padded widths: K beyond the width of B (band positions 9)
bad2 = tot2 = 0
for B in samples:
    B2, g, _ = step(B)
    Bp = B + [9]*12; B2p = B2 + [9]*14
    for K in range(1, len(B)+12):
        y, gg = trans(Bp[:K], backcarry(Bp, K)); tot2 += 1
        if gg != g or y != B2p[:K]: bad2 += 1
print('padded (K up to width+11): checked', tot2, 'mismatches', bad2)

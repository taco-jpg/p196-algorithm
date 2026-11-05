#!/usr/bin/env python3
"""Independent Python reference for cen2 (klib.pairword_step): T^(80K)(P(q0,C)) vs P(q0+K,C) for every centre of length L
(or every stride-th); prints RESULT/HIST in cen2's format (fields: centres returns clockdev lenerr guardfail maxprefix argmax).
usage: ref2.py REC L q0 K [stride]"""
import os, sys
from collections import Counter
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'repo/calculation/decimal_frontier/lattice_kinks/edge_relaxation'))
from klib import load_rec, pairword_step
rec, Lc, q0, K = map(int, sys.argv[1:5]); stride = int(sys.argv[5]) if len(sys.argv) > 5 else 1
lat = load_rec(rec); B, W, g = lat.B, lat.W, lat.g; nB, m = lat.nB, lat.m
def P(q, C):
    hh = B[0] + W[0]*q; return hh + C + hh[::-1]
h, odd = Lc//2, Lc % 2
total = 19**h * (10 if odd else 1)
st = Counter(); hist = Counter(); best = (-1, 0)
for idx in range(0, total, stride):
    r = idx; mid = None
    if odd: mid = 2*(r % 10); r //= 10
    half = []
    for _ in range(h): half.append(r % 19); r //= 19
    half = half[::-1]
    C = half + ([mid] if odd else []) + half[::-1]
    a = P(q0, C); clk = guard = True
    for t in range(80*K):
        if a[:nB+m] != B[t % 8] + W[t % 8]: guard = False
        a, gam = pairword_step(a)
        if gam != g[t % 8]: clk = False
    tg = P(q0+K, C); pre = 0
    while pre < min(len(a), len(tg)) and a[pre] == tg[pre]: pre += 1
    st['n'] += 1; st['ret'] += a == tg; st['clk'] += not clk; st['len'] += len(a) != len(tg); st['guard'] += not guard
    hist[pre] += 1
    if pre > best[0]: best = (pre, idx)
print(f"RESULT rec{rec} L={Lc} q0={q0} K={K} stride={stride} centres={st['n']} returns={st['ret']} clockdev={st['clk']} lenerr={st['len']} guardfail={st['guard']} maxprefix={best[0]} argmax_idx={best[1]}")
print('HIST' + ''.join(f' {k}:{hist[k]}' for k in sorted(hist)))

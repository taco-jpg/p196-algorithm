#!/usr/bin/env python3
"""Python reference (klib.pairword_step) for centre.cpp: per-centre 'D idx prefix clockok len guardok'.
usage: ref.py REC L q0 [stride]"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../../calculation/decimal_frontier/lattice_kinks/edge_relaxation'))
from klib import load_rec, pairword_step
rec, Lc, q0 = map(int, sys.argv[1:4]); stride = int(sys.argv[4]) if len(sys.argv) > 4 else 1
lat = load_rec(rec); B, W, g = lat.B, lat.W, lat.g
def P(q, C):
    hh = B[0] + W[0]*q; return hh + C + hh[::-1]
h, odd = Lc//2, Lc % 2
total = 19**h * (10 if odd else 1)
for idx in range(0, total, stride):
    r = idx; mid = None
    if odd: mid = 2*(r % 10); r //= 10
    half = []
    for _ in range(h): half.append(r % 19); r //= 19
    half = half[::-1]
    C = half + ([mid] if odd else []) + half[::-1]
    a = P(q0, C); clk = guard = True
    for t in range(80):
        if a[:59] != B[t % 8] + W[t % 8]: guard = False
        a, gam = pairword_step(a)
        if gam != g[t % 8]: clk = False
    tg = P(q0+1, C); pre = 0
    while pre < min(len(a), len(tg)) and a[pre] == tg[pre]: pre += 1
    print('D', idx, pre, int(clk), len(a), int(guard))

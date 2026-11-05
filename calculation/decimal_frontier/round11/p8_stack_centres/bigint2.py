#!/usr/bin/env python3
"""Literal decimal big-integer control (bigint.py generalised): canonical seed of P(q0,C), NP*80K genuine N+rev(N)
additions; pairword of every state == klib.pairword_step evolution; no palindrome; after each block of 80K steps
report the matching prefix against P(q0+jK,C) and whether it is an exact return.
usage: bigint2.py REC L q0 K NP idx [idx...]"""
import os, sys
if hasattr(sys, "set_int_max_str_digits"): sys.set_int_max_str_digits(0)
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'repo/calculation/decimal_frontier/lattice_kinks/edge_relaxation'))
from klib import load_rec, pairword_step
rec, Lc, q0, K, NP = map(int, sys.argv[1:6]); lat = load_rec(rec)
def centre(idx):
    h, odd = Lc//2, Lc % 2; r = idx; mid = None
    if odd: mid = 2*(r % 10); r //= 10
    half = []
    for _ in range(h): half.append(r % 19); r //= 19
    half = half[::-1]; return half + ([mid] if odd else []) + half[::-1]
def seed(P):
    n = len(P); d = [0]*n
    for i in range((n+1)//2):
        j = n-1-i
        if i == j: d[i] = P[i]//2
        else: lo = min(9, P[i]); d[j] = lo; d[i] = P[i]-lo
    assert d[0] != 0; return int(''.join(map(str, d)))
def pw(N):
    s = str(N); n = len(s); return [int(s[i]) + int(s[n-1-i]) for i in range(n)]
def Pq(q, C):
    hh = lat.B[0] + lat.W[0]*q; return hh + C + hh[::-1]
for idx in map(int, sys.argv[6:]):
    C = centre(idx); P = Pq(q0, C); N = seed(P); assert pw(N) == P
    out = []
    for j in range(1, NP+1):
        for t in range(80*K):
            P, _ = pairword_step(P); N = N + int(str(N)[::-1])
            assert pw(N) == P, (idx, j, t); s = str(N); assert s != s[::-1], 'PALINDROME'
        tgt = Pq(q0 + j*K, C)
        pre = next((i for i in range(min(len(P), len(tgt))) if P[i] != tgt[i]), min(len(P), len(tgt)))
        out.append(f'{pre}{"=RET" if P == tgt else ""}')
    print(f'rec{rec} L{Lc} q0={q0} K={K} idx {idx} C={C}: {NP*80*K} bigint additions == pairword, no palindrome; prefix per period {out}')

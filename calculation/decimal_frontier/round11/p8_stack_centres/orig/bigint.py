#!/usr/bin/env python3
"""Independent literal-decimal big-integer control: canonical seed of P(5,C), 80 genuine N+rev(N) additions,
pairword of every state compared with klib.pairword_step evolution; no palindrome along the way.
usage: bigint.py REC L idx [idx...]   (idx: centre index as in centre.cpp)"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../../calculation/decimal_frontier/lattice_kinks/edge_relaxation'))
from klib import load_rec, pairword_step
rec, Lc = int(sys.argv[1]), int(sys.argv[2]); lat = load_rec(rec)
def centre(idx):
    h, odd = Lc//2, Lc % 2; r = idx; mid = None
    if odd: mid = 2*(r % 10); r //= 10
    half = []
    for _ in range(h): half.append(r % 19); r //= 19
    half = half[::-1]; return half + ([mid] if odd else []) + half[::-1]
def seed(P):  # digits most-significant first: coefficient P[i] = d[i] + d[n-1-i]
    n = len(P); d = [0]*n
    for i in range((n+1)//2):
        j = n-1-i
        if i == j: d[i] = P[i]//2
        else: lo = min(9, P[i]); d[j] = lo; d[i] = P[i]-lo
    assert d[0] != 0; return int(''.join(map(str, d)))
def pw(N):
    s = str(N); n = len(s); return [int(s[i]) + int(s[n-1-i]) for i in range(n)]
for idx in map(int, sys.argv[3:]):
    C = centre(idx); hh = lat.B[0] + lat.W[0]*5; P = hh + C + hh[::-1]
    N = seed(P); assert pw(N) == P
    for t in range(80):
        P, _ = pairword_step(P); N = N + int(str(N)[::-1])
        assert pw(N) == P, (idx, t); s = str(N); assert s != s[::-1]
    hh6 = lat.B[0] + lat.W[0]*6; tgt = hh6 + C + hh6[::-1]
    pre = next((i for i in range(min(len(P), len(tgt))) if P[i] != tgt[i]), min(len(P), len(tgt)))
    print(f'rec{rec} L{Lc} idx {idx} C={C}: 80 bigint additions == pairword, no palindrome, prefix {pre}, return={P==tgt}')

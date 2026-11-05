#!/usr/bin/env python3
"""ref2.py for an arbitrary cen2 table (rec0/rec1/stk*): independent Python reference using klib.pairword_step.
Prints RESULT/HIST in cen2 field names for direct diffing.  usage: ref2gen.py TBL L q0 K"""
import os, sys
from collections import Counter
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "repo/calculation/decimal_frontier/lattice_kinks/edge_relaxation"))
from klib import pairword_step
tbl, Lc, q0, K = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
v = list(map(int, open(tbl).read().split())); p, nB, m = v[:3]; g = v[3:3+p]; o = 3+p
B = [v[o+t*nB:o+(t+1)*nB] for t in range(p)]; o += p*nB; W = [v[o+t*m:o+(t+1)*m] for t in range(p)]
def P(q, C): hh = B[0] + W[0]*q; return hh + C + hh[::-1]
h, odd = Lc//2, Lc % 2; total = 19**h * (10 if odd else 1)
st = Counter(); hist = Counter(); best = (-1, 0)
for idx in range(total):
    r = idx; mid = None
    if odd: mid = 2*(r % 10); r //= 10
    half = []
    for _ in range(h): half.append(r % 19); r //= 19
    half = half[::-1]; C = half + ([mid] if odd else []) + half[::-1]
    a = P(q0, C); clk = True
    for t in range(80*K):
        a, gam = pairword_step(a)
        if gam != g[t % p]: clk = False
    tg = P(q0+K, C); pre = 0
    while pre < min(len(a), len(tg)) and a[pre] == tg[pre]: pre += 1
    st["n"] += 1; st["ret"] += a == tg; st["clk"] += not clk; st["len"] += len(a) != len(tg); hist[pre] += 1
    if pre > best[0]: best = (pre, idx)
print(f"RESULT tbl={tbl} L={Lc} q0={q0} K={K} centres={st['n']} returns={st['ret']} clockdev={st['clk']} lenerr={st['len']} maxprefix={best[0]} argmax_idx={best[1]}")
print("HIST" + "".join(f" {k}:{hist[k]}" for k in sorted(hist)))

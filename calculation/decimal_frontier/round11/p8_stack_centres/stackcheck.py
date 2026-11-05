#!/usr/bin/env python3
"""Direct check of the cap replacement J (B1 -> S(s) = B2 W48^s B1[11:]) along genuine pairword evolution:
for random legal centres C (|C| = 4..16), W20 count r, s W48 blocks: T^t(Stack(s,r,C)) == J_t(T^t(P1(r,C))) for t = 0..80
(J_t replaces the B1_t cap by S_t at both ends), and the 80-step return test gives the same answer and the same
matching length measured from the centre side.  usage: stackcheck.py"""
import os, sys, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'repo/calculation/decimal_frontier/lattice_kinks/edge_relaxation'))
from klib import load_rec, pairword_step
r1, r2 = load_rec(1), load_rec(2); p = 8
B1, W20, B2, W48 = r1.B, r1.W, r2.B, r2.W; nB = 39
rng = random.Random(11)
def cen(Lc):
    h = [rng.randrange(19) for _ in range(Lc//2)]
    return h + ([2*rng.randrange(10)] if Lc % 2 else []) + h[::-1]
tot = bad = 0
for s in (0, 1, 2, 3, 5):
    S = [B2[t] + W48[t]*s + B1[t][11:] for t in range(p)]; nS = len(S[0])
    for r in (4, 5, 6):
        badr = 0
        for k in range(40):
            C = cen(rng.randrange(4, 17))
            a = B1[0] + W20[0]*r; a = a + C + a[::-1]
            b = S[0] + W20[0]*r; b = b + C + b[::-1]
            ok = True
            for t in range(81):
                if not (a[:nB] == B1[t % p] and a[-nB:] == B1[t % p][::-1] and b == S[t % p] + a[nB:-nB] + S[t % p][::-1]):
                    ok = False; break
                if t == 80: break
                a, ga = pairword_step(a); b, gb = pairword_step(b)
                if ga != gb: ok = False; break
            tot += 1; bad += not ok; badr += not ok
        print(f's={s} r={r}: 40 random centres, J-equivariance over 80 genuine steps fails for {badr}')
print(f'total {tot}, failures {bad}')

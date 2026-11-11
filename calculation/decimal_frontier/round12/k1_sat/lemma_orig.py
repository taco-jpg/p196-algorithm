#!/usr/bin/env python3
"""Applicability of the R03A1 / N10 / Agent1P8Ref80 argument to a p8 record (rec0 or rec1).
(1) phase words B_t,W_t from klib.load_rec, checked against genuine pairword_step;
(2) symbolic one-step insertion equivariance T(I_t P) = I_{t+1}(T P) (N10 generalised; formal centre tokens);
(3) universal two-inlet 81-state shield: minimal q0 for which every t<=80 keeps B_t W_t.
Usage: python3 lemma.py REC"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "repo/calculation/decimal_frontier/lattice_kinks/edge_relaxation"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../lattice_kinks/edge_relaxation'))   # repository layout
from klib import load_rec, pairword_step
rec = int(sys.argv[1]); L = load_rec(rec)
p, nB, m = L.p, L.nB, L.m
B = [L.B[t] for t in range(p)]; W = [L.W[t] for t in range(p)]
print(f'rec{rec}: p={p} nB={nB} m={m} g={L.g}')
# (1) genuine bulk check, as agent-N10/build_phase.py
half = B[0] + W[0]*20; P = half + half[::-1]; ov = []
for t in range(16):
    assert P[:nB] == B[t % p] and P[nB:nB+m] == W[t % p], t
    for i in range(nB, nB + 15*m): assert P[i] == W[t % p][(i-nB) % m], (t, i)
    P, gam = pairword_step(P); ov.append(gam)
assert ov == L.g*2, ov
print('PASS (1) 16 genuine steps reproduce B_t,W_t; clock', ov[:8])
def norm(a, c):
    d = []
    for x in a:
        v = x + c; d.append(v % 10); c = v // 10
    return d, c
def word(t, r, u, M):
    b, w = B[t], W[t]
    lo, c = norm(b + w*r, 0)
    hi, g = norm((w*r)[::-1] + b[::-1], u)
    d = [(x, ()) for x in lo] + [(0, (i,)) for i in range(M)] + [(x, ()) for x in hi]
    if g: d.append((g, ()))
    return d, c, g
def pairs(d):
    return [(d[i][0] + d[-1-i][0], tuple(sorted(d[i][1] + d[-1-i][1]))) for i in range(len(d))]
# (2)
tests = 0
for t in range(p):
    w, b = W[t], B[t]
    assert norm(w, 0)[1] == norm(w, 1)[1], ('W not absorbing', t)
    assert norm(w[::-1], 0)[1] == norm(w[::-1], 1)[1], ('rev W not absorbing', t)
    assert norm(b, 0)[1] == norm(w, 0)[1], ('B carry not steady', t)
    # stronger block facts used by the fixed-point factorisation: normalized W block identical for both carry-ins
    for r in (1, 2, 3, 4):
        for u in (0, 1):
            for M in (0, 1, 2, 3, 4, 5, 7, 11, 17, 24):
                a, cin, g = word(t, r, u, M)
                plus, cin1, g1 = word(t, r+1, u, M)
                assert cin == cin1 and g == g1, (t, r, u, M, 'carry')
                pa, pb = pairs(a), pairs(plus)
                nxt = [(x, ()) for x in W[(t+1) % p]]
                target = pa[:nB] + nxt + pa[nB:-nB] + nxt[::-1] + pa[-nB:]
                assert pb == target, (t, r, u, M, 'symbolic mismatch')
                assert g == L.g[t], (t, r, u, M, 'clock')
                tests += 1
print(f'PASS (2) symbolic insertion equivariance: {tests} cases (8 phases x r=1..4 x u=0,1 x 10 formal centre lengths);'
      f' insertion = literal {m}-coefficient block after the {nB}-site cap, injective')
# absorbing carries per phase
print('    W carry-out fwd', [norm(W[t],0)[1] for t in range(p)], 'rev', [norm(W[t][::-1],0)[1] for t in range(p)])
# (3)
def step(prefix):
    k = len(prefix); low, carry = norm(prefix, 0); outs = []
    for inc in (0, 1):
        high = [0]*k; c = inc
        for i in range(k-1, -1, -1):
            v = prefix[i] + c; high[i] = v % 10; c = v // 10
        out = [low[0]+1] + [low[i]+high[i-1] for i in range(1, k)] if c else [low[i]+high[i] for i in range(k)]
        outs.append((c, out))
    if outs[0][0] != outs[1][0]: return None, []
    a, b2 = outs[0][1], outs[1][1]
    mm = next((i for i in range(k) if a[i] != b2[i]), k)
    return outs[0][0], a[:mm]
def shield(q, Cmin=4, H=80):
    pr = B[0] + W[0]*q; n = 2*len(pr) + Cmin; k0 = len(pr)
    for t in range(H+1):
        if not (len(pr) + 2 <= n//2): return False, t, 'midpoint'
        if pr[:nB+m] != B[t % p] + W[t % p]: return False, t, f'root (prefix {len(pr)})'
        if t == H: return True, t, f'prefix {k0}->{len(pr)}'
        g, pr = step(pr)
        if g != L.g[t % p]: return False, t, 'clock'
        n += g
for q in range(1, 9):
    print(f'    shield q={q}:', shield(q))
q0 = next(q for q in range(1, 20) if shield(q)[0])
print(f'PASS (3) minimal universal-shield q0 = {q0}')
odd = [sum(x % 2 for x in B[t]) for t in range(p)]
assert min(odd) > 0
print('PASS (4) odd coefficient count in every B_t:', odd, '-> every shielded state nonpalindromic')

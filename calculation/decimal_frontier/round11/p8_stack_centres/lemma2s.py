#!/usr/bin/env python3
"""r11a: iff thresholds for longer return periods and for the rec2->rec1 stacked exterior.
(A) universal two-inlet shield over H = 80, 160, 240 steps for rec0/rec1 (same step() as p8_centre_exhaust/lemma.py):
    minimal q0(H) such that every state T^t(P(q,C)), t < H, keeps the root B_t W_t for ANY interior (both inner carries).
(B) stacked cap S_t(s) = B2_t W48_t^s B1_t[11:] (PRO-R03-e, #481) in place of B1_t:
    (B1) symbolic cap-replacement equivariance T(J_t P) = J_{t+1}(T P) (formal centre tokens, both centre carry-outs,
         r = 1..4 W20 blocks) -- same finite kernel as lemma.py (2), with J_t: B1_t -> S_t(s) at both ends;
    (B2) symbolic W20 insertion equivariance for the stacked cap (lemma.py (2) with B := S_t(s));
    (B3) universal shield of the stacked word S(s) W20^r: minimal r for H = 80, 160, 240.
usage: lemma2s.py  (part B only, s = 9..16; extends lemma2.log s = 0..8)"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'repo/calculation/decimal_frontier/lattice_kinks/edge_relaxation'))
from klib import load_rec

def norm(a, c):
    d = []
    for x in a:
        v = x + c; d.append(v % 10); c = v // 10
    return d, c

def make(cap, W, g):
    p = len(g); nB = len(cap[0]); m = len(W[0])
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
    def shield(q, H, Cmin=4):
        pr = cap[0] + W[0]*q; n = 2*len(pr) + Cmin; k0 = len(pr)
        for t in range(H+1):
            if not (len(pr) + 2 <= n//2): return False, t, 'midpoint'
            if pr[:nB+m] != cap[t % p] + W[t % p]: return False, t, f'root (prefix {len(pr)})'
            if t == H: return True, t, f'prefix {k0}->{len(pr)}'
            gg, pr = step(pr)
            if gg != g[t % p]: return False, t, 'clock'
            n += gg
    return shield

def word(b, w, r, u, M):
    lo, c = norm(b + w*r, 0)
    hi, gg = norm((w*r)[::-1] + b[::-1], u)
    d = [(x, ()) for x in lo] + [(0, (i,)) for i in range(M)] + [(x, ()) for x in hi]
    if gg: d.append((gg, ()))
    return d, c, gg

def pairs(d):
    return [(d[i][0] + d[-1-i][0], tuple(sorted(d[i][1] + d[-1-i][1]))) for i in range(len(d))]

Ms = (0, 1, 2, 3, 4, 5, 7, 11, 17, 24)
print('== (B) stacked cap S_t(s) = B2_t W48_t^s B1_t[11:] over rec1 bulk')
r1, r2 = load_rec(1), load_rec(2); p = 8
assert r1.g == r2.g
B1, W20, B2, W48 = r1.B, r1.W, r2.B, r2.W
assert all(B2[t] == B1[t][:11] and B1[t][11:17] == W48[t][:6] for t in range(p))
for s in range(9, 17):
    S = [B2[t] + W48[t]*s + B1[t][11:] for t in range(p)]
    nS = len(S[0]); nB = len(B1[0])
    # (B1) cap replacement and (B2) insertion, finite symbolic kernel
    nrep = nins = 0
    for t in range(p):
        w = W20[t]; nxtS = [(x, ()) for x in S[(t+1) % p]]; nxtB = [(x, ()) for x in B1[(t+1) % p]]
        nxtW = [(x, ()) for x in W20[(t+1) % p]]
        assert norm(S[t], 0)[1] == norm(w, 0)[1] == norm(B1[t], 0)[1], ('cap carry not steady', s, t)
        for r in (1, 2, 3, 4):
            for u in (0, 1):
                for M in Ms:
                    a, ca, ga = word(B1[t], w, r, u, M)
                    b, cb, gb = word(S[t], w, r, u, M)
                    assert ca == cb and ga == gb == r1.g[t], (s, t, r, u, M, 'carry/clock')
                    pa, pb = pairs(a), pairs(b)
                    assert pa[:nB] == nxtB and pa[-nB:] == nxtB[::-1], (s, t, 'rec1 cap not lattice')
                    assert pb == nxtS + pa[nB:-nB] + nxtS[::-1], (s, t, r, u, M, 'replacement mismatch')
                    nrep += 1
                    c2, cc, gc = word(S[t], w, r+1, u, M)
                    pc = pairs(c2)
                    assert cc == cb and gc == gb
                    assert pc == pb[:nS] + nxtW + pb[nS:-nS] + nxtW[::-1] + pb[-nS:], (s, t, r, u, M, 'insertion mismatch')
                    nins += 1
    sh = make(S, W20, r1.g)
    thr = {}
    for H in (80, 160, 240):
        res = {r: sh(r, H) for r in range(0, 30)}
        r0 = min(r for r in res if res[r][0]); thr[H] = (r0, all(res[r][0] for r in range(r0, 30)), res[r0][2], res[r0-1] if r0 > 0 else None)
    print(f's={s} |S|={nS}: replacement {nrep}/{nrep} PASS, insertion {nins}/{nins} PASS; shield r0: ' +
          '; '.join(f'H={H}: r0={v[0]} (all above {v[1]}, {v[2]}; r0-1 -> {v[3]})' for H, v in thr.items()))

#!/usr/bin/env python3
"""CP-SAT search for a time-periodic centre ("kink") of a periodic-band exterior in base 10.
usage: kink_sat.py rec_index W M T offset_lo offset_hi timelimit   (single worker)"""
import sys, time
sys.path.insert(0, '/home/claude/research/w3_formats/code')
from ortools.sat.python import cp_model
from scc_to_tmpl import parse
from kink import fwd_window
b = 10

def lattice_data(rec):
    p = rec['p']; P = rec['path']; C = rec['cyc']
    nB = len(P); m = len(C)
    gam = [int(ch) for ch in rec['g']]
    Bt = [[P[k][t] for k in range(nB)] for t in range(p)]
    Wt = [[C[j][t] for j in range(m)] for t in range(p)]
    cup = []
    for t in range(p):
        word = Bt[t] + Wt[t] * 12
        c = 0; carries = []
        for x, d in enumerate(word):
            carries.append(c)       # carry INTO position x
            c = 1 if d + c >= b else 0
        # steady: residues r = (x-nB) mod m, take from last block
        tab = [None] * m
        for x in range(nB + m * 8, nB + m * 9):
            tab[(x - nB) % m] = carries[x]
        # check periodicity
        for x in range(nB + m * 6, len(word)):
            assert carries[x] == tab[(x - nB) % m], 'carry not steady'
        cup.append(tab)
    return dict(p=p, nB=nB, m=m, gam=gam, Bt=Bt, Wt=Wt, cup=cup)

def build(L, W, M, T, o, extra_fix=None):
    K = W + M + 2
    p, nB, m, gam = L['p'], L['nB'], L['m'], L['gam']
    S = [0]
    for t in range(T): S.append(S[-1] + gam[t % p])
    assert (S[T] % 2 == 0) and ((S[T] // 2) % m == 0), 'T not a period of the centre shift'
    mdl = cp_model.CpModel()
    n_t = [o + S[t] for t in range(T + 1)]
    hm = [((n + 1) // 2) % m for n in n_t]
    def lat(t, i):
        return L['Wt'][t % p][(hm[t] - K + i - nB) % m]
    P = [[None] * K for _ in range(T)]
    for t in range(T):
        for i in range(K):
            if i < K - W:
                P[t][i] = mdl.NewConstant(lat(t, i))
            else:
                P[t][i] = mdl.NewIntVar(0, 18, f'P{t}_{i}')
    for t in range(T):
        tn = (t + 1) % T
        n = n_t[t]; g = gam[t % p]
        odd = n % 2 == 1
        c0 = L['cup'][t % p][(hm[t] - K - nB) % m]
        cu = [None] * (K + 1); cu[0] = c0
        Oup = [None] * K
        for i in range(K):
            co = mdl.NewBoolVar(f'cu{t}_{i+1}')
            d = mdl.NewIntVar(0, b - 1, f'ou{t}_{i}')
            mdl.Add(P[t][i] + cu[i] == d + b * co)
            cu[i + 1] = co; Oup[i] = d
        cd = [None] * K; Odn = [None] * K
        if odd:
            Odn[K - 1] = Oup[K - 1]; cd[K - 2] = cu[K]; top = K - 2
        else:
            cd[K - 1] = cu[K]; top = K - 1
        # descending chain: carry-out of upper position mirror(i) is the carry into mirror(i-1)
        for i in range(top, -1, -1):
            d = mdl.NewIntVar(0, b - 1, f'od{t}_{i}')
            co2 = mdl.NewBoolVar(f'cdo{t}_{i}')
            mdl.Add(P[t][i] + cd[i] == d + b * co2)
            Odn[i] = d
            if i > 0: cd[i - 1] = co2
        delta = (n_t[t + 1] + 1) // 2 - (n + 1) // 2
        for i2 in range(2, K):
            i = i2 + delta
            if i >= K + 1: continue
            if g == 0:
                up = Oup[i]; part = Oup[i] if (odd and i == K - 1) else Odn[i]
            else:
                up = Oup[i] if i <= K - 1 else Odn[K - 1]
                part = Odn[i - 1]
            mdl.Add(P[tn][i2] == up + part)
    return mdl, P, K, n_t

def solve(rec, W, M, T, o, tl):
    L = lattice_data(rec)
    mdl, P, K, n_t = build(L, W, M, T, o)
    s = cp_model.CpSolver()
    s.parameters.num_workers = 1
    s.parameters.max_time_in_seconds = tl
    st = s.Solve(mdl)
    name = s.StatusName(st)
    sol = None
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        sol = [[s.Value(P[t][i]) for i in range(K)] for t in range(T)]
    return name, sol, K, n_t

if __name__ == '__main__':
    fn = sys.argv[8] if len(sys.argv) > 8 else '/home/claude/research/w3_formats/out/p8_scc.txt'
    recs = parse(fn)
    ri = int(sys.argv[1]); W = int(sys.argv[2]); M = int(sys.argv[3]); T = int(sys.argv[4])
    olo = int(sys.argv[5]); ohi = int(sys.argv[6]); tl = float(sys.argv[7])
    for o in range(olo, ohi):
        t0 = time.time()
        name, sol, K, n_t = solve(recs[ri], W, M, T, o, tl)
        print(f'rec{ri} W={W} M={M} T={T} o={o}: {name} ({time.time()-t0:.1f}s)', flush=True)
        if sol is not None:
            import json
            fn = f'/home/claude/research/w3_formats/out/kink_{fn.split("/")[-1][:-4]}_rec{ri}_W{W}_T{T}_o{o}.json'
            json.dump(dict(rec=ri, W=W, M=M, T=T, o=o, K=K, sol=sol), open(fn, 'w'))
            print('SOLUTION saved', fn, flush=True)

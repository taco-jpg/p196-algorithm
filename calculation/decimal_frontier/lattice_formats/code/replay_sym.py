#!/usr/bin/env python3
"""Replay of a "merged symmetric lattice" candidate: pair word P_t = B_t ++ chunk(w_t^inf, len l_t) ++ rev(B_t),
l_t = l_0 + S_t, with big-integer reverse-and-add on pair words (N' = val(P) has pair word pairs(digits)).
usage: replay_sym.py base recfile rec_index gap periods"""
import sys
sys.path.insert(0, '/home/claude/research/w3_formats/code')
import kink_sat
from scc_to_tmpl import parse

def lattice(rec, b):
    kink_sat.b = b
    return kink_sat.lattice_data(rec)

def axes(w):
    m = len(w)
    return [a for a in range(m) if all(w[k] == w[(a - k) % m] for k in range(m))]

def build_pair(Bt, w, l):
    m = len(w)
    chunk = [w[j % m] for j in range(l)]
    return list(Bt) + chunk + list(Bt)[::-1]

def raa_pair(P, b):
    M = sum(p * b ** i for i, p in enumerate(P))
    O = []
    while M:
        M, r = divmod(M, b); O.append(r)
    n = len(O)
    return O, [O[i] + O[n - 1 - i] for i in range(n)]

def main():
    b = int(sys.argv[1]); fn = sys.argv[2]; ri = int(sys.argv[3]); gap = int(sys.argv[4]); periods = int(sys.argv[5])
    rec = parse(fn)[ri]
    L = lattice(rec, b)
    p, nB, m, gam = L['p'], L['nB'], L['m'], L['gam']
    S = sum(gam)
    w0 = L['Wt'][0]
    ax = axes(w0)
    print(f"base {b} p={p} |B|={nB} m={m} S_p={S} axes of w_0: {ax}")
    if not ax:
        print('w_0 is not a palindromic necklace'); return
    best = None
    for a in ax:
        # l = a+1 mod m, l ~ gap*m
        l0 = (gap * m) // m * m + (a + 1) % m
        if l0 < gap * m: l0 += m
        # parity/centre free.  l0 chosen >= gap*m
        P = build_pair(L['Bt'][0], w0, l0)
        assert P == P[::-1], 'not palindromic'
        ok = True
        l = l0
        for t in range(p * periods):
            O, Pn = raa_pair(P, b)
            if O == O[::-1]:
                print(f'axis {a}: PALINDROME at step {t}'); ok = False; break
            tt = (t + 1) % p
            l += gam[t % p]
            Pe = build_pair(L['Bt'][tt], L['Wt'][tt], l)
            if Pn != Pe:
                # find first mismatch
                i = next(i for i in range(min(len(Pn), len(Pe))) if Pn[i] != Pe[i]) if len(Pn) == len(Pe) else -1
                print(f'axis {a}: MISMATCH at step {t+1} (len {len(Pn)} vs {len(Pe)}) first diff idx {i} actual {Pn[i] if i>=0 else None} expected {Pe[i] if i>=0 else None}; |B|={nB}, lattice start {nB}, l={l}')
                ok = False; break
            P = Pn
        if ok:
            print(f'axis {a}: OK for {p*periods} steps ({periods} periods), start n={len(build_pair(L["Bt"][0], w0, l0))}, final n={len(P)}')
            return True
    return False

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Q01 T*: exact bulk phase map and centre-splice gate.

Run at repository root:
  python3 calculation/new_structures/Q01/tstar_phase_center_gate.py

The proof is symbolic; independent canonical-integer checks validate the local
bulk formula, while a finite exact 30-state enumeration verifies the 120 clock.
"""
from itertools import product
from pathlib import Path
import tstar_carry_symmetry as core

ROOT = Path(__file__).resolve().parents[3]
WIDTH_PAIRS = ((20,20),(40,80),(80,40),(160,160))
J = [5]
C = [12]


def load_phases():
    rows = (ROOT / "calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt").read_text().splitlines()
    p, nB, m, base = map(int, rows[0].split())
    gamma = list(map(int, rows[1].split()))
    W = [list(map(int, s.split())) for s in rows[2:2+p]]
    B = [list(map(int, s.split())) for s in rows[2+2*p:2+3*p]]
    assert (p,nB,m,base) == (12,34,9,10)
    return gamma,B,W


def bulk_successor(U, gamma):
    _, s = core.steady_path(U)
    if gamma == 0:
        return tuple(2*U[i]-9+11*(s[i]-s[i+1]) for i in range(3))
    return tuple(U[i]+U[(i-1)%3]-9+10*(s[(i-1)%3]-s[(i+1)%3]) for i in range(3))


def centre_path(C, incoming):
    cuts = [incoming]
    for x in C:
        cuts.append((x+cuts[-1])//10)
    return cuts


def centre_criterion(C, incoming):
    if len(C)%2 == 0:
        return False
    types = ['L' if x<=8 else 'H' for x in C if x != 9]
    if not types:
        return False
    if any(types[i] == types[i+1] for i in range(len(types)-1)):
        return False
    return incoming == (1 if types[0]=='L' else 0)


def pal_centres(n):
    half=n//2
    if n%2 == 0:
        for prefix in product(range(19), repeat=half):
            yield list(prefix)+list(prefix[::-1])
    else:
        for prefix in product(range(19), repeat=half):
            for mid in range(0,19,2):
                yield list(prefix)+[mid]+list(prefix[::-1])


def actual_bulk_step(U, t, B, W, gamma, qwidth, kwidth):
    H=B[t]+W[t]*qwidth+J+U*kwidth
    P=H+C+H[::-1]
    n=core.realize_pairword(P)
    n1=n+core.reverse_value(n)
    P1=core.pairword(n1)
    start=len(B[t])+len(W[t])*qwidth+len(J)
    off=start+3*5
    observed=tuple(P1[off:off+3])
    assert all(tuple(P1[i:i+3])==observed for i in range(off,off+3*10,3))
    assert len(core.digits(n1))-len(core.digits(n)) == gamma[t]
    return observed


def main():
    gamma,B,W=load_phases()
    rows=core.all_u3_rows()
    rowset=set(map(tuple,rows))

    # Exact local formula cross-check at all 12 phases, all 30 rows, and four widths.
    for qwidth,kwidth in WIDTH_PAIRS:
        for t,g in enumerate(gamma):
            for U in rows:
                pred=bulk_successor(U,g)
                assert pred in rowset, (t,U,g,pred)
                obs=actual_bulk_step(U,t,B,W,gamma,qwidth,kwidth)
                assert pred==obs, (qwidth,kwidth,t,U,g,pred,obs)

    # Exhaust the exact phase automaton, with no width cutoff in its formula.
    patterns=[]
    for U0 in rows:
        U=tuple(U0)
        bits=[]
        for t in range(120):
            bits.append(core.steady_path(U)[0])
            U=bulk_successor(U,gamma[t%12])
            assert U in rowset
        assert U==tuple(U0)
        assert bits.count(0)==bits.count(1)==60
        patterns.append(''.join(map(str,bits)))
    assert len(set(patterns))==30

    # Among odd-centre phases the required low/high midpoint class follows tau_U.
    # Count the mandatory class switches over each 120-step clock.
    switch_counts=[]
    for initial_parity in (0,1):
        for U0 in rows:
            U=tuple(U0); parity=initial_parity; odd_tau=[]
            for t in range(120):
                tau=core.steady_path(U)[0]
                if parity == 1:
                    odd_tau.append(tau)
                g=gamma[t%12]
                U=bulk_successor(U,g)
                parity ^= g
            assert len(odd_tau)==60 and set(odd_tau)=={0,1}
            assert sorted((odd_tau.count(0),odd_tau.count(1))) == [28,32]
            switches=sum(odd_tau[i]!=odd_tau[i-1] for i in range(1,len(odd_tau)))
            assert switches in (33,34)
            switch_counts.append(switches)
    assert min(switch_counts)==33 and max(switch_counts)==34

    # Exhaustively validate the exact centre-splice criterion through length 8.
    centres=0
    for n in range(1,9):
        for C0 in pal_centres(n):
            for incoming in (0,1):
                cuts=centre_path(C0,incoming)
                actual=all(cuts[i]+cuts[n-i]==1 for i in range(n+1))
                assert actual==centre_criterion(C0,incoming),(
                    C0,incoming,cuts,actual,centre_criterion(C0,incoming)
                )
                centres+=1
    assert centres==419920
    print(f'TSTAR_BULK_MAP_PASS: {len(WIDTH_PAIRS)*12*len(rows)} phase/U bigint checks across {len(WIDTH_PAIRS)} independent (q,k) widths')
    print('TSTAR_CLOCK_PASS: all 30 U3 rows return after 120 steps; each tau word has 60 zeros and 60 ones')
    print('CENTRE_TYPE_SWITCH_PASS: on odd-centre phases tau has 28/32 or 32/28 split and requires 33 or 34 low/high switches per 120 steps')
    print(f'CENTRE_SPLICE_PASS: exact criterion matches {centres} palindromic-centre/carry cases through length 8')
    print('Scope: no stationary centre can carry complementary reflection at every phase; asymmetric centre/interface routes remain open')


if __name__=='__main__':
    main()

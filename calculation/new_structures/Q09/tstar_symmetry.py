#!/usr/bin/env python3
"""Q09 exact T* rooted p12/m9 carry-symmetry gate.
Run from repository root: python3 calculation/new_structures/Q09/tstar_symmetry.py

PAPER PROOF / COMPUTED TABLE; NOT a decimal Lychrel certificate.

Theorem (phase 0, all interior widths). Let B0 be the actual 34-coefficient
phase-0 exterior in calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt.
For a digit permutation pi and coefficient bijections a_0,a_1 satisfying
T(a_c(p),c)=(pi(digit(T(p,c))), carry(T(p,c))) for all p=0..18,c=0,1,
if applying a_(incoming carry) to any canonical symmetric pairword with low
exterior B0 and high exterior reverse(B0) leaves it symmetric, then pi and
both a_c are identity. This holds for every realizable interior and centre.

Proof. Such a carry-preserving lift exists only if pi(0)=0 and pi(9)=9, and
then it is unique:
a_0(p)=10*floor(p/10)+pi(p mod 10),
a_1(p)=10*floor((p+1)/10)+pi((p+1) mod 10)-1.
Since B0[33]=5, processing the first high-side coefficient resets either
incoming carry to 0; hence the carry entering every mirrored B0[i], i<33,
is independent of the interior. Eight fixed mirrored carry mismatches have
remainders r=0,2,3,4,5,6,7,8. A mismatch forces
pi(r+1)=pi(r)+1. With pi(0)=0 and pi(9)=9 these equations force
pi(1)=1 and pi(8)=8, then pi(7)=7, pi(6)=6, pi(5)=5, pi(4)=4,
pi(3)=3 and pi(2)=2. Thus pi and both unique lifts are identity.

All 12 B_t[33] values differ from 9, so the same reset argument yields a
phase-specific outer-boundary gate. Enumerating all 40,320 permutations fixing
0 and 9 gives candidate counts (1,2,2,1,1,1,1,1,2,1,1,24). Phases 1,2,8,11
retain candidates only at the outer boundary; these are not full-word
symmetries. This rules out a nontrivial fixed digit-permutation,
carry-preserving quotient at phase 0, but not phase-dependent/position-dependent
maps, carry-flipping seams, or exterior changes. No all-time decimal orbit is
claimed.
"""
from itertools import permutations
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT / "calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt"
EXPECTED_R = [
    (0,2,3,4,5,6,7,8), (0,1,3,4,5,7), (0,1,2,3,7,8),
    (0,2,3,5,6,7,8), (0,2,4,5,6,7,8), (0,1,2,3,4,5,7,8),
    (0,1,2,3,4,5,7,8), (0,3,4,5,6,7,8), (0,1,2,4,7,8),
    (0,1,2,4,5,6,8), (0,1,2,3,4,5,6,8), (2,3,6,8),
]
EXPECTED_COUNTS = [1,2,2,1,1,1,1,1,2,1,1,24]

def read_data():
    rows = [[int(x) for x in line.split()] for line in DATA.read_text().splitlines() if line.strip()]
    assert rows[0] == [12,34,9,10]
    bands, exteriors = rows[2:14], rows[26:38]
    assert len(bands) == len(exteriors) == 12
    assert all(len(w)==9 for w in bands) and all(len(b)==34 for b in exteriors)
    assert all(0 <= x <= 18 for b in exteriors for x in b)
    assert all(b[-1] != 9 for b in exteriors)
    return bands, exteriors

def carry_inputs(word, initial=0):
    c, incoming = initial, []
    for p in word:
        incoming.append(c)
        c = (p+c)//10
    return incoming, c

def high_mirror_carry(B, i, initial):
    c = initial
    for p in reversed(B[i+1:]):
        c = (p+c)//10
    return c

def boundary_constraints(B):
    low, _ = carry_inputs(B, 0)
    R, witnesses = set(), []
    for i in range(33):
        h0, h1 = high_mirror_carry(B,i,0), high_mirror_carry(B,i,1)
        assert h0 == h1, (i,h0,h1,B[-1])
        r = B[i] % 10
        if low[i] != h0 and r != 9:
            R.add(r)
            witnesses.append((i,B[i],r,low[i],h0))
    return tuple(sorted(R)), witnesses

def digits(n, base=10):
    out=[]
    while n:
        out.append(n%base)
        n//=base
    return out or [0]

def value(ds, base=10):
    n=0
    for d in reversed(ds):
        n=n*base+d
    return n

def realize(P):
    assert P == P[::-1] and P[0] > 0
    n, ds = len(P), [0]*len(P)
    for i in range(n//2):
        ds[i] = max(0,P[i]-9)
        ds[n-1-i] = P[i]-ds[i]
    if n%2:
        assert P[n//2] % 2 == 0
        ds[n//2] = P[n//2]//2
    assert ds[-1] > 0
    return value(ds,10)

def pairword(n):
    s=str(n)
    return [int(s[-1-i])+int(s[i]) for i in range(len(s))]

def lifted_word(P, pi):
    cins,_ = carry_inputs(P,0)
    Q=[]
    for p,c in zip(P,cins):
        if c == 0:
            Q.append(10*(p//10)+pi[p%10])
        else:
            Q.append(10*((p+1)//10)+pi[(p+1)%10]-1)
    return Q

def main():
    # Required positive controls first: existing independent bigint replay reproduces
    # the Lean-verified base-9 cycle and computed base-50 positive-growth cycle.
    subprocess.run([sys.executable, str(ROOT/"calculation/new_structures/Q09/check.py")], check=True)

    bands, exteriors = read_data()
    perms = [(0,)+p+(9,) for p in permutations(range(1,9))]
    assert len(perms)==40320
    table=[]
    for t,B in enumerate(exteriors):
        R,_ = boundary_constraints(B)
        assert R == EXPECTED_R[t], (t,R,EXPECTED_R[t])
        survivors=[pi for pi in perms if all(pi[r+1]==pi[r]+1 for r in R)]
        assert len(survivors)==EXPECTED_COUNTS[t], (t,R,len(survivors))
        table.append((t,B[-1],R,len(survivors)))
        print(f"PHASE {t:02d}: B[-1]={B[-1]}; R={list(R)}; outer-boundary candidates={len(survivors)}")

    R0,wit=boundary_constraints(exteriors[0])
    assert R0==(0,2,3,4,5,6,7,8)
    assert [pi for pi in perms if all(pi[r+1]==pi[r]+1 for r in R0)] == [tuple(range(10))]
    print("PHASE 0: only identity among all 40,320 carry-preserving digit permutations")
    print("PHASE 0 witnesses (i,p,r,low,high):", wit)

    # Physical canonical decimal sources at four independent W9 widths, for all phases.
    J,C=[5,2,7],[4,14,4]
    for q in (20,40,80,160):
        for t,(B,W) in enumerate(zip(exteriors,bands)):
            inner=W*q + J + C + J[::-1] + W[::-1]*q
            P=B+inner+B[::-1]
            assert P==P[::-1] and P[len(P)//2]%2==0
            n=realize(P)
            assert pairword(n)==P, (q,t,"source pairword")
            out=n+int(str(n)[::-1])
            cins,final=carry_inputs(P,0)
            normalized=[]
            c=0
            for p in P:
                z=p+c
                normalized.append(z%10)
                c=z//10
            if c:
                normalized.append(c)
            assert digits(out)==normalized, (q,t,"integer normalization")
            full,_=carry_inputs(P,0)
            for i in range(33):
                assert full[len(P)-1-i]==high_mirror_carry(B,i,0), (q,t,i)
            if t==0:
                pi=(0,2,1,3,4,5,6,7,8,9)
                assert lifted_word(P,pi)!=lifted_word(P,pi)[::-1], (q,"nonidentity mirror")
        print(f"TRUE DECIMAL SOURCE CONTROL q={q}: all 12 phases and exact carries PASS")
    print("SCOPE: all-width result follows from carry reset plus exact phase-0 witnesses; no Lychrel certificate.")

if __name__ == "__main__":
    main()

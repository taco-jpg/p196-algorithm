#!/usr/bin/env python3
"""Audit phase-1 odd-centre modulo-11 gate: algebra, residues and exact counts."""
from collections import Counter
from pathlib import Path
from itertools import product
import random

ROOT=Path(__file__).resolve().parents[3]
LATTICE=ROOT/'calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt'

def load():
    rows=[[int(z) for z in s.split()] for s in LATTICE.read_text().splitlines()]
    assert rows[0]==[12,34,9,10]
    return rows[27],rows[3]  # B1 and W1, 12 W then 12 auxiliary then 12 B

def alt(w):
    return sum(x if i%2==0 else -x for i,x in enumerate(w))

def tpl(B,W,J,U,C,q,k):
    h=B+W*q+J+U*k
    return h+C+h[::-1]

def candidates():
    return [v[r:]+v[:r] for a in range(0,19,2) for v in [[9,a,18-a]] for r in range(3)]

def counts(length):
    d=Counter({0:1})
    for i in range(length):
        nxt=Counter()
        for residue,n in d.items():
            for digit in range(19):
                nxt[(residue+(digit if i%2==0 else -digit))%11]+=n
        d=nxt
    return d

def main():
    B,W=load()
    assert (len(B),len(W),alt(B),alt(W))==(34,9,-5,10)
    C=[4,14,4]
    U=candidates()
    valid=[(i+1,v) for i,v in enumerate(U) if alt(v)%11==alt(C)%11]
    assert valid==[(1,[9,0,18]),(29,[18,0,9])]
    d=counts(6)
    assert sum(d.values())==19**6 and d[8]==4_276_882
    rng=random.Random(34261029)
    for _ in range(2000):
        J=[rng.randrange(19) for _ in range(6)]
        V=U[rng.randrange(30)]
        for q,k in product((14,15),(100,101)):
            actual=alt(tpl(B,W,J,V,C,q,k))
            formula=2*(-5+10*(q%2)+(-1)**q*(alt(J)+(k%2)*alt(V)))+(-1)**(q+k)*alt(C)
            assert actual==formula
    print('PAPER GATE CHECK PASS')
    print('B1 A=-5 W1 A=10; for odd C: A(U)=A(C), 2A(J)+A(C)=10 mod11')
    print('C=(4,14,4): eligible U ranks',valid)
    print('eligible J with A(J)=8:',d[8], 'of',19**6)
    print('all-width eligible odd-centre J/U:',2*d[8], 'of',30*19**6)
    print('Even centres are unfiltered; reference-only U exclusion is unsound.')

if __name__=='__main__':main()

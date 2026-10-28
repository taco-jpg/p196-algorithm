#!/usr/bin/env python3
"""Exact test (Fractions) of the scalar recurrence  V(B') = (1+b^-gam) V(B) - (b^2-1) kappa(B),
V(B)=sum_{i<n} B_i b^-i + b^(1-n),  kappa(B)=sum_{i<n} c_i b^(-1-i) (+ e1 * b^(-n)/(b-1)*... tested below), c_i forward carry out of position i."""
import sys, random
from fractions import Fraction as Fr
sys.path.insert(0,'/home/claude/research/w2_theory'); sys.path.insert(0,'/home/claude/research/w2_theory/scripts')
import mirror as m, lib
from parse_bw import parse_bw
def V(b,B):
    n=len(B); return sum(Fr(v)*Fr(1,b**i) for i,v in enumerate(B))+Fr(b,b**n)
def kappa(b,B):
    c=0; s=Fr(0)
    for i,v in enumerate(B):
        t=v+c; c=t//b; s+=Fr(c,b**(i+1))
    e1=c
    return s,e1
def stepU(b,B):
    e1=m.e1(b,B); DB=m.DB(b,B); DR,gm=m.norm(b,B[::-1],1-e1)
    nb=m._zw(DB,DR[::-1]) if gm==0 else m._zw(DB+[(b-1)*(1-e1)],[1]+DR[::-1])
    return nb,gm,e1
random.seed(3); worst=Fr(0); cnt=0; diffs=set()
for b in (3,10,11):
    for _ in range(3000):
        n=random.randint(1,9); B=[random.randint(0,2*b-2) for _ in range(n)]
        nb,gm,e1=stepU(b,B)
        lhs=V(b,nb); rhs=(1+Fr(1,b**gm))*V(b,B)
        k,e=kappa(b,B)
        d=(rhs-lhs)  # should equal (b^2-1)*kappa_eff
        keff=d/(b*b-1)
        diffs.add((e1, gm, ( keff-k)*b**n ))   # correction as multiple of b^-n
print(sorted(diffs)[:20], len(diffs))

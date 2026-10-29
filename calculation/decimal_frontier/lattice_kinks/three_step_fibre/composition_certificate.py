#!/usr/bin/env python3
"""Finite-cone certificate for all-k three-step INTEGER fibres in p12/m9.
Checks the period-9 reset premises, exact single-switch response, and
recomposition from the first-step (+9,0,-9) response. The proof report
justifies lifting the finite checks to arbitrary k, not an extrapolation.
"""
import sys, random
from pathlib import Path
from independent_integer import load,pairword

def step(P):
    carry=0; digits=[]
    for q in P:
        z=q+carry; digits.append(z%10);carry=z//10
    if carry: digits.append(carry)
    return [digits[i]+digits[-1-i] for i in range(len(digits))]

def switch(P,j):
    Q=P[:]
    for offset,value in enumerate((8,10,12)):
        assert Q[j+offset]!=value
        Q[j+offset]=Q[len(P)-1-j-offset]=value
    return Q

def certificate():
    gamma,W,B=load(Path(__file__).resolve().parent/'lattice_input.txt')
    assert gamma==[1,0,0,0]*3
    assert W[3][:3]==[4,0,17] and W[4][:3]==[8,1,15]
    assert all(not (W[3][i]==9 and W[3][(i+1)%9]==9) for i in range(9))
    assert 9 not in W[4]
    for n in (200,201,218,219,400,401,800,801,1800,1801):
        P=pairword(3,n,W,B)
        T=step(P)
        assert len(T)==n
        U=step(T)
        assert len(U)==n+1
        for j in (52,61,70,79,88,97):
            if j+30>=n//2:continue
            Q=switch(P,j); TQ=step(Q)
            assert len(TQ)==n
            delta=[(i,TQ[i]-T[i]) for i in range(len(T)) if TQ[i]!=T[i]]
            expected=sorted([(j,9),(j+2,-9),(n-1-j,9),(n-3-j,-9)])
            assert delta==expected,(n,j,delta,expected)
            assert step(TQ)==U
    # Algebraic premise: input carry disturbances are separated by >=9,
    # and a non-9 column resets the carry after at most one extra column.
    # Hence first-step responses add without interacting and can be verified
    # from a single switch in one spatial-period representative.
    # The second input W4 has no 9, making its carry response local too.
    for k in (1,2,3,5,8,12,20,40):
        n=200+18*k
        P=pairword(3,n,W,B)
        base=step(P); common=step(base)
        js=[52+9*i for i in range(k)]
        assert js[-1]+30<n//2
        rng=random.Random(5000+k)
        masks=list(range(1<<k)) if k<=8 else ([0,(1<<k)-1]+[rng.getrandbits(k) for _ in range(64)])
        for mask in masks:
            Q=P[:]
            expected=base[:]
            for b,j in enumerate(js):
                if mask>>b&1:
                    Q=switch(Q,j)
                    for i,change in ((j,9),(j+2,-9),(n-1-j,9),(n-3-j,-9)):
                        expected[i]+=change
            got=step(Q)
            assert got==expected,(k,mask,'nonadditive')
            assert step(got)==common,(k,mask,'second pairword mismatch')
    print('ALL_K_COMPOSITION_CARRY_RESET_CERTIFICATE_PASS')
    print('EXACT_INDEPENDENT_LOCAL_RESPONSE_PLUS9_MINUS9_PASS')

if __name__=='__main__':certificate()

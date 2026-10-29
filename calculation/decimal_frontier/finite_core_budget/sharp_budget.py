#!/usr/bin/env python3
"""Sharp phase-aligned source guard for a finite-core cycle.
Run: python3 calculation/decimal_frontier/finite_core_budget/sharp_budget.py .
Python 3 stdlib, no Lean or decimal certificate claim.
"""
import sys
from itertools import product
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'finite_core_pumping'))
from finite_core_check import base26, edge, templ, to_digits, from_digits

def threshold(m,ds):
    assert m>=1
    s=low=0
    for d in ds:
        low=min(low,s)
        s+=d
    return 2*m-low

def align_up(n,m,rho):
    assert m>=1 and 0<=rho<m
    return rho+m*max(0,(n-rho+m-1)//m)

def forward(m,ds,l):
    for d in ds:
        if l<2*m:return False
        l+=d
        if l<0:return False
    return True

def exhaustive():
    count=0
    for m in range(1,7):
        for p in range(1,6):
            for ds in product(range(-3,4),repeat=p):
                if sum(ds)<0 or sum(ds)%m:continue
                T=threshold(m,ds)
                for rho in range(m):
                    L=align_up(T,m,rho)
                    assert L%m==rho and forward(m,ds,L)
                    if L-m>=0: assert not forward(m,ds,L-m)
                    for gap in range(T-1,T+2):
                        if gap>=0:assert forward(m,ds,gap)==(gap>=T)
                    count+=1
    assert count==76955,count
    return count

def gauged(s,a):
    B,W,C,rho=s
    tail=[W[(rho+i)%len(W)] for i in range(a*len(W))]
    return B,W,tail+C+tail[::-1],rho

def signed_control():
    original=base26()
    gauges=(4,2,4,1)
    states=[gauged(e[0],a) for e,a in zip(original,gauges)]
    shifts=[original[i][2]+gauges[i]-gauges[(i+1)%4] for i in range(4)]
    assert shifts==[2,-2,3,-2]
    assert all(edge(26,states[i],states[(i+1)%4],shifts[i]) for i in range(4))
    assert sum(shifts)==1
    L=align_up(threshold(1,shifts),1,states[0][3])
    conservative=2+sum(max(0,-s) for s in shifts)
    assert (L,conservative)==(2,6)
    N=from_digits(templ(*states[0][:3],L),26)
    for t in range(2000):
        j=t%4
        D=to_digits(N,26)
        assert N==from_digits(templ(*states[j][:3],L),26),('template',t)
        assert D!=D[::-1],('palindrome',t)
        nxt=N+from_digits(D[::-1],26)
        assert nxt==from_digits([a+b for a,b in zip(D,D[::-1])],26),('arithmetic',t)
        L+=shifts[j]
        assert nxt==from_digits(templ(*states[(j+1)%4][:3],L),26),('next',t)
        N=nxt
    return conservative,L

if __name__=='__main__':
    n=exhaustive()
    conservative,L=signed_control()
    print(f'PHASE_MIN_BUDGET_EXHAUSTIVE_PASS {n} exact cases')
    print(f'SIGNED_BASE26_POSITIVE_CONTROL_PASS 2000 steps, optimal gap=2, conservative gap={conservative}, final gap={L}')

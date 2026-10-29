#!/usr/bin/env python3
"""N09: independently test the necessary p12 W9/U3 joint-growth clock.
PAPER PROOF is in reports/N09P12DualGrowth240Gate.md.
This code tests genuine decimal integers, NOT an infinite orbit certificate.
"""
import sys
sys.set_int_max_str_digits(0)

B=[10,4,6,6,7,12,9,16,16,13,0,2,10,17,7,0,18,6,5,18,4,18,14,9,14,8,12,17,10,4,6,4,0,5]
W=[5,18,4,8,1,15,4,0,5]
def word(q,k,J,U,C):
    H=B+W*q+J+U*k
    return H+C+H[::-1]
def root(P):
    assert P==P[::-1] and P[0]>0
    d=[0]*len(P)
    for i in range(len(P)//2):
        d[i]=min(9,P[i])
        d[-1-i]=P[i]-d[i]
        assert 0<=d[-1-i]<=9
    if len(P)%2:
        assert P[len(P)//2]%2==0
        d[len(P)//2]=P[len(P)//2]//2
    assert d[-1]>0
    return int("".join(str(t) for t in reversed(d)))
def pair(n):
    s=str(n)
    return [int(a)+int(b) for a,b in zip(s[::-1],s)]
def advance(n):
    return n+int(str(n)[::-1])
def arithmetic(r):
    valid=[]
    for dq in range(6*r+1):
        for dk in range(6*r+1):
            if 9*dq+3*dk==15*r and (120*dq+54*dk)%9==0:
                valid.append((dq,dk))
    return valid
def physical(q,k,J,U,C):
    P=word(q,k,J,U,C)
    x=root(P)
    assert pair(x)==P and x%11==0
    total=0
    for i in range(240):
        old=len(str(x))
        x=advance(x)
        total+=len(str(x))-old
    assert total==60,(q,k,total)
    target=word(q+3,k+1,J,U,C)
    actual=pair(x)
    assert len(actual)==len(target)
    assert (sum(target)-sum(P))%9==0
    bad=[i for i in range(len(target)) if target[i]!=actual[i]]
    return (q,k,len(actual),total,len(bad),bad[0] if bad else None)
def main():
    assert len(B)==34 and len(W)==9 and sum(W)==60
    for a in range(0,19,2):
        U=[9,a,18-a]
        assert sum(U)==27
    table={r:arithmetic(r) for r in range(1,13)}
    assert table[1]==[(0,5)]
    assert table[2]==[(0,10),(3,1)]
    assert all(dq%3==0 and 3*dq+dk==5*r for r,v in table.items() for dq,dk in v)
    assert all(not(dq>0 and dk>0) for dq,dk in table[1])
    assert [(dq,dk) for dq,dk in table[2] if dq>0 and dk>0]==[(3,1)]
    print('ALL_R_CLOCK_GATE_PASS (symbolic proof in report); r=1',table[1],'r=2',table[2])
    J=[2,2];U=[9,8,10];C=[0]
    for q in (20,40,80,160):
        for k in (80,240):
            row=physical(q,k,J,U,C)
            print('REAL_INTEGER_CONTROL',*row)
            assert row[-2]>0
            assert row[-1]==9*q-8
    print('N09_TWO_BANK_GATE_CHECK_PASS; no complete return or decimal Lychrel claimed')
if __name__=='__main__':
    main()

#!/usr/bin/env python3
"""Necessary all-length gate for a linearly-correlated slow coordinate.
No decimal Lychrel certificate or candidate is claimed.
Reproduce: python3 calculation/new_structures/Q21/correlated_gate.py
"""
from math import gcd
B=[17,5,0,1,13,4,14,12,9,8,15,16,17,13,17,9,1,4,4,11,8,16,0,9,14,11,9,11,6,13,18,9,4,7,17,15,9,7,13]
W=[17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13]

def seed(P):
    assert P==P[::-1]
    ds=[0]*len(P)
    for i in range((len(P)+1)//2):
        j=len(P)-1-i;p=P[i]
        if i==j:
            assert p%2==0
            ds[i]=p//2
        else:
            h=max(p-9,1 if i==0 else 0)
            ds[i]=p-h;ds[j]=h
            assert 0<=ds[i]<10 and 0<=h<10
    n=0
    for d in ds[::-1]:n=n*10+d
    return n

def rev(n):
    z=0
    while n:z=z*10+n%10;n//=10
    return z

def pair(n):
    ds=[]
    while n:ds.append(n%10);n//=10
    return [a+b for a,b in zip(ds,ds[::-1])]

def nextpair(P):
    ds=[];carry=0
    for x in P:
        z=x+carry;ds.append(z%10);carry=z//10
    if carry:ds.append(carry)
    return [a+b for a,b in zip(ds,ds[::-1])]

def passes_necessary(r,a,d,delta,h):
    """Arithmetic permission only, NOT a certificate."""
    if not(r>=1 and a>=0 and d>=1 and delta>=1 and gcd(h,9)==1):
        return False
    if ((pow(7,r,9)-1)*h)%9: return False
    if r%3==0 and (delta*h)%9: return False
    return delta*(20*a+d)==22*r

def test():
    assert len(B)==39 and len(W)==20 and sum(W)==180
    for r in range(1,9):
        for a in range(4):
            for d in range(1,100):
                for delta in range(1,200):
                    assert not passes_necessary(r,a,d,delta,1),(r,a,d,delta)
    assert passes_necessary(9,1,2,9,1)
    assert passes_necessary(9,0,22,9,1)
    assert passes_necessary(9,0,11,18,1)
    V=[8]*21+[7] # d=22, sum=175 (unit modulo 9)
    assert len(V)==22 and gcd(sum(V),9)==1
    for a in (0,1):
        for s in (20,40,80,160):
            q=40+a*s
            C=V*s+[16]+V[::-1]*s
            P=B+W*q+C+W[::-1]*q+B[::-1]
            n=seed(P)
            for t in range(8):
                Q=nextpair(P)
                n+=rev(n)
                assert pair(n)==Q,(a,s,t)
                P=Q
    print("PASS correlated unit-charge r<9 necessary gate; r=9 arithmetic control and independent ordinary-decimal q(s)=40+a*s integer replay at s=20/40/80/160")
if __name__=="__main__":test()

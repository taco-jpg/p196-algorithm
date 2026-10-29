#!/usr/bin/env python3
"""Q21 all-symbolic-length necessary gate (not a decimal Lychrel certificate)."""
from math import gcd

# Published p8/m20 rooted phase-0 coefficient fixture, units first.
B = [17,5,0,1,13,4,14,12,9,8,15,16,17,13,17,9,1,4,4,11,8,16,0,9,14,11,9,11,6,13,18,9,4,7,17,15,9,7,13]
W = [17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13]
C = [8,0,0,16,0,0,8]

def admissible(r,d,h):
    """Necessary candidates (e,delta), not sufficient physical certificates."""
    assert r>=1 and d>=1
    if ((pow(2,88*r,9)-1)*h)%9: return []
    out=[]
    for e in range((22*r-1)//20+1):
        a=22*r-20*e
        if a>0 and a%d==0:
            delta=a//d
            if r%3==0 and delta*h%9: continue
            out.append((e,delta))
    return out

def seed(P):
    assert P==P[::-1] and P
    n=len(P);ds=[0]*n
    for i in range((n+1)//2):
        j=n-1-i;p=P[i]
        if i==j:
            assert p%2==0;ds[i]=p//2
        else:
            hi=max(p-9,1 if i==0 else 0);lo=p-hi
            assert 0<=hi<=9 and 0<=lo<=9
            ds[i]=lo;ds[j]=hi
    assert ds[-1]>0
    x=0
    for v in ds[::-1]:x=x*10+v
    return x

def rev(x):
    y=0
    while x:y=y*10+x%10;x//=10
    return y

def pair(x):
    ds=[]
    while x:ds.append(x%10);x//=10
    return [a+b for a,b in zip(ds,ds[::-1])]

def nextpair(P):
    ds=[];carry=0
    for a in P:
        z=a+carry;ds.append(z%10);carry=z//10
    if carry:ds.append(carry)
    return [a+b for a,b in zip(ds,ds[::-1])]

def test():
    assert len(B)==39 and len(W)==20 and sum(W)==180
    for r in range(1,6):
        for d in range(1,22*r+1):
            for h in (1,2,4,5,7,8):assert not admissible(r,d,h)
    assert admissible(6,8,64)==[(3,9)]
    for r in range(1,20):
        for d in range(1,15):
            for h in range(9):
                for e,delta in admissible(r,d,h):
                    assert 20*e+d*delta==22*r
                    assert (pow(2,88*r,9)-1)*h%9==0
                    if r%3==0:assert delta*h%9==0
    for q in (20,40,80,160):
        P=B+W*q+C+W[::-1]*q+B[::-1]
        n=seed(P)
        for t in range(264):
            Q=nextpair(P)
            n+=rev(n)
            assert pair(n)==Q,(q,t)
            P=Q
        assert len(P)==2*len(B)+40*q+len(C)+132
    print("PASS: necessary unit-charge r<6 obstruction, r=6 arithmetic witness, and independent ordinary-decimal controls at q=20/40/80/160 for 264 steps.")
if __name__=="__main__":test()

#!/usr/bin/env python3
"""AC02 independent Python arbitrary-precision ordinary-decimal reverse/add check.

Compares all intermediate decimal numbers against an independent
LSD-first coefficient normalizer, and verifies the centre necessary test.
"""
import sys,random
sys.set_int_max_str_digits(0)
B=[10,4,6,6,7,12,9,16,16,13,0,2,10,17,7,0,18,6,5,18,4,18,14,9,14,8,12,17,10,4,6,4,0,5]
W=[5,18,4,8,1,15,4,0,5]
US=[(9,2,16),(2,16,9),(16,9,2)]
def templ(U,C,q,k,J=(5,)):
    h=B+W*q+list(J)+list(U)*k
    return h+list(C)+h[::-1]
def to_source(p):
    if p!=p[::-1]:raise ValueError('nonpalindromic pairword')
    n=len(p);d=[0]*n
    for i in range(n//2):
        d[i]=max(0,p[i]-9);d[-1-i]=p[i]-d[i]
    if n%2:
        assert p[n//2]%2==0
        d[n//2]=p[n//2]//2
    assert d[-1]>0 and all(0<=x<=9 for x in d)
    return int(''.join(map(str,d[::-1])))
def from_n(n):return [int(z) for z in str(n)[::-1]]
def decimal_pair(n):
    d=from_n(n)
    return [d[i]+d[-1-i] for i in range(len(d))]
def run(U,C,q,k):
    P=templ(U,C,q,k)
    n=to_source(P);pp=P;g=[]
    for t in range(120):
        assert decimal_pair(n)==pp,(U,C,q,k,t,'pairword discrepancy')
        d=str(n)
        n2=n+int(d[::-1]);g.append(len(str(n2))-len(d));n=n2
        dl=[];carry=0
        for x in pp:
            z=x+carry;dl.append(z%10);carry=z//10
        if carry:dl.append(carry)
        assert dl==from_n(n)
        pp=[dl[i]+dl[-1-i] for i in range(len(dl))]
    assert pp==decimal_pair(n)
    target=templ(U,C,q,k+5)
    mid=len(pp)//2;span=122+len(C)+30
    match=(len(pp)==len(target) and all(pp[i]==target[i] for i in range(mid-span,mid+span+1)))
    assert sum(g)==30 and g==[1,0,0,0]*30
    return match
if __name__=='__main__':
    rng=random.Random(20261029);cases=0
    for U in US:
        for clen in (7,8,13,14):
            h=[rng.randrange(19) for _ in range(clen//2)]
            C=h+([2*rng.randrange(10)] if clen%2 else [])+h[::-1]
            for q,k in ((14,100),(20,80),(40,160),(80,320),(160,640)):
                assert not run(U,C,q,k)
                cases+=1
    print('PASS',cases,'cases /',120*cases,'genuine decimal transitions')
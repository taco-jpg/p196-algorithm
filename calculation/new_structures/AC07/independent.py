#!/usr/bin/env python3
"""Separate Python arbitrary-precision decimal n+reverse(n) physical replay."""
import sys,random
if hasattr(sys,'set_int_max_str_digits'):sys.set_int_max_str_digits(0)
from abstract import B,W,U
def pair(u,c,q,k,J=(5,)):
    h=B+W*q+list(J)+list(U[u])*k
    return h+c+h[::-1]
def realize(p):
    n=len(p);d=[0]*n
    for i in range(n//2):
        high=min(9,p[i]);low=p[i]-high
        assert 0<=low<=9
        d[i]=low;d[n-1-i]=high
    if n%2:assert p[n//2]%2==0;d[n//2]=p[n//2]//2
    assert d[-1]
    return int(''.join(map(str,d[::-1])))
def replay(ui,C,q,k,J=(5,)):
    n=realize(pair(ui,C,q,k,J));clock=[]
    for t in range(120):
        s=str(n);n+=int(s[::-1]);clock.append(len(str(n))-len(s))
    s=str(n);got=[int(s[i])+int(s[-1-i]) for i in range(len(s))]
    want=pair(ui,C,q,k+5,J)
    i=next((i for i,(a,b) in enumerate(zip(got,want)) if a!=b),None)
    return i,got==want,clock
if __name__=='__main__':
    r=random.Random(707)
    for ui in range(3):
        for cl in (7,8,9,10,13,14):
            C=[0]*cl
            for i in range(cl//2):C[i]=C[cl-1-i]=r.randrange(19)
            if cl%2:C[cl//2]=2*r.randrange(10)
            for q,k in ((14,100),(20,100),(40,160),(80,320),(160,640)):
                i,ok,g=replay(ui,C,q,k)
                assert g==[1,0,0,0]*30
                print('BIGINT',ui,cl,q,k,'first',i,'return',ok)

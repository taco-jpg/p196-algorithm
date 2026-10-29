#!/usr/bin/env python3
"""AC43 independent Python integer replay (no carry-cap code imported)."""
import random,sys
sys.set_int_max_str_digits(0)
B0=[10,4,6,6,7,12,9,16,16,13,0,2,10,17,7,0,18,6,5,18,4,18,14,9,14,8,12,17,10,4,6,4,0,5]
W0=[5,18,4,8,1,15,4,0,5]
B10=[2,11,1,1,11,17,14,3,9,3,0,0,12,13,16,4,9,6,6,4,6,4,8,14,12,16,12,8,17,5,6,5,9,16]

def source(q,k,J,U,C):
    H=B0+W0*q+J+U*k
    P=H+C+H[::-1]
    d=[0]*len(P)
    for i in range(len(P)//2):
        h=min(9,P[i]);d[i]=P[i]-h;d[-1-i]=h
    if len(P)%2:
        assert P[len(P)//2]%2==0
        d[len(P)//2]=P[len(P)//2]//2
    return int("".join(map(str,d[::-1])))

def root(n):
    a=[int(c) for c in str(n)]
    return [a[i]+a[-1-i] for i in range(34)]

def run(q,k,J,U,C):
    n=source(q,k,J,U,C);g=[];r10=None
    for t in range(130):
        if t==10:r10=root(n)
        s=str(n);n+=int(s[::-1]);g.append(len(str(n))-len(s))
    assert r10==root(n)==B10
    assert g[:10]==[1,0,0,0,1,0,0,0,1,0]
    assert g[10:]==[0,0,1,0,0,0,1,0,0,0,1,0]*10

if __name__=="__main__":
    rng=random.Random(4309003)
    for q,k in [(14,100),(20,80),(40,160),(80,320),(160,640)]:
        for U,C in [([9,0,18],[4,4]),([16,9,2],[4,14,4])]:
            run(q,k,[rng.randrange(19) for _ in range(6)],U,C)
    print("PASS ten true-integer 130-step controls, both centre parities")

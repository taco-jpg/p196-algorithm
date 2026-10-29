#!/usr/bin/env python3
"""Independent true-bigint decimal reverse-and-add audit for AC22 controls."""
import random,sys,subprocess,argparse
sys.set_int_max_str_digits(0)
B=[1,5,10,12,13,10,3,7,14,11,4,2,3,9,15,7,9,15,11,14,13,13,14,5,5,13,11,11,9,5,10,10,4,5]
W=[10,14,13,12,9,7,10,4,5]
def realize(P):
    assert P==P[::-1]
    d=[0]*len(P)
    for i in range(len(P)//2):
        high=min(P[i],9);d[i]=P[i]-high;d[-1-i]=high
    if len(P)%2:
        assert P[len(P)//2]%2==0
        d[len(P)//2]=P[len(P)//2]//2
    assert d[-1]
    return int(''.join(map(str,reversed(d))))
def run(J,U,C,q,k):
    H=B+W*q+J+U*k
    n=realize(H+C+H[::-1]);clock=[]
    for t in range(120):
        s=str(n);n2=n+int(s[::-1]);clock.append(len(str(n2))-len(s));n=n2
    s=str(n);P=[int(a)+int(b) for a,b in zip(s,s[::-1])][::-1]
    Ht=B+W*q+J+U*(k+5);target=Ht+C+Ht[::-1]
    mismatch=next((i for i,(x,y) in enumerate(zip(P,target)) if x!=y),None)
    if mismatch is None and len(P)!=len(target):mismatch=min(len(P),len(target))
    return mismatch,clock
if __name__=="__main__":
    rng=random.Random(20261029)
    for q,k in [(14,100),(20,80),(40,160),(80,320),(160,640)]:
        for parity in (0,1):
            for t in range(3):
                j=rng.randrange(19**5);v=j;J=[]
                for x in range(5):J.append(v%19);v//=19
                a=rng.randrange(10);rot=rng.randrange(3)
                U=[9,2*a,18-2*a];U=U[rot:]+U[:rot]
                C=[4,14,4] if parity else [4,4]
                mismatch,clock=run(J,U,C,q,k)
                assert sum(clock)==30
                assert mismatch is not None
                print(q,k,J,U,C,"mismatch",mismatch,"overflow",''.join(map(str,clock)))

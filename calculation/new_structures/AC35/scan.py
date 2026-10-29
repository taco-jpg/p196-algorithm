#!/usr/bin/env python3
"""Phase-2 rooted p12/m9 physical Python integer test, not an all-time certificate."""
import sys
sys.set_int_max_str_digits(0)
B=(2,11,1,6,8,1,7,15,9,3,9,4,7,9,10,16,9,11,4,10,8,8,9,11,11,7,4,3,9,12,1,1,9,11)
W=(1,10,8,5,9,16,0,9,11)
def rotations():
    return [tuple(([9,a,18-a]*2)[t:t+3]) for a in range(0,19,2) for t in range(3)]
def word(J,U,C,q,k):
    H=list(B)+list(W)*q+list(J)+list(U)*k
    return H+list(C)+H[::-1]
def realize(P):
    assert P==P[::-1]
    d=[0]*len(P)
    for i in range(len(P)//2):
        hi=min(9,P[i]);lo=P[i]-hi
        d[i],d[-1-i]=lo,hi
    if len(P)%2:
        z=P[len(P)//2];assert z%2==0
        d[len(P)//2]=z//2
    assert d[-1]>0
    return int(''.join(map(str,d[::-1])))
def pair(n):
    s=str(n)
    return [int(s[-1-i])+int(s[i]) for i in range(len(s))]
def run(J,U,C,q=14,k=100,steps=120,trace=False):
    P=word(J,U,C,q,k);n=realize(P);gamma=[]
    for t in range(steps):
        s=str(n);nn=n+int(s[::-1]);gamma.append(len(str(nn))-len(s));n=nn
    target=word(J,U,C,q,k+5);got=pair(n)
    first=next((i for i,(a,b) in enumerate(zip(got,target)) if a!=b),min(len(got),len(target)))
    return {'q':q,'k':k,'return':got==target,'first_mismatch':first,
            'overflow_sum':sum(gamma),
            'overflow':''.join(map(str,gamma)) if trace else None,
            'len':len(got),'target_len':len(target)}
if __name__=='__main__':
    for q,k in [(14,100),(20,80),(40,160),(80,320),(160,640)]:
        for J in [(0,0,0,0,0,0),(0,1,2,3,4,5)]:
            print(run(J,rotations()[0],(4,4),q,k,trace=True))

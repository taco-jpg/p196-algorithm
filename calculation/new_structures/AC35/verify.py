#!/usr/bin/env python3
"""Independent schoolbook physical-digit versus Python bigint reverse-add."""
import random
from scan import rotations,word,realize,pair,run
def source_digits(P):
    D=[0]*len(P)
    for i in range(len(P)//2):
        D[i]=P[i]-min(9,P[i]);D[-i-1]=min(9,P[i])
    if len(P)%2:
        assert P[len(P)//2]%2==0
        D[len(P)//2]=P[len(P)//2]//2
    assert D[-1]>0
    return D
def digitstep(D):
    out=[];carry=0;size=len(D)
    for i in range(size):
        z=D[i]+D[size-1-i]+carry
        out.append(z%10);carry=z//10
    if carry:out.append(carry)
    return out
def check(J,U,C,q,k):
    P=word(J,U,C,q,k);D=source_digits(P);n=realize(P)
    assert int(''.join(map(str,D[::-1])))==n
    gamma=[]
    for t in range(120):
        prev=len(D);D=digitstep(D)
        text=str(n);n+=int(text[::-1])
        assert D==[int(x) for x in str(n)[::-1]],(J,U,C,q,k,t)
        gamma.append(len(D)-prev)
    target=word(J,U,C,q,k+5);got=pair(n)
    first=next((i for i,(a,b) in enumerate(zip(got,target)) if a!=b),min(len(got),len(target)))
    other=run(J,U,C,q,k)
    assert first==other['first_mismatch'] and sum(gamma)==other['overflow_sum']
    return first
if __name__=='__main__':
    rng=random.Random(3535)
    controls=[(0,0,0,0,0,0),(0,1,2,3,4,5),(0,18,18,18,18,18)]
    c=78742;J=[0]*6
    for p in range(5,0,-1):J[p]=c%19;c//=19
    controls.append(tuple(J))
    controls.extend(tuple([0]+[rng.randrange(19) for _ in range(5)]) for _ in range(3))
    for J in controls:
        for U in (rotations()[0],rotations()[14],rotations()[29]):
            for C in ((4,4),(4,14,4)):
                for q,k in ((14,100),(20,80),(40,160),(80,320),(160,640)):
                    check(J,U,C,q,k)
    print('PASS: 7 J x3 U x2 C x5 widths x120 physical digit-array/bigint checks = 25200')

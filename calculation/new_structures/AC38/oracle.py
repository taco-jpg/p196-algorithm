#!/usr/bin/env python3
"""Independent canonical source integer vs schoolbook pairword comparison."""
import random
import sys
from pathlib import Path
from guard import load_exterior
if hasattr(sys,"set_int_max_str_digits"):sys.set_int_max_str_digits(0)

def make_pair(B,W,J,U,C,q,k):
    h=B+W*q+J+U*k
    p=h+C+h[::-1]
    assert p==p[::-1] and all(0<=x<=18 for x in p)
    return p

def source_digits(p):
    n=len(p);d=[0]*n
    for i in range(n//2):
        v=p[i];d[i]=max(0,v-9);d[n-i-1]=min(v,9)
    if n%2:
        assert p[n//2]%2==0
        d[n//2]=p[n//2]//2
    assert d[-1]>0
    return d

def pair_of(n):
    d=list(map(int,str(n)[::-1]))
    return [d[i]+d[-i-1] for i in range(len(d))]

def digit_step(p):
    carry=0;d=[]
    for x in p:
        v=x+carry;d.append(v%10);carry=v//10
    if carry:d.append(carry)
    return [d[i]+d[-i-1] for i in range(len(d))]

def verify(B,W,J,U,C,q,k):
    p=make_pair(B,W,J,U,C,q,k)
    n=int("".join(map(str,source_digits(p)[::-1])))
    assert pair_of(n)==p
    initial=len(p)
    for t in range(120):
        old=n;n+=int(str(n)[::-1]);p=digit_step(p)
        assert n>old and pair_of(n)==p,(t,J,U,C,q,k)
    target=make_pair(B,W,J,U,C,q,k+5)
    bad=next((i for i,(x,y) in enumerate(zip(p,target)) if x!=y),None)
    return bad,len(p)-initial,p[8],target[8],p==target

if __name__=="__main__":
    B,W=load_exterior(Path(sys.argv[1]))
    rng=random.Random(38005);total=0;hist={}
    for q,k in ((14,100),(20,80),(40,160),(80,320),(160,640)):
        for a in (0,4,8,12,18):
            base=[9,a,18-a];rot=a%3;U=base[rot:]+base[:rot]
            for parity in (0,1):
                C=[4,4] if parity==0 else [4,14,4]
                J=[0]+[rng.randrange(19) for _ in range(5)]
                bad,growth,p8,t8,eq=verify(B,W,J,U,C,q,k)
                assert growth==30 and p8==t8==11 and not eq
                assert bad>=34+9*q-26
                hist[bad-(34+9*q)]=hist.get(bad-(34+9*q),0)+1
                total+=1
        print("verified",q,k,"10 controls x 120 integer transitions",flush=True)
    print("TOTAL",total,"cut-relative first mismatches",sorted(hist.items()))

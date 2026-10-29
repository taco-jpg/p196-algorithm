#!/usr/bin/env python3
"""Independent true Python bigint vs LSD schoolbook physical 120-step controls."""
from pathlib import Path
import random,sys
sys.set_int_max_str_digits(0)
LATTICE=Path(__file__).resolve().parents[3]/'calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt'

def bw():
    r=[[int(x) for x in s.split()] for s in LATTICE.read_text().splitlines()]
    assert r[0]==[12,34,9,10]
    return r[27],r[3]

def realize(P):
    assert P==P[::-1]
    d=[0]*len(P)
    for i in range(len(P)//2):
        d[i]=max(0,P[i]-9);d[-i-1]=min(9,P[i])
    if len(P)%2:
        assert P[len(P)//2]%2==0
        d[len(P)//2]=P[len(P)//2]//2
    assert d[-1]!=0
    return d

def schoolbook(d):
    c=0;out=[]
    for i in range(len(d)):
        z=d[i]+d[-1-i]+c
        out.append(z%10);c=z//10
    if c:out.append(c)
    return out

def bigint(d):return int(''.join(map(str,d[::-1])))

def check(J,U,C,q,k):
    B,W=bw();h=B+W*q+J+U*k
    d=realize(h+C+h[::-1]);n=bigint(d);g=[]
    for t in range(120):
        old=len(d)
        d=schoolbook(d)
        n+=int(str(n)[::-1])
        assert bigint(d)==n,(t,q,k,J,U,C)
        g.append(len(d)-old)
    assert ''.join(map(str,g))=='0001'*30
    P=[d[i]+d[-1-i] for i in range(len(d))]
    h=B+W*q+J+U*(k+5)
    target=h+C+h[::-1]
    first=next((i for i,(x,y) in enumerate(zip(P,target)) if x!=y),None)
    if first is None and len(P)!=len(target):first=min(len(P),len(target))
    assert first is not None
    return first

def main():
    r=random.Random(76196)
    for q,k in [(14,100),(20,80),(40,160),(80,320),(160,640)]:
        for t in range(3):
            J=[1]+[r.randrange(19) for _ in range(5)]
            a=r.randrange(0,19,2);U=[9,a,18-a];s=r.randrange(3);U=U[s:]+U[:s]
            C=([4,4],[4,14,4])[t%2]
            print('PASS',q,k,'J',J,'U',U,'C',C,'first',check(J,U,C,q,k))
    print('15 independent 120-step bigint/digit-list controls: PASS')

if __name__=='__main__':main()

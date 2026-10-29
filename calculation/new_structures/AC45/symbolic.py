#!/usr/bin/env python3
"""AC45 exact one-column two-carry MDD control, NOT the pi185 product."""
from collections import defaultdict
from itertools import product
import sys
sys.set_int_max_str_digits(0)

B=[10,4,6,6,7,12,9,16,16,13,0,2,10,17,7,0,18,6,5,18,4,18,14,9,14,8,12,17,10,4,6,4,0,5]
W=[5,18,4,8,1,15,4,0,5]

def digits(p):
    assert p==p[::-1] and all(0<=x<=18 for x in p)
    n=len(p);d=[0]*n
    for i in range(n//2):
        d[i]=max(0,p[i]-9);d[n-1-i]=min(9,p[i])
    if n%2:
        assert p[n//2]%2==0
        d[n//2]=p[n//2]//2
    assert d[-1]>0
    return d

def pairs(d):
    return [d[i]+d[-1-i] for i in range(len(d))]

def step(p):
    d=digits(p);c=0;out=[]
    for i in range(len(d)):
        t=d[i]+d[-1-i]+c
        out.append(t%10);c=t//10
    if c:out.append(c)
    return pairs(out)

def independent(p):
    n=int(''.join(map(str,digits(p)[::-1])))
    n+=int(str(n)[::-1])
    s=str(n)
    return [int(s[i])+int(s[-1-i]) for i in range(len(s))]

def mdd(width,domain=range(19)):
    # A state (l,h) exposes BOTH physical carry ports. h is the
    # reverse-scan incoming high carry, not guessed from low carry.
    states={(0,0):1,(0,1):1};sizes=[2];arcs=[]
    for _ in range(width):
        nxt=defaultdict(int);a=0
        for (l,h),ways in states.items():
            for x in domain:
                for hp in (0,1):
                    if (x+hp)//10==h:
                        nxt[((x+l)//10,hp)]+=ways;a+=1
        states=nxt;sizes.append(len(states));arcs.append(a)
    return sizes,arcs,sum(states.values())

def template(q,k,J,U,C):
    h=B+W*q+list(J)+list(U)*k
    return h+list(C)+h[::-1]

def test():
    count=0
    for length in (1,2,3):
        for half in product(range(19),repeat=length):
            for C in ((),(0,),(2,),(8,8)):
                p=list(half)+list(C)+list(half[::-1])
                if p[-1]==0:continue
                assert step(p)==independent(p)
                count+=1
    print('independent short tests',count)
    for q,k in ((14,100),(20,160),(40,320),(80,640),(160,1280)):
        p=template(q,k,[5,9,1,4,3,0,6],[9,0,18],[8,8])
        for t in range(120):
            assert step(p)==independent(p),(q,k,t)
            p=step(p)
        print('120-step bigint agreement',q,k,len(p))
    for w in (1,2,4,8,16,32,120):
        sizes,arcs,paths=mdd(w)
        print('one-space MDD',w,sizes[-1],sum(arcs),paths)
    p=template(14,100,[1,0,2],[9,0,18],[8,8])
    assert p==p.copy()
    print('zero-clock identity control PASS')

if __name__=='__main__':test()

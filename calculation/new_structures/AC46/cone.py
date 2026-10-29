#!/usr/bin/env python3
"""Exact two-inlet central cone for a prescribed 120-bit physical clock.
The theorem is a sound over-approximation for any unknown exterior.
"""
from collections import Counter
from itertools import product
B=(10,4,6,6,7,12,9,16,16,13,0,2,10,17,7,0,18,6,5,18,4,18,14,9,14,8,12,17,10,4,6,4,0,5)
W=(5,18,4,8,1,15,4,0,5)

def normalize(w,c):
    d=[]
    for x in w:
        z=x+c; d.append(z%10);c=z//10
    return d,c

def outer_clock(q=14,steps=120):
    p=list(B+W*q);clock=[];lengths=[len(p)]
    for t in range(steps):
        n=len(p);d,_=normalize(p,0)
        a,g0=normalize(p[::-1],0)
        b,g1=normalize(p[::-1],1)
        assert g0==g1,(t,n,g0,g1)
        g=g0;clock.append(g)
        if g:
            lo=[d[0]+1]+[d[i]+a[n-i] for i in range(1,n)]
            hi=[d[0]+1]+[d[i]+b[n-i] for i in range(1,n)]
        else:
            lo=[d[i]+a[n-1-i] for i in range(n)]
            hi=[d[i]+b[n-1-i] for i in range(n)]
        j=next((i for i in range(n) if lo[i]!=hi[i]),n)
        p=lo[:j];lengths.append(len(p))
        assert p,(t,'empty prefix')
    assert clock==[1,0,0,0]*30,(clock[:20],sum(clock))
    return clock,lengths

def centre_step(s,g):
    n=len(s)
    d0,_=normalize(s,0);d1,_=normalize(s,1)
    out0=[d0[g+j]+d0[n-1-j] for j in range(n-g)]
    out1=[d1[g+j]+d1[n-1-j] for j in range(n-g)]
    assert out0==out0[::-1] and out1==out1[::-1]
    trim=max((min(j,n-g-1-j)+1 for j,(x,y) in enumerate(zip(out0,out1)) if x!=y),default=0)
    return out0[trim:n-g-trim],g+trim

def iterate(U,C,k=100,clock=None):
    if clock is None:clock=[1,0,0,0]*30
    s=list(U)*k+list(C)+list(U[::-1])*k
    sizes=[len(s)];shift=0
    for t,g in enumerate(clock):
        s,cut=centre_step(s,g)
        assert s and s==s[::-1],(t,'centre destroyed')
        sizes.append(len(s));shift+=cut
    return s,shift,sizes

def us():
    return [tuple((9,a,18-a)[r:]+(9,a,18-a)[:r]) for a in range(0,19,2) for r in range(3)]

def window(s,n):
    i=(len(s)-n)//2
    assert i>=1
    return tuple(s[i-1:i+n+1])

def check(L=1):
    clock,p=outer_clock()
    print('outer',p[0],p[-1],sum(clock))
    hist=Counter();hits=[];mincore=10000
    for length in range(1,L+1):
        half=(length+1)//2
        for a in product(range(19),repeat=half):
            C=a+a[::-1] if length%2==0 else a+a[-2::-1]
            if length%2 and C[length//2]%2:continue
            for U in us():
                s,shift,sizes=iterate(U,C,clock=clock)
                want=(U[-1],)+C+(U[-1],)
                got=window(s,length)
                ishit=(got==want)
                hist[(length,ishit)]+=1
                mincore=min(mincore,len(s))
                if ishit:hits.append((U,C,shift,got))
        print('length',length,'total',hist[(length,False)]+hist[(length,True)],'hits',hist[(length,True)],'mincore',mincore,'example',hits[:3])
    return hist,hits

if __name__=='__main__':
    import sys
    if '--clock' in sys.argv:
        clk,lengths=outer_clock()
        print('PASS phase-0 physical clock', ''.join(map(str,clk)), 'prefix',lengths[0],lengths[-1])
    else:
        check(int(sys.argv[1]) if len(sys.argv)>1 else 2)

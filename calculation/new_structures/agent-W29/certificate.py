#!/usr/bin/env python3
"""W29 all-base carry-spectrum band quotients: F^3=F and U^4=U^2."""
from random import Random

def states(b): return [(c,x) for c in (0,1) for x in range(-1,b)]
def ident(b): return {(c,x):(c,x,0) for c,x in states(b)}
def edge(a,d,b):
    return 0 if a<0 or a==d else 1 << (min(a,d)*b+max(a,d))
def atom(p,b,kind):
    out={}
    for c,last in states(b):
        digit=(p+c)%b
        mask=(1<<digit) if kind=='hist' else edge(last,digit,b)
        out[c,last]=((p+c)//b,last if kind=='hist' else digit,mask)
    return out
def compose(f,g):
    return {key:(g[c,x][0],g[c,x][1],z^g[c,x][2]) for key,(c,x,z) in f.items()}
def trans(w,b,kind):
    f=ident(b)
    for p in w:
        assert 0<=p<=2*b-2
        f=compose(f,atom(p,b,kind))
    return f
def power(f,k,b):
    v=ident(b)
    while k:
        if k&1:v=compose(v,f)
        f=compose(f,f);k>>=1
    return v
def mask(w,b,kind):
    c,last,z=trans(w,b,kind)[0,-1]
    if c:z ^= (1<<1) if kind=='hist' else edge(last,1,b)
    return z
def normal(w,b):
    out=[];c=0
    for p in w:
        s=p+c;out.append(s%b);c=s//b
    if c:out.append(1)
    return out
def direct_mask(d,b,kind):
    if kind=='hist':
        x=0
        for a in d:x^=1<<a
        return x
    x=0
    for a,z in zip(d,d[1:]):x^=edge(a,z,b)
    return x

def check():
    rng=Random(290475)
    for b in (2,3,9,10,13,26,146):
        for _ in range(140):
            w=[rng.randrange(2*b-1) for _ in range(rng.randrange(1,13))]
            h=trans(w,b,'hist');u=trans(w,b,'edge')
            assert power(h,3,b)==h
            assert power(u,4,b)==power(u,2,b)
            for k in (1,2,3,4,5,8):
                assert trans(w*k,b,'hist')==power(h,k,b)
                assert trans(w*k,b,'edge')==power(u,k,b)
            test=[rng.randrange(2*b-1) for _ in range(25)]
            for kind in ('hist','edge'):
                assert mask(test,b,kind)==direct_mask(normal(test,b),b,kind)
    for b in (2,10):
        for i in range(500):
            h=[rng.randrange(b) for _ in range(rng.randrange(1,10))]
            p=h+([rng.randrange(b)] if i%2 else [])+h[::-1]
            assert direct_mask(p,b,'edge')==0
            assert direct_mask(p,b,'hist').bit_count()<=1
    L,W,C=[4,18],[10,12,12],[0]
    hs=[];es=[]
    for k in (1,2,3):
        p=L+W*k+C+W[::-1]*k+L[::-1]
        assert p==p[::-1] and all(x%2==0 for x in p)
        hs.append(mask(p,10,'hist'));es.append(mask(p,10,'edge'))
    assert hs==[830]*3 and es==[576742227289321472]*3
    for k in (1,2,3,4,5,12,99,500):
        p=L+W*k+C+W[::-1]*k+L[::-1]
        q=1 if k==1 else 2+k%2
        assert mask(p,10,'edge')==mask(L+W*q+C+W[::-1]*q+L[::-1],10,'edge')
        n=len(p);d=[0]*n
        for i in range(n//2):
            d[i]=0 if i==0 else min(9,p[i]);d[n-1-i]=p[i]-d[i]
        d[n//2]=0
        assert d[-1]>0 and d!=d[::-1]
        N=int(''.join(map(str,d[::-1])));N2=N+int(str(N)[::-1])
        r=list(map(int,str(N2)[::-1]))
        assert direct_mask(r,10,'edge')==es[0] and r!=r[::-1]
    print('PASS: 980 all-base blocks, 1000 palindrome controls, and universal decimal family')
if __name__=='__main__':check()

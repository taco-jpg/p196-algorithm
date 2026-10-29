#!/usr/bin/env python3
"""Universal reversal-orbit h-gram parity quotient: T_w^(h+2)=T_w^h."""
from random import Random

def words(b,h):
    for q in range(h):
        for i in range(b**q):
            yield tuple((i//(b**j))%b for j in range(q))
def states(b,h):return [(c,x) for c in (0,1) for x in words(b,h)]
def atom(a,b,h):
    out={}
    for c,s in states(b,h):
        d=(a+c)%b
        w=s+(d,)
        new=w[-(h-1):]
        if len(w)==h and w!=w[::-1]:
            u=min(w,w[::-1]);idx=0
            for x in u:idx=idx*b+x
            v=1<<idx
        else:v=0
        out[c,s]=((a+c)//b,new,v)
    return out
def ident(b,h):return {(c,s):(c,s,0) for c,s in states(b,h)}
def compose(f,g):return {key:(g[c,s][0],g[c,s][1],mask^g[c,s][2]) for key,(c,s,mask) in f.items()}
def trans(word,b,h):
    f=ident(b,h)
    cache={a:atom(a,b,h) for a in set(word)}
    for a in word:f=compose(f,cache[a])
    return f
def power(f,k,b,h):
    g=ident(b,h)
    while k:
        if k&1:g=compose(g,f)
        f=compose(f,f);k//=2
    return g
def spec(d,b,h):
    mask=0
    for i in range(len(d)-h+1):
        w=tuple(d[i:i+h]);r=w[::-1]
        if w!=r:
            n=0
            for x in min(w,r):n=n*b+x
            mask^=1<<n
    return mask
def normalize(p,b):
    c=0;d=[]
    for x in p:
        s=x+c;d.append(s%b);c=s//b
    if c:d.append(1)
    return d
def out_spec(p,b,h):
    c,tail,mask=trans(p,b,h)[0,()]
    if c:
        w=tail+(1,)
        if len(w)==h and w!=w[::-1]:
            n=0
            for x in min(w,w[::-1]):n=n*b+x
            mask^=1<<n
    return mask
def check():
    rng=Random(290476);tested=0
    for b,h,trials in [(2,3,350),(3,3,350),(9,3,100),(10,3,100),(2,4,150),(3,4,150),(10,2,100),(2,5,120),(3,5,80)]:
        for _ in range(trials):
            w=[rng.randrange(2*b-1) for i in range(rng.randrange(1,7))]
            f=trans(w,b,h)
            assert power(f,h+2,b,h)==power(f,h,b,h),(b,h,w)
            for k in (1,2,3,h,h+1,h+4):
                assert power(f,k,b,h)==trans(w*k,b,h)
            p=[rng.randrange(2*b-1) for i in range(15)]
            assert out_spec(p,b,h)==spec(normalize(p,b),b,h)
            tested+=1
    print('PASS universal kgram quotient cases',tested)
    n=[1,2,3,1,2,3,1]
    digitmask=0
    for x in n:digitmask^=1<<x
    assert digitmask.bit_count()==1
    assert spec(n,10,2)==0 and spec(n,10,3)!=0 and n!=n[::-1]
    print('STRICT GAIN: 1231231 passes histogram and 2-gram obstructions but fails 3-gram')
    L,W,C=[2,8,12,4,12,6,16],[8,12],[8]
    witnesses=[]
    for k in (1,2,3,4):
        p=L+W*k+C+W[::-1]*k+L[::-1]
        d=normalize(p,10)
        hist=0
        for x in d:hist^=1<<x
        assert p==p[::-1] and all(x%2==0 for x in p)
        assert hist.bit_count()==1 and spec(d,10,2)==0
        e3=out_spec(p,10,3)
        assert e3==spec(d,10,3) and e3.bit_count()==2
        witnesses.append(e3)
    assert len(set(witnesses))==1
    for k in (1,2,3,4,5,8,30,1000):
        p=L+W*k+C+W[::-1]*k+L[::-1]
        assert out_spec(p,10,3)==witnesses[0]
        n=len(p);d=[0]*n
        for i in range(n//2):
            d[i]=0 if i==0 else min(9,p[i])
            d[n-1-i]=p[i]-d[i]
        d[n//2]=p[n//2]//2
        assert d[-1]>0 and d!=d[::-1]
        S=''.join(map(str,d[::-1]))
        actual=int(S)+int(S[::-1])
        output_digits=list(map(int,str(actual)[::-1]))
        assert output_digits==normalize(p,10)
        assert spec(output_digits,10,3)==witnesses[0]
        assert output_digits!=output_digits[::-1]
    print('ALL-k family: even pair coefficients, histogram <=1, 2-gram zero, 3-gram parity two bits (5,2,8),(5,2,9); big-int k<=1000 PASS')
if __name__=='__main__':check()

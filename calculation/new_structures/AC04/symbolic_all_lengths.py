#!/usr/bin/env python3
"""A proved symbolic carry-mask pumping checker for every palindromic C length >=7.
The unknown central A^K band is a supersets-of-values abstraction; only
forcefully missing endpoint digits justify a negative result.
"""
from functools import lru_cache
from centre_scan_data import B,W,U
ALL=(1<<19)-1
FULL=(1<<10)-1

@lru_cache(maxsize=None)
def norm(p,c):
    d=0;co=0;x=p
    while x:
        lb=x&-x;v=lb.bit_length()-1;x-=lb
        y=c
        while y:
            lb=y&-y;z=lb.bit_length()-1;y-=lb
            n=v+z;d|=1<<(n%10);co|=1<<(n//10)
    return d,co

@lru_cache(maxsize=None)
def add(a,b):
    out=0;x=a
    while x:
        lb=x&-x;i=lb.bit_length()-1;x-=lb
        y=b
        while y:
            lb=y&-y;j=lb.bit_length()-1;y-=lb
            out|=1<<(i+j)
    return out

def step(X,K):
    # Exact masked normalization of X A^K reverse(X) for EVERY K>=1.
    dL=[];c=1
    for v in X:
        z,c=norm(v,c);dL.append(z)
    dcore,c=norm(ALL,c)
    assert dcore==FULL and c==3
    dR=[]
    for v in reversed(X):
        z,c=norm(v,c);dR.append(z)
    if c not in (1,2):return None
    gamma=(c==2)
    x=len(X)
    if not gamma:
        X2=[add(dL[i],dR[x-1-i]) for i in range(x)]
        K2=K
    else:
        X2=[add(dL[0],1<<1)]
        for i in range(1,x):
            X2.append(add(dL[i],dR[x-i]))
        X2.append(add(FULL,dR[0]))
        K2=K-1
    while X2 and X2[-1]==ALL:
        X2.pop();K2+=2
    return X2,K2,int(gamma)

def scan(ui,a,b):
    h=B+W*14+[5]+U[ui]*100
    X=[1<<v for v in h+[a,b]]
    K=3  # arbitrary C length L>=7 corresponds to K0=L-4>=3
    minK=K
    for t in range(120):
        if K<1:return False,None,minK,'CORE_EXHAUSTED'
        s=step(X,K)
        if s is None:return False,None,minK,'AMBIGUOUS_GAMMA'
        X,K,g=s
        if g!=int(t%4==0):return False,None,minK,'CLOCK'
        minK=min(K,minK)
    cut=len(h)+15
    assert cut-1 < len(X)+K, 'left-collar overlaps right symbolic boundary'
    fail=[]
    for i in range(cut-150,cut):
        want=U[ui][(i-(len(h)-300))%3]
        mask=X[i] if i<len(X) else ALL
        if not(mask & (1<<want)):
            fail.append(i-cut)
    return True,fail,minK,'OK'

if __name__=='__main__':
    for ui in range(3):
        reject=0;uncertain=0;minK=99;histogram={};bad=[]
        for b in range(19):
            for a in range(19):
                ok,fail,k,status=scan(ui,a,b)
                if not ok:bad.append((a,b,status))
                else:
                    minK=min(minK,k)
                    if fail:
                        reject+=1
                        histogram[fail[0]]=histogram.get(fail[0],0)+1
                    else:uncertain+=1
        print('ALL-LENGTH-SYMBOLIC U',ui,'prefixes',361,'rejected',reject,
              'unresolved',uncertain,'invalid',len(bad),'K_min',minK,
              'mismatch_histogram',histogram,flush=True)
        assert not bad
        assert (reject,uncertain)==[(228,133),(25,336),(82,279)][ui]
        assert minK>=1
    print('PASS all C lengths >=7 in sound abstract domain')
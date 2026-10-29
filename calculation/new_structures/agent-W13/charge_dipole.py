#!/usr/bin/env python3
"""W13: exact base-10 charge-neutral arbitrarily long corridor -> 2 particles -> erasure."""
from itertools import product
from random import Random
import json,sys
sys.path.insert(0,__file__.rsplit('/',1)[0])
from three_step_eraser import next_pair,pair,literal_step

def root(h):
    assert h>=50
    half=[17]+[(4 if i%3==1 else 1) for i in range(1,h)]
    return half+half[::-1]

def patch(p,a,k):
    assert a>=30 and a%3==2 and k>=1
    b=a+6*k+3
    assert b+20<=len(p)//2
    q=p[:]
    change=[3,4,3]+[2,0,5,0,2,3]*k+[4,3,4]
    assert len(change)==b+3-a
    for j,val in enumerate(change,a):
        assert p[j] in (1,4)
        q[j]=q[-j-1]=val
    return q

def digit_lift(p):
    assert p==p[::-1] and len(p)%2==0
    d=[0]*len(p)
    for i in range(len(p)//2):
        d[i]=min(9,p[i]);d[-i-1]=p[i]-d[i]
    assert d[-1]!=0 and pair(d)==p
    return d

def check(h,a,k,verbose=False):
    A=root(h);B=patch(A,a,k); b=a+6*k+3
    A1=next_pair(A);B1=next_pair(B)
    diffs=[j for j in range(len(A1)//2) if A1[j]!=B1[j]]
    assert diffs==[a,a+1,a+2,b,b+1,b+2],(k,diffs)
    assert A1[a:a+3]==[5,2,5] and A1[b:b+3]==[5,2,5]
    assert B1[a:a+3]==[7,7,7] and B1[b:b+3]==[7,7,7]
    Acur=A;Bcur=B;supports=[];odd=[]
    for t in range(6):
        diffs=[j for j in range(len(Acur)//2) if Acur[j]!=Bcur[j]]
        supports.append((t,len(diffs), (diffs[0],diffs[-1]) if diffs else []))
        odd.append(next(i for i in range(25) if Acur[i]%2))
        if t==5:assert not diffs
        if t<5:Acur,Bcur=next_pair(Acur),next_pair(Bcur)
    assert odd==[0,2,0,4,0,3],odd
    # Ordinary-digit arithmetic and completely separate Python bigint reversal.
    da=digit_lift(A);db=digit_lift(B)
    na=int(''.join(map(str,da[::-1])));nb=int(''.join(map(str,db[::-1])))
    for t in range(7):
        assert str(na)==''.join(map(str,da[::-1]))
        assert str(nb)==''.join(map(str,db[::-1]))
        assert str(na)!=str(na)[::-1] and str(nb)!=str(nb)[::-1]
        if t==5:assert pair(da)==pair(db)
        if t==6:assert na==nb and da==db
        if t<6:
            da=literal_step(da);db=literal_step(db)
            na+=int(str(na)[::-1]);nb+=int(str(nb)[::-1])
    return {'k':k,'h':h,'a':a,'b':b,'corridor_coefficients':6*k+6,
            'pair_merge_t':5,'integer_merge_t':6,'supports':supports}

def multi(h,sites,pattern):
    p=root(h)
    for (a,k),bit in zip(sites,pattern):
        if bit:p=patch(p,a,k)
    return p

def verify():
    sys.set_int_max_str_digits(0)
    ks=[1,2,3,4,5,10,20,50,100,300,1000,2000]
    compact=check(80,32,1)
    runs=[check(max(600,200+6*k+3+70),200,k) for k in ks]
    sites=[(200,1),(500,2),(800,4),(1100,6)]
    base=multi(1500,sites,(0,0,0,0));T=base
    for _ in range(5):T=next_pair(T)
    for pattern in product((0,1),repeat=len(sites)):
        p=multi(1500,sites,pattern)
        for _ in range(5):p=next_pair(p)
        assert p==T
    rng=Random(20261028)
    checked=0;bigint_end=None
    for _ in range(16):
        pat=tuple(rng.randrange(2) for _ in sites)
        p=multi(1500,sites,pat)
        d=digit_lift(p);n=int(''.join(map(str,d[::-1])))
        for t in range(7):
            assert str(n)==''.join(map(str,d[::-1]))
            if t<6:
                d=literal_step(d);n+=int(str(n)[::-1])
        if bigint_end is None:bigint_end=n
        else:assert n==bigint_end
        checked+=1
    return {'label':'PAPER PROOF for all k>=1 + COMPUTED exact controls',
            'base':10,'dipole_start':200,'separations_checked':[6*k+3 for k in ks],
            'max_corridor_len':6*max(ks)+6,'sample_replay':runs,'compact_160digit_pair':compact,
            'compact_baseline_seed':''.join(map(str,digit_lift(root(80))[::-1])),
            'compact_dipole_seed':''.join(map(str,digit_lift(patch(root(80),32,1))[::-1])),
            'independent_2pow4_exact_checks':16,'independent_bigint_variants':checked,
            'ordinary_integer_merge_step':6,
            'infinite_lychrel_certificate':False}

if __name__=='__main__':print(json.dumps(verify(),indent=2))

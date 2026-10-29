#!/usr/bin/env python3
"""Independently check phase-9 pair coefficients and 240 true-decimal steps.

No success is inferred from these finite controls; the theorem comes from
mod-11 arithmetic and the full exact residue DP, not replay.
"""
from __future__ import annotations
import random
import sys
from phase9_gate import (B9,W9,ODD_C,EVEN_C,alternating,pair,a_formula,
                         words_u,gate,mod11_dp)
if hasattr(sys,'set_int_max_str_digits'):sys.set_int_max_str_digits(0)


def realize(p):
    assert p==p[::-1]
    digits=[0]*len(p)
    for i in range(len(p)//2):
        hi=min(9,p[i]); lo=p[i]-hi
        assert 0<=lo<=9
        digits[i]=lo;digits[-1-i]=hi
    if len(p)%2:
        assert p[len(p)//2]%2==0
        digits[len(p)//2]=p[len(p)//2]//2
    assert digits[-1]>0
    return digits


def decimal_step(d):
    nxt=[];carry=0
    for i in range(len(d)):
        s=d[i]+d[-1-i]+carry
        nxt.append(s%10);carry=s//10
    if carry:nxt.append(carry)
    return nxt


def as_int(d):
    return int(''.join(str(x) for x in d[::-1]))


def check(J,U,C,q,k,steps=240):
    p=pair(B9,W9,J,U,C,q,k)
    d=realize(p);n=as_int(d)
    assert [d[i]+d[-1-i] for i in range(len(d))]==p
    over=[]; returns=[]; mismatches=[]
    # Independent arithmetic: Python bigint n+int(str(n)[::-1]),
    # compared every step to a separate fixed-source schoolbook digit array.
    for t in range(steps):
        oldlen=len(d)
        d=decimal_step(d)
        n+=int(str(n)[::-1])
        assert n==as_int(d), (q,k,J,U,C,t)
        over.append(len(d)-oldlen)
        if t in (119,239):
            assert sum(over[:t+1])==(t+1)//4,('length-clock',t)
            assert n%11==0,(t,n%11)
            pcur=[d[i]+d[-1-i] for i in range(len(d))]
            assert alternating(pcur)%11==0
            target=pair(B9,W9,J,U,C,q,k+(t+1)//24)  # 120 -> +5, 240 -> +10
            eq=(pcur==target)
            m=next((i for i,(x,y) in enumerate(zip(pcur,target)) if x!=y),min(len(pcur),len(target)))
            returns.append(eq);mismatches.append(None if eq else m)
    assert over==[0,0,0,1]*(steps//4), over[:20]
    return {'q':q,'k':k,'steps':steps,'overflow_sum':sum(over),
            'Nmod11_240':n%11,'digits':len(d),
            'returns_120_240':returns,'mismatches_120_240':mismatches}


def test_modular_dp():
    allowed,res=gate()
    a,n=mod11_dp(j0=0,residue=res)
    brute=[0]*11
    # Independent bounded combinatorial cross-check of the DP, length 3.
    from itertools import product
    small,_=mod11_dp(junction_len=3,j0=0,residue=res)
    for x,y in product(range(19),repeat=2):
        brute[(-x+y)%11]+=1
    assert small==brute
    assert n==225117
    assert len(words_u())==len(set(words_u()))==30
    assert allowed==[(1,(9,0,18)), (29,(18,0,9))]
    return True


def test_alternating_formula():
    rng=random.Random(20261029)
    for _ in range(1000):
        J=[rng.randrange(19) for _ in range(6)]
        U=rng.choice(words_u())
        q=rng.randrange(14,23);k=rng.randrange(100,110)
        actual=alternating(pair(B9,W9,J,U,ODD_C,q,k))
        predicted=a_formula(B9,W9,J,U,ODD_C,q,k)
        assert actual==predicted
        # Even palindromic centre removes odd-C gate entirely.
        assert alternating(pair(B9,W9,J,U,EVEN_C,q,k))==0
    return True


def main():
    test_modular_dp()
    print('Exact DP small brute-control and 1000 formula trials:',test_alternating_formula())
    cases=[([0,0,0,0,0,2],(9,0,18),ODD_C),
           ([0,0,0,0,0,0],(18,0,9),ODD_C),
           ([0,1,2,3,4,5],(9,2,16),ODD_C),
           ([0,0,0,0,0,9],(9,2,16),EVEN_C)]
    widths=[(14,100),(20,80),(40,160),(80,320),(160,640)]
    for J,U,C in cases:
        print('control',J,U,C)
        for q,k in widths:
            print(check(J,U,C,q,k))
    print('ALL INDEPENDENT BIGINT/DIGIT-ARRAY TESTS PASSED')

if __name__=='__main__':main()

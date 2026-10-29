#!/usr/bin/env python3
"""Exact four-impulse carry-erasure for 8 independent switches per period-20 cell.
Run: python3 calculation/new_structures/agent-W06/toggle_family.py
No dependencies; includes independent full-number bigint controls.
"""
import random
import sys
from itertools import product
sys.set_int_max_str_digits(1000000)
B=[17,5,0,1,13,4,14,12,9,8,15,16,17,13,17,9,1,4,4,11,8,16,0,9,14,11,9,11,6,13,18,9,4,7,17,15,9,7,13]
W=[17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13]
TOGGLES={1:12,3:4,5:2,7:12,9:10,12:16,14:5,19:4}
SITES=sorted(TOGGLES)

def make(m,centre,masks):
    assert 1<=m==len(masks) and 0<=centre<=18 and centre%2==0
    h=B.copy()
    for mask in masks:
        assert 0<=mask<256
        a=W.copy()
        for bit,j in enumerate(SITES):
            if mask>>bit&1:a[j]=TOGGLES[j]
        h.extend(a)
    return h+[centre]+h[::-1]

def normalize(pairword):
    digits=[];c=0
    for x in pairword:
        s=x+c;digits.append(s%10);c=s//10
    if c:digits.append(c)
    return digits

def paired(d):return [d[i]+d[len(d)-1-i] for i in range(len(d))]

def split(p):
    d=[0]*len(p)
    for i in range(len(p)//2):
        d[i]=min(9,p[i]);d[len(p)-1-i]=p[i]-d[i]
    d[len(p)//2]=p[len(p)//2]//2
    assert d[0]!=0 and d[-1]!=0
    return d

def check(m,centre,masks,bigint=False):
    plain=make(m,centre,[0]*m)
    alt=make(m,centre,masks)
    assert alt==alt[::-1]
    a,b=normalize(plain),normalize(alt)
    n=len(alt)
    assert len(a)==len(b)==n+1 and a[-1]==b[-1]==1
    impulses={}
    def push(i,x):
        impulses[i]=impulses.get(i,0)+x
        assert impulses[i]!=0,'impulses overlap: not independent'
    for r,mask in enumerate(masks):
        for bit,j in enumerate(SITES):
            if mask>>bit&1:
                x=len(B)+20*r+j;y=n-1-x
                # toggle +9: digit at x loses 1, at x+1 gains 1
                sign=1 if TOGGLES[j]>W[j] else -1
                push(x,-sign);push(x+1,sign)
                push(y,-sign);push(y+1,sign)
    actual={i:y-x for i,(x,y) in enumerate(zip(a,b)) if x!=y}
    assert actual==impulses,(m,centre,masks,actual,impulses)
    assert paired(a)==paired(b)
    assert normalize(paired(a))==normalize(paired(b))
    if bigint:
        def asint(d):return int(''.join(map(str,d[::-1])))
        def R(num):return num+int(str(num)[::-1])
        na,nb=asint(split(plain)),asint(split(alt))
        assert list(map(int,str(R(na))[::-1]))==a
        assert list(map(int,str(R(nb))[::-1]))==b
        assert R(R(na))==R(R(nb))
        # Both initial and step-1 are forced nonpalindromes by their odd pair coefficients.
        assert str(na)!=str(na)[::-1] and str(nb)!=str(nb)[::-1]
        assert str(R(na))!=str(R(na))[::-1] and str(R(nb))!=str(R(nb))[::-1]


def main():
    assert len(SITES)==8 and len(set(SITES))==8
    for j in SITES:
        assert abs(TOGGLES[j]-W[j])==9
        assert W[j]!=9
        assert W[(j-1)%20]!=9 and W[(j+1)%20]!=9
    # The sites are pairwise separated by at least two even across periods.
    cyc=SITES+[SITES[0]+20]
    assert all(v-u>=2 for u,v in zip(cyc,cyc[1:]))
    runs=0
    # Fully exhaust ALL 256 states of one period, including all even centre symbols.
    for C,mask in product(range(0,19,2),range(256)):
        check(1,C,[mask],bigint=(mask in (0,1,33,85,170,255)))
        runs+=1
    rng=random.Random(4740608)
    large=0;bigints=0
    for _ in range(500):
        m=rng.choice((1,2,3,4,5,10,20,80,320,500))
        C=rng.randrange(10)*2
        masks=[rng.randrange(256) for _ in range(m)]
        big=large<30
        check(m,C,masks,bigint=big)
        large+=1;bigints+=big
    # Strong adversarial control: adjacent sites 7,8 (8 isn't certified) interact.
    P=make(3,18,[0]*3)
    h=B+W*3
    a=h.copy();a[len(B)+7]=12;a[len(B)+8]=9
    bad=a+[18]+a[::-1]
    assert paired(normalize(P))!=paired(normalize(bad))
    assert str(56+65)=='121'
    print('COMPUTED W06 toggle controls:',runs,'exhaustive single-block masks;',large,
          'random multi-block masks;',bigints+60,'independent true-bigint cases; adjacent mutant rejected')
    print('PAPER PROOF scope 2^(8M) distinct canonical decimal seeds, for every M>=1 and even centre C in 0..18, all share identical complete first-step pairword and identical second iterate')
if __name__=='__main__':main()

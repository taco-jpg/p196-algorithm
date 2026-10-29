#!/usr/bin/env python3
"""Independent ordinary decimal digit normalization, no cyclic-carry primary import.
The all-q theorem is proved by primary.cpp's carry-port induction; these are controls.
"""
from pathlib import Path
from random import Random

lines=[line.strip() for line in Path(__file__).with_name('controls.txt').read_text().splitlines()
       if line.strip() and not line.lstrip().startswith('#')]
rows=[[int(x) for x in line.split()] for line in lines]
assert list(map(len,rows))==[48,11,20,11]
W0,B6,raw,B0=rows
PATCH=dict(zip(raw[::2],raw[1::2]));assert len(PATCH)==10

def lift(H):
    P=H+H[::-1];digits=[0]*len(P)
    for i,p in enumerate(H):
        assert 0<=p<=18
        digits[i]=max(p-9,0)
        digits[-1-i]=min(p,9)
    assert digits[-1]>0
    return digits

def reverse_add(d):
    # Independent literal ordinary-digit engine, no pairword transition formula.
    carry=0;result=[]
    for i in range(len(d)):
        x=d[i]+d[len(d)-1-i]+carry
        result.append(x%10);carry=x//10
    if carry:result.append(carry)
    return result

def half_pairs(d):
    return [d[i]+d[len(d)-1-i] for i in range((len(d)+1)//2)]

# Independently derive the phase-6 lattice and rooted prefix from SIX genuine
# decimal reverse-and-add operations, rather than reusing primary's cyclic map.
source=lift(B0+W0*6+[10,14,1,10])
for _ in range(6):source=reverse_add(source)
P=half_pairs(source)
assert P[:11]==B6
W6=P[11+2*48:11+3*48]
assert len(W6)==48
print('INDEPENDENT six genuine rooted phase0->phase6 digit normalizations PASS')

rng=Random(0x6302026);checked=0
for q in range(3,13):
    masks=range(1<<(q-2)) if q<=10 else [rng.randrange(1<<(q-2)) for _ in range(120)]
    for mask in masks:
        C=[rng.randrange(19) for _ in range(rng.randrange(0,24))]
        H=B6+W6*q+C;H2=H[:]
        for i in range(1,q-1):
            if mask>>(i-1)&1:
                for j,v in PATCH.items():H2[11+48*i+j]=v
        a,b=lift(H),lift(H2)
        for t in range(6):
            old_len=len(a)
            a,b=reverse_add(a),reverse_add(b)
            assert len(a)==len(b)==old_len+(t%2==0)
            if t<=4:
                assert any(x%2 for x in half_pairs(a)[:11])
                assert any(x%2 for x in half_pairs(b)[:11])
            if t==4:assert half_pairs(a)==half_pairs(b),(q,mask,'pairword t5')
            if t==5:assert a==b,(q,mask,'integer t6')
        checked+=1
print('INDEPENDENT',checked,'literal six-step controls PASS, all masks q<=10')

# A second oracle: Python arbitrary-precision integer N + decimal_reverse(N).
def to_int(d):return int(''.join(map(str,d[::-1])))
def int_step(n):return n+int(str(n)[::-1])
for q in (3,4,5,7):
    C=[1,8,12,0,18]
    H=B6+W6*q+C;H2=H[:]
    for i in range(1,q-1):
        if i%2:
            for j,v in PATCH.items():H2[11+48*i+j]=v
    x,y=to_int(lift(H)),to_int(lift(H2))
    for _ in range(6):x,y=int_step(x),int_step(y)
    assert x==y
print('INDEPENDENT Python bigint 6-step controls PASS')

# Negative control: a wrong shoulder value does NOT merge in the claimed clock.
H=B6+W6*5+[10,14,1,10];H2=H[:]
for j,v in PATCH.items():H2[11+48*2+j]=v
H2[11+48*2+20]=3  # correct emitted value is 2
x,y=lift(H),lift(H2)
for _ in range(6):x,y=reverse_add(x),reverse_add(y)
assert x!=y
print('INDEPENDENT wrong-shoulder negative control PASS')
print('ALL CHECKS PASSED (no decimal all-time Lychrel certificate)')

#!/usr/bin/env python3
"""Full pairword sound bitset-overapproximation for arbitrary centre coefficients.
Every coefficient mask is a superset of real possibilities. The gamma sequence
is an external condition; this NEVER imposes intermediate W9 preservation.
"""
B=[10,4,6,6,7,12,9,16,16,13,0,2,10,17,7,0,18,6,5,18,4,18,14,9,14,8,12,17,10,4,6,4,0,5]
W=[5,18,4,8,1,15,4,0,5]
U=[(9,12,6),(12,6,9),(6,9,12)]
MASK19=(1<<19)-1
G=[1,0,0,0]*30
def bits(x):
    while x:
        i=(x&-x).bit_length()-1
        yield i
        x&=x-1
def norm(p):
    car=1;dig=[]
    for pm in p:
        dc=cc=0
        for x in bits(pm):
            for c in bits(car):
                z=x+c;dc|=1<<(z%10);cc|=1<<(z//10)
        dig.append(dc);car=cc
    return dig,car
def step(p,g):
    d,car=norm(p)
    if not car&(1<<g):raise AssertionError('impossible gamma')
    if g:d.append(1<<1)
    n=len(d);out=[]
    for i in range(n//2):
        m=0
        for a in bits(d[i]):
            for b in bits(d[-i-1]):m|=1<<(a+b)
        out.append(m)
    mid=[sum(1<<(2*a) for a in bits(d[n//2]))] if n%2 else []
    return out+mid+out[::-1]

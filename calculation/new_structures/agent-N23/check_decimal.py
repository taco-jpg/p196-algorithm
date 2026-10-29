#!/usr/bin/env python3
"""Independent decimal-arithmetic check of radix-100 twisted two-edge path."""
import random
def digit_reverse(n):return int(str(n)[::-1])
def dec_block_value(blocks):return int(''.join(str(d).zfill(2) for d in blocks))
for q in range(1001):
    a=int('12'+'99'*(q+2)+'34')
    b=dec_block_value([56]+[99]*(q+1)+[98,55])
    c=int('1'+'12'+'89'+'99'*q+'98'+'20')
    assert a+digit_reverse(a)==b, ('first',q)
    assert b+digit_reverse(b)==c, ('second',q)
    assert a!=digit_reverse(a) and b!=digit_reverse(b) and c!=digit_reverse(c)
print('PASS decimal twisted radix-100 1001 family instances, 2 exact genuine decimal steps each')
r=random.Random(23)
for k in range(3000):
    n=r.randrange(3,50)
    groups=[r.randrange(100) for _ in range(n-1)]+[r.randrange(10,100)]
    v=sum(x*100**i for i,x in enumerate(groups))
    twist=lambda a:int(str(a).zfill(2)[::-1])
    w=sum(twist(groups[n-i-1])*100**i for i in range(n))
    assert w==digit_reverse(v)
print('PASS 3000 independent random base-100 group/reverse conjugacy trials')

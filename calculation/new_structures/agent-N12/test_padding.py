#!/usr/bin/env python3
"""Independent integer-level controls for the central-zero insertion identity."""
from itertools import product
from random import Random

def ra(s):
    return str(int(s) + int(s[::-1]))

def pad(s, count):
    return s[:len(s)//2] + '0'*count + s[len(s)//2:]

def central_zero_width(s):
    pairs = [int(s[i])+int(s[-1-i]) for i in range(len(s)//2)]
    head = max((i+1 for i,p in enumerate(pairs) if p),default=0)
    return len(s)-2*head

def check(s):
    assert s[0] != '0' and central_zero_width(s)>=4
    after=ra(s)
    assert central_zero_width(after)>=central_zero_width(s)-2
    for k in (1,2,3,7):
        padded=pad(s,k)
        assert ra(padded)==pad(after,k), (s,k)
        assert (s==s[::-1]) == (padded==padded[::-1])

count=0
for n in range(6,9):
    for digits in product('0123456789',repeat=n-4):
        s=''.join(digits[:(n-4)//2])+'0000'+''.join(digits[(n-4)//2:])
        if s[0]=='0' or len(s)!=n or central_zero_width(s)<4:continue
        check(s)
        count+=1
rng=Random(1202612)
for _ in range(10000):
    k=rng.randrange(1,15)
    left=str(rng.randrange(10**(k-1),10**k))
    right=''.join(str(rng.randrange(10)) for _ in range(k))
    if rng.randrange(2):right=right[:-1]+'0'
    s=left+'0'*rng.randrange(4,40)+right
    if central_zero_width(s)>=4:
        check(s);count+=1
print(f'PADDING_INTEGER_CONTROLS_PASS examples={count}')

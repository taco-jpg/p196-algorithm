#!/usr/bin/env python3
"""Independent integer and arbitrary ordinary digit-list checks for two-track map."""
from random import Random
from two_track_certificate import twotrack_step,fold,decode,all_positive,mismatch,check_closure

def radix(n,b):
    if not n:return [0]
    out=[]
    while n:out.append(n%b);n//=b
    return out

def value(ds,b):
    v=0
    for d in reversed(ds):v=v*b+d
    return v

def direct(ds,b):
    out=[];carry=0
    for x,y in zip(ds,ds[::-1]):
        q=x+y+carry;out.append(q%b);carry=q//b
    if carry:out.append(carry)
    return out

cases=0
for b in range(2,13):
    for n in range(1,b**4):
        ds=radix(n,b);src,cent=fold(ds)
        nextpairs,nextcentre,g=twotrack_step(src,cent,b)
        out=radix(n+value(ds[::-1],b),b)
        assert out==direct(ds,b)
        assert (nextpairs,nextcentre)==fold(out)
        assert len(out)-len(ds)==g
        cases+=1
rng=Random(707)
for b in (2,3,9,10,11,26,50):
    for i in range(5000):
        length=rng.randrange(1,100)
        ds=[rng.randrange(b) for _ in range(length-1)]+[rng.randrange(1,b)]
        pairs,cent=fold(ds)
        np,nc,g=twotrack_step(pairs,cent,b)
        s=radix(value(ds,b)+value(ds[::-1],b),b)
        assert fold(s)==(np,nc)
        assert len(s)-len(ds)==g
        cases+=1
    assert check_closure(all_positive(b)) is None
    x=check_closure(mismatch(b),True)
    assert x is not None and x[0]=='not_closed'

# 196 step 8: a nonpalindrome *inside* an all-even pair-sum class.
n=196
for i in range(8):
    s=str(n);n+=int(s[::-1])
assert n==1067869
pairs,cent=fold(radix(n,10))
assert pairs==[(9,1),(6,0),(8,6)] and cent==7
assert all((a+b)%2==0 for a,b in pairs)
assert any(a!=b for a,b in pairs)
# Mirror-palindromic realization with identical P: 5377735
pal=5377735
pp,pc=fold(radix(pal,10))
assert pc==cent and [a+b for a,b in pp]==[a+b for a,b in pairs]
assert str(pal)==str(pal)[::-1]
print('PASS: two-track map vs independent bigint + digit-list',cases,'source states; strict separator 1067869 vs 5377735')
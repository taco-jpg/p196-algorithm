#!/usr/bin/env python3
"""W18 exact decimal reversal in radix 10**k groups with a one-block zipper.
Group digits are least-significant first. Run: python3 zipper.py
"""
from random import Random
import sys
if hasattr(sys,'set_int_max_str_digits'):sys.set_int_max_str_digits(1000000)
def blocks(n,k):
    B=10**k
    if n<=0:raise ValueError(n)
    x=[]
    while n:x.append(n%B);n//=B
    return x
def value(x,k):
    B=10**k;n=0
    for a in reversed(x):
        assert 0<=a<B
        n=n*B+a
    return n
def rho(x,k):
    return int(str(x).zfill(k)[::-1])
def zipped_decimal_reverse(x,k):
    """Exact true decimal reversal, not ordinary base-10**k reversal.
    The output block depends on adjacent reversed source blocks and h.
    """
    B=10**k;m=len(x)
    assert m>=1 and x[-1]>0 and all(0<=a<B for a in x)
    h=len(str(x[-1]));assert 1<=h<=k
    a=[rho(z,k) for z in x[:-1]]
    ah=rho(x[-1],h)
    if m==1:return blocks(ah,k)
    c=10**(k-h);power=10**h
    r=[ah+power*(a[-1]%c)]
    for j in range(1,m-1):
        r.append(a[m-1-j]//c+power*(a[m-2-j]%c))
    r.append(a[0]//c)
    while len(r)>1 and r[-1]==0:r.pop()
    return r
def zipped_raa(x,k):
    B=10**k;r=zipped_decimal_reverse(x,k)
    y=[];c=0
    for j in range(max(len(x),len(r))):
        z=(x[j] if j<len(x) else 0)+(r[j] if j<len(r) else 0)+c
        y.append(z%B);c=z//B
    if c:y.append(c)
    while len(y)>1 and y[-1]==0:y.pop()
    return y
def test():
    rng=Random(1818);num=0
    for k in [1,2,3]:
        for n in range(1,10001):
            if k==1 and n>3000:break
            x=blocks(n,k)
            assert value(zipped_decimal_reverse(x,k),k)==int(str(n)[::-1])
            assert value(zipped_raa(x,k),k)==n+int(str(n)[::-1]);num+=1
        for _ in range(14000):
            digits=rng.randrange(1,85)
            s=str(rng.randrange(1,10))+''.join(str(rng.randrange(10)) for _ in range(digits-1))
            n=int(s);x=blocks(n,k)
            assert value(zipped_decimal_reverse(x,k),k)==int(s[::-1])
            assert value(zipped_raa(x,k),k)==n+int(s[::-1]);num+=1
        print('PASS zipper base',10**k,'true decimal arithmetic checks')
    for k in [2,3]:
        n=int('5'+'99'*52+'4')
        for t in range(700):
            x=blocks(n,k);y=zipped_raa(x,k)
            nn=n+int(str(n)[::-1])
            assert value(y,k)==nn
            n=nn;num+=1
        print('PASS zipper real orbit radix',10**k,'700 steps and partial-phase changes')
    for k in [2,3]:
        print('sample',10**k,'5994 reverse',zipped_decimal_reverse(blocks(5994,k),k),
              'successor',zipped_raa(blocks(5994,k),k))
    for Q in range(2,151):
        n=int('5'+'99'*Q+'4')
        target=[
          [94]+[99]*(Q-1)+[59],
          [89]+[99]*(Q-1)+[9,1],
          [90,98]+[99]*(Q-1)+[10],
          [91,97]+[99]*(Q-2)+[89,20],
        ]
        for t in range(4):
            assert blocks(n,2)==target[t],(Q,t)
            if t<3:n=value(zipped_raa(blocks(n,2),2),2)
        num+=3
    print('PASS positive base-100 three-edge symbolic corridor Q=2..150')
    print('ALL BLOCK-ZIPPER DECIMAL CONTROL CHECKS PASSED:',num)
if __name__=='__main__':test()

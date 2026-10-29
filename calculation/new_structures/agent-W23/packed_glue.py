#!/usr/bin/env python3
"""W23 dense 48-spaced non-gauge packet gluing, actual Python arbitrary-precision integers."""
import sys,random
sys.set_int_max_str_digits(0)
from bigint_short import B,W,ra,pairs
def realize_packed(M,mask):
    q=M+4
    h=list(B)+list(W)*q+[10,14,1,10]
    for j in range(M):
        if (mask>>j)&1:
            pos=11+48*(2+j)+20
            assert tuple(h[pos:pos+2])==(13,9)
            h[pos:pos+2]=[8,5]
    d=[0]*(2*len(h)-1)
    for i,p in enumerate(h[:-1]):
        d[i]=max(0,p-9);d[-1-i]=min(9,p)
    d[len(h)-1]=5
    return int(''.join(map(str,d[::-1])))
def check(M,masks):
    original=set();p3=n4=None
    for mask in masks:
        x=realize_packed(M,mask)
        assert x not in original
        original.add(x)
        for t in range(4):
            s=str(x)
            assert s!=s[::-1],(M,mask,t)
            if t==3:
                p=pairs(x)
                if p3 is None:p3=p
                else:assert p==p3,(M,mask,'pairs')
            x=ra(x)
        if n4 is None:n4=x
        else:assert x==n4,(M,mask,'integer')
    return dict(M=M,cases=len(original),q=M+4,
                seed_digits=2*(len(B)+48*(M+4)+4)-1,N4_digits=len(str(n4)))
def main():
    print(check(10,range(1<<10)))
    rng=random.Random(20261028)
    masks={0,(1<<128)-1}
    masks.update(rng.getrandbits(128) for _ in range(18))
    print(check(128,sorted(masks)))
    print(check(96,[0,(1<<96)-1,int('aa'*12,16)]))
if __name__=='__main__':main()

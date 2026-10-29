#!/usr/bin/env python3
"""An independent bigint (not digit-list) replay of the N15 decimal seed."""
import sys

def source_digits(h):
    w='A'
    for _ in range(h):
        w=''.join('AB' if c=='A' else 'BA' for c in w)
    P=[4]+[14 if c=='A' else 16 for c in w]
    P+=P[::-1]
    m=len(P)//2
    lo=[1]+[v-9 for v in P[1:m]]
    hi=[3]+[9]*(m-1)
    d=lo+hi[::-1]
    assert all(d[i]+d[-1-i]==P[i] for i in range(len(d)))
    return int(''.join(map(str,d[::-1])))

def check(h=7,n=256):
    x=source_digits(h)
    for t in range(n+1):
        s=str(x)
        assert s!=s[::-1],(h,t)
        if t==n:break
        x+=int(s[::-1])
    print('INDEPENDENT_BIGINT_PASS',h,n,len(str(x)))
if __name__=='__main__':check(int(sys.argv[1]) if len(sys.argv)>1 else 7,int(sys.argv[2]) if len(sys.argv)>2 else 256)

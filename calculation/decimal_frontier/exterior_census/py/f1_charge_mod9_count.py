#!/usr/bin/env python3
"""Count binary carry streams e satisfying the existing charge-closure congruence.
This constrains e, not the overflow stream g alone.
"""
from math import gcd
import sys
def count(p):
    m=gcd(pow(2,p,9)-1,9)
    dp=[1]+[0]*(m-1)
    for t in range(p):
        w=pow(2,p-1-t,m);nxt=[0]*m
        for r,c in enumerate(dp):
            nxt[(r+w)%m]+=c
            nxt[(r-w)%m]+=c
        dp=nxt
    assert sum(dp)==2**p
    return m,dp[0]
if __name__=='__main__':
    for p in range(1,int(sys.argv[1])+1):
        m,c=count(p)
        expected=2**p if p%2 else ((2**p+8)//9 if p%6==0 else (2**p+2)//3)
        assert c==expected,(p,m,c,expected)
        print(p,m,c)

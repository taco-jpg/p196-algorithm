#!/usr/bin/env python3
"""Seed for the independent GMP and schoolbook replay, with no floating point."""
from math import isqrt
import sys
def fl(k,num=0,den=1):
    t=k*den
    return (isqrt(5*t*t)-t+2*num)//(2*den)
def seed(n,num=0,den=1):
    assert n>=2 and 0<=num<den
    s=[fl(i+1,num,den)-fl(i,num,den) for i in range(n)]
    assert all(v in (0,1) for v in s)
    return '9'*n+''.join(str(7+v) for v in reversed(s))
if __name__=='__main__':
    if len(sys.argv) not in (2,4):
        raise SystemExit('usage: make_seed.py WIDTH [PHASE_NUM PHASE_DEN]')
    print(seed(int(sys.argv[1]),int(sys.argv[2]) if len(sys.argv)==4 else 0,
               int(sys.argv[3]) if len(sys.argv)==4 else 1))

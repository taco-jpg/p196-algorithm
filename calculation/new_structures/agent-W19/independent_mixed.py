#!/usr/bin/env python3
"""Independent arbitrary-precision control with unequal positive packet spacers."""
import sys
from make_seed import B,W,C
sys.set_int_max_str_digits(100000)
def make(packets,copies,gaps,mask):
    assert len(gaps)==packets-1 and all(g>0 for g in gaps)
    h=list(B)+list(W)*copies
    for i in range(packets):
        h.extend(C[(mask>>i)&1])
        if i<packets-1:h.extend(W*gaps[i])
    lo=[min(v,9) for v in h]
    hi=[v-x for v,x in zip(h,lo)]
    return int(''.join(str(v) for v in (lo+hi[::-1])[::-1]))
def check(packets,copies,gaps):
    stages=[set() for _ in range(4)]
    for mask in range(1<<packets):
        n=make(packets,copies,gaps,mask)
        for t in range(4):
            s=str(n)
            assert s!=s[::-1] or t==3,('palindrome',mask,t)
            stages[t].add(n)
            if t<3:n+=int(s[::-1])
    sizes=list(map(len,stages))
    assert sizes==[1<<packets,1<<packets,1<<packets,1],sizes
    print('INDEPENDENT_MIXED_PASS',dict(packets=packets,copies=copies,gaps=gaps,distinct_by_time=sizes))
if __name__=='__main__':
    for copies in (0,1,3):check(8,copies,[1,2,3,1,4,2,5])
    for copies in (0,1):check(6,copies,[1,1,1,1,1])

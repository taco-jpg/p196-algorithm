#!/usr/bin/env python3
"""Independent Python integer-reversal oracle for finite X12 dual-clock controls."""
import sys
sys.set_int_max_str_digits(0)
from beat import seed,integer,pairs,splice,normstep

def check(q,r,L):
    p,z=seed(q,r),seed(q,r+1)
    x,y=integer(p),integer(z)
    for t in range(L+1):
        a,b=pairs(x),pairs(y)
        assert a==p and b==z,(q,r,t,'pairword mismatch')
        got=splice(a,b)
        if t<L:assert got is not None,(q,r,t,'premature splice death')
        else:assert got is None,(q,r,t,'missing splice death')
        assert str(x)!=str(x)[::-1] and str(y)!=str(y)[::-1]
        if t==L:break
        x+=int(str(x)[::-1]);y+=int(str(y)[::-1]);p,_=normstep(p);z,_=normstep(z)
    print('PASS independent decimal integers',q,r,L,'states',2*(L+1),flush=True)
for q,r,L in [(1,100,131),(4,500,611),(9,850,1031)]:check(q,r,L)

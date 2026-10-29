#!/usr/bin/env python3
"""Independent physical bigint check at every state of both cone invariants."""
from verify import B,W,template,realize
from cone_certificate import step as central_step,all_u
from outer_clock import step as outer_step
import random

def verify_one(U,C,J,q,k):
    n=realize(template(J,U,C,q,k))
    prefix=B+W*14
    centre=U*100+C+(U*100)[::-1]
    a=len(B)+9*q+len(J)+3*(k-100)
    for t in range(121):
        d=[int(x) for x in str(n)[::-1]]
        p=[d[i]+d[-1-i] for i in range(len(d))]
        assert len(p)==2*a+len(centre)
        assert p[:len(prefix)]==prefix,(t,'outer',J,U,C,q,k)
        assert p[a:len(p)-a]==centre,(t,'centre',J,U,C,q,k)
        if t==120:break
        next_n=n+int(str(n)[::-1])
        true_g=len(str(next_n))-len(str(n))
        prefix,g,_=outer_step(prefix)
        assert true_g==g==(t%4==0),(t,J,U,C,true_g,g)
        centre,change=central_step(centre,g)
        a+=change
        n=next_n
    return 121

if __name__=='__main__':
    import sys
    if hasattr(sys,'set_int_max_str_digits'):sys.set_int_max_str_digits(0)
    count=0
    for C in ([4,4],[4,14,4]):
        for U in all_u():
            for J in ([0]*6,[5,13,0,14,18,7]):
                count+=verify_one(U,C,J,14,100)
    print('REFERENCE verified intermediate states',count)
    rng=random.Random(3712)
    for C in ([4,4],[4,14,4]):
        for U in ([9,0,18],[18,0,9],[9,8,10],[6,9,12]):
            J=[rng.randrange(19) for _ in range(6)]
            for q,k in ((20,80),(40,160),(80,320),(160,640)):
                count+=verify_one(U,C,J,q,max(k,100))
    assert count==18392
    print('TOTAL independently verified physical states',count)

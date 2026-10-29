#!/usr/bin/env python3
"""Independent genuine Python-bigint RAA cross-check at five widths."""
import random,sys
sys.set_int_max_str_digits(0)
from prefix_engine import cone_trace
from carry_prefix import B,W
def word(q,k,J,U,C):
    h=B+W*q+list(J)+list(U)*k
    return h+list(C)+h[::-1]
def physical_integer(coeff):
    n=len(coeff);d=[0]*n
    for i in range(n//2):
        d[i]=min(coeff[i],9);d[n-1-i]=coeff[i]-d[i]
        assert 0<=d[n-1-i]<=9
    if n%2:
        assert coeff[n//2]%2==0
        d[n//2]=coeff[n//2]//2
    assert d[-1]>0
    return int(''.join(map(str,d[::-1])))
def coeff_of_n(n):
    d=[int(x) for x in str(n)[::-1]]
    return [d[i]+d[-1-i] for i in range(len(d))]
def verify(q,k,J,U,C,steps=120):
    init=word(q,k,J,U,C);n=physical_integer(init)
    assert coeff_of_n(n)==init
    gamma=[]
    for t in range(steps):
        prev=len(str(n));s=str(n)
        n=n+int(s[::-1])
        gamma.append(len(str(n))-prev)
    p=coeff_of_n(n);target=word(q,k+5,J,U,C)
    assert len(p)==len(target) and sum(gamma)==steps//4
    diff=next((i for i,(x,y) in enumerate(zip(p,target)) if x!=y),len(p))
    n0,n1,ix,amb,pr=cone_trace(J,U,q,min(50,k),steps)
    assert p[:len(pr)]==list(pr)
    assert diff<len(pr) and diff==ix
    assert not amb
    return diff,len(pr),len(str(n)),''.join(map(str,gamma[:12]))
if __name__=='__main__':
    rng=random.Random(131311)
    N=int(sys.argv[1]) if len(sys.argv)>1 else 30
    for ix in range(N):
        a=2*(ix%10);u=[9,a,18-a];r=(ix//10)%3
        U=u[r:]+u[:r]
        J=[rng.randrange(19) for _ in range(3+(ix%2))]
        C=[4,14,4] if ix%2 else [4,4]
        for q,k in ((14,100),(20,100),(40,160),(80,320),(160,640)):
            result=verify(q,k,J,U,C)
            print('BIGINT_PASS',ix,q,k,U,J,C,result,flush=True)
    print('INDEPENDENT_ALL_PASS',N)

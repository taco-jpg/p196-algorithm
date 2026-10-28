#!/usr/bin/env python3
"""Regression checks for cyclic carry-independent linear charges. Not a census or certificate."""
from math import gcd
from pathlib import Path
from random import Random


def predicted_weights(mod, m, base=10):
    return [[pow(base, j, mod)*z % mod for j in range(m)] for z in range(mod)
            if ((base*base-1)*z) % mod == 0 and (pow(base, m, mod)*z-z) % mod == 0]


def good_by_coefficients(q, mod, gam, base=10):
    m=len(q)
    for j in range(m):
        asc=(q[j]-base*q[(j-1)%m])%mod
        desc=((q[j]-base*q[(j+1)%m]) if gam==0
              else (q[(j+1)%m]-base*q[(j+2)%m]))%mod
        if asc or desc: return False
    return True


def step_cell(P,c,d,gam,base=10):
    m=len(P)
    if gam==0:
        return [2*P[j]+c[j]+d[j]-base*(c[(j+1)%m]+d[(j-1)%m]) for j in range(m)]
    return [P[j]+P[(j-1)%m]+c[j]+d[(j-1)%m]
            -base*(c[(j+1)%m]+d[(j-2)%m]) for j in range(m)]


def check():
    for mod in range(2,402):
        for m in (1,2,3,4,5,6,7,8,11,48):
            qs=predicted_weights(mod,m)
            assert len(qs)==gcd(mod,99 if m%2==0 else 9)
            assert all(good_by_coefficients(q,mod,0) and good_by_coefficients(q,mod,1) for q in qs)
    for base in range(2,27):
        for mod in range(2,81):
            for m in (1,2,3,4,5,6,7,8,48):
                qs=predicted_weights(mod,m,base)
                assert len(qs)==gcd(mod,base*base-1 if m%2==0 else base-1)
                assert all(good_by_coefficients(q,mod,0,base) and
                           good_by_coefficients(q,mod,1,base) for q in qs)
    rng=Random(3196); charges=predicted_weights(99,48)
    for _ in range(20000):
        P=[rng.randrange(19) for _ in range(48)]
        a=[rng.randrange(2) for _ in range(48)]
        d=[rng.randrange(2) for _ in range(48)]
        q=charges[rng.randrange(99)]; g=rng.randrange(2)
        lhs=sum(x*y for x,y in zip(q,step_cell(P,a,d,g)))%99
        rhs=(2 if g==0 else 11)*sum(x*y for x,y in zip(q,P))%99
        assert lhs==rhs
    dat=Path(__file__).resolve().parents[1]/'data'/'lat2.txt'
    v=list(map(int,dat.read_text().split()))
    p,nB,m,b=v[:4]; assert (p,nB,m,b)==(8,11,48,10)
    gam=v[4:4+p]; z=v[4+p:]
    W=[z[t*m:(t+1)*m] for t in range(p)]
    a=[z[p*m+t*m:p*m+(t+1)*m] for t in range(p)]
    assert len(W[-1])==len(a[-1])==48
    for t in range(p):
        old,nxt=W[t],W[(t+1)%p]
        if gam[t]==0:
            d=[(nxt[j]-a[t][j])%2 for j in range(m)]
        else:
            d=[(nxt[(j+1)%m]-old[(j+1)%m]-old[j]-a[t][(j+1)%m])%2 for j in range(m)]
        assert step_cell(old,a[t],d,gam[t])==nxt
        assert all(a[t][(j+1)%m]==int(old[j]+a[t][j]>=10) for j in range(m))
        assert all(d[(j-1)%m]==int(old[j]+d[j]>=10) for j in range(m))
        assert sum(pow(10,j,99)*old[j] for j in range(m))%99==0
    assert pow(22,4,99)==22 and pow(22,96,99)==55
    print('PASS: 400 moduli, bases 2..26, 20,000 updates, rec2 384 bulk cells')


if __name__=='__main__':
    check()

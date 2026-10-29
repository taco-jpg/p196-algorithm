#!/usr/bin/env python3
"""R34: phasewise odd-pair witness for the charge-zero decimal U3 shuttle.

PAPER PROOF: the finite 30-state bulk map is closed for gamma=0 and gamma=1.
A surviving interior U3 copy contains a pair coefficient 9, so no decimal
palindrome can have that pairword. No physical regenerative return is claimed.
"""
G=(1,0,0,0,1,0,0,0,1,0,0,0)
B=(10,4,6,6,7,12,9,16,16,13,0,2,10,17,7,0,18,6,5,18,4,18,14,9,14,8,12,17,10,4,6,4,0,5)
W=(5,18,4,8,1,15,4,0,5)

def carries(u, reverse=False):
    inds=range(len(u)-1,-1,-1) if reverse else range(len(u))
    for seed in (0,1):
        c=seed; buf=[0]*len(u)
        for i in inds:
            buf[i]=c
            c=(u[i]+c)//10
        if c==seed:return buf
    raise AssertionError('no cyclic carry')

def step(u,gamma):
    lo=carries(u);hi=carries(u,True);m=len(u)
    dl=[(u[i]+lo[i])%10 for i in range(m)]
    dh=[(u[i]+hi[i])%10 for i in range(m)]
    return tuple(dl[i]+dh[(i-gamma)%m] for i in range(m))

S={tuple((9,a,18-a)[r:]+(9,a,18-a)[:r]) for a in range(0,19,2) for r in range(3)}

def theorem_finite_check():
    assert len(S)==30
    for a in range(0,19,2):
        u=(9,a,18-a)
        b=(2*a+2)%22
        assert step(u,0)==(9,b,18-b)
        c=(8-a)%20
        assert step(u,1)==(c,18-c,9)
    for u in S:
        assert sum(u)==27 and sum(x==9 for x in u)==1
        for gamma in (0,1):assert step(u,gamma) in S
        z=u;returns=[]
        for t in range(120):
            z=step(z,G[t%12])
            if (t+1)%12==0 and z==u:returns.append(t+1)
        assert returns==[120]
    assert step(W,1)==(10,14,13,12,9,7,10,4,5)
    print('ALL_30_ODD_SAFETY_CLOSED_BOTH_GAMMAS_PASS')

def pair(q,k,u):
    h=list(B)+list(W)*q+[6]+list(u)*k
    return h+[8,8]+h[::-1]

def realize(p):
    n=len(p); assert p==p[::-1];d=[0]*n
    for i in range(n//2):
        hi=min(9,p[i]);d[i]=p[i]-hi;d[n-i-1]=hi
        assert 0<=d[i]<=9
    assert d[-1]>0
    return d

def val(d):
    x=0
    for z in reversed(d):x=10*x+z
    return x

def digits(n):
    v=[]
    while n:
        n,r=divmod(n,10);v.append(r)
    return v

def schoolbook(d):
    n=len(d);c=0;v=[]
    for i in range(n):
        x=d[i]+d[n-1-i]+c
        v.append(x%10);c=x//10
    if c:v.append(c)
    return v

def physical_control():
    # Four independent widths; true bigint + independent schoolbook engine.
    for q in (20,40,80,160):
        u=(9,2,16);k=q;d=realize(pair(q,k,u));v=val(d)
        for t in range(120):
            nxt=schoolbook(d);nv=v+val(d[::-1])
            assert nxt==digits(nv)
            assert len(nxt)-len(d)==G[t%12]
            d,v=nxt,nv
    # Every U row: all 120 physical phases at q=20,k=160;
    # the checked interior block is >=120 cells from either seam.
    q,k=20,160
    for u in S:
        d=realize(pair(q,k,u));z=u
        start=len(B)+9*q+1;probe=start+201
        for t in range(120):
            p=[d[i]+d[-1-i] for i in range(len(d))]
            expect=tuple(z[(probe+i-start)%3] for i in range(3))
            assert tuple(p[probe:probe+3])==expect and 9 in expect
            nxt=schoolbook(d)
            assert len(nxt)-len(d)==G[t%12]
            d=nxt;z=step(z,G[t%12])
    print('ACTUAL_DECIMAL_30_BY_120_PHASE_ODD_WITNESS_PASS')

if __name__=='__main__':
    theorem_finite_check()
    physical_control()

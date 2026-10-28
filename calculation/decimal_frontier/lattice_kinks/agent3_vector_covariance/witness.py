#!/usr/bin/env python3
"""Exact PAPER PROOF arithmetic witness for all-modulus rec2 vector-carry obstruction."""
from pathlib import Path
from math import gcd
import sys
def parse(path):
    nums=list(map(int,Path(path).read_text().split()))
    p,nb,m,b=nums[:4];assert (p,nb,m,b)==(8,11,48,10)
    assert nums[4:12]==[1,0]*4
    x=nums[12:];assert len(x)==8*(2*m+nb)
    W=[x[i*m:(i+1)*m] for i in range(8)]
    cup=[x[8*m+i*m:8*m+(i+1)*m] for i in range(8)]
    return W,cup
def carries(row):
    m=len(row);up=[]
    for initial in (0,1):
        a=[initial]
        for x in row:a.append(int(x+a[-1]>=10))
        if a[-1]==initial:up.append(a[:-1])
    down=[]
    for final in (0,1):
        a=[0]*m;a[-1]=final
        for j in range(m-1,0,-1):a[j-1]=int(row[j]+a[j]>=10)
        if final==int(row[0]+a[0]>=10):down.append(a)
    assert len(up)==len(down)==1
    return up[0],down[0]
def step(row,g):
    a,d=carries(row);m=len(row)
    if not g:
        out=[2*row[i]+a[i]+d[i]-10*(a[(i+1)%m]+d[(i-1)%m]) for i in range(m)]
    else:
        out=[row[i]+row[(i-1)%m]+a[i]+d[(i-1)%m]-10*(a[(i+1)%m]+d[(i-2)%m]) for i in range(m)]
    assert all(0<=x<=18 for x in out)
    return out
def equation(row,g):
    nxt=step(row,g);_,d=carries(row);_,dn=carries(nxt)
    factor=11 if g else 2
    bare=sum(10**j*(nxt[j]-factor*row[j]) for j in range(48))
    coeff=[10**j*(dn[j]-factor*d[j]) for j in range(48)]
    return bare,coeff
def perturb(W,t,i,delta):
    r=W[t].copy();r[i]+=delta;assert 0<=r[i]<=18
    orig=equation(W[t],1-t%2);changed=equation(r,1-t%2)
    return changed[0]-orig[0],[a-b for a,b in zip(changed[1],orig[1])]
def check(path):
    W,cup=parse(path)
    for t in range(8):
        assert step(W[t],1-t%2)==W[(t+1)%8]
        assert carries(W[t])[0]==cup[t]
    a,v=perturb(W,0,47,1)
    assert all(x==0 for x in v) and a==-(10**48-1)
    b,u=perturb(W,0,2,1)
    assert b==0 and u==([0,10]+[0]*46)
    c,w=perturb(W,1,2,1)
    assert c==-990 and w==([0,-30]+[0]*46)
    assert all(3*x+y==0 for x,y in zip(u,w))
    assert gcd(abs(a),abs(c))==99
    print("PASS: 8/8 physical cyclic rec2 bulk steps, 384 row cells and both carry streams")
    print("Witness A: phase0 cell47+1 gives zero vector coefficient and bare=-(10^48-1)")
    print("Witness B: phase0 cell2+1 (bare=0, coeff[1]=10); phase1 cell2+1 (bare=-990, coeff[1]=-30)")
    print("gcd(10^48-1,990)=99; allowed moduli are divisors of 99")
if __name__=="__main__":
    check(sys.argv[1] if len(sys.argv)>1 else str(Path(__file__).with_name("lat2.txt")))

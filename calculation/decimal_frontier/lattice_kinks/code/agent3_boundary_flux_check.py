#!/usr/bin/env python3
"""Reproduce physical-carry moving-centre boundary-flux checks. Standard library only."""
from pathlib import Path
from random import Random

def check(d,b,L):
    n=len(d); h=(n+1)//2; R=h-1; mod=b*b-1
    P=[d[i]+d[-i-1] for i in range(n)]
    c=[0]; O=[]
    for x in P:
        v=x+c[-1]; O.append(v%b); c.append(v//b)
    g=c[-1]
    if g: O.append(g)
    h2=(len(O)+1)//2
    nxt=[O[i]+O[-i-1] for i in range(len(O))]
    q=lambda i:pow(b,i,mod)
    Q=sum(q(i)*P[i] for i in range(L,h))%mod
    Q2=sum(q(i)*nxt[i] for i in range(L,h2))%mod
    dwn=lambda j:c[n-1-j]
    if g==0:
        left=q(L)*(c[L]-b*dwn(L-1))
        rawtop=q(R)*(-b*c[R+1]+dwn(R))
        top=q(R)*((1-b)*c[h] if n%2==0 else c[R]-b*c[R+1])
    else:
        left=q(L)*(P[L-1]+c[L]-b*dwn(L-2))
        rawtop=q(R)*(-b*P[R]-b*c[R+1]+dwn(R-1))
        if n%2==0:
            rawtop+=q(h)*nxt[h]
            top=q(R)*b*O[h]
        else:
            top=q(R)*(-b*P[R]+(1-b)*c[h])
    assert (top-rawtop)%mod==0,(b,n,g,L,'midpoint')
    assert (Q2-(2 if g==0 else b+1)*Q-left-top)%mod==0,(b,n,g,L,'flux')
    return (b,n%2,g)

def run():
    rng=Random(319614); counts={}
    for b in range(2,32):
        for _ in range(3000):
            n=rng.randrange(22,200)
            d=[rng.randrange(b) for _ in range(n)]
            d[-1]=rng.randrange(1,b)
            L=rng.randrange(3,(n+1)//2-4)
            key=check(d,b,L)
            counts[key]=counts.get(key,0)+1
    assert all(counts.get((b,par,g),0)>0 for b in range(2,32) for par in range(2) for g in range(2))
    dat=Path(__file__).resolve().parents[1]/'data'/'lat2.txt'
    v=list(map(int,dat.read_text().split()))
    p,nb,m,b=v[:4]; assert (p,nb,m,b)==(8,11,48,10)
    gam=v[4:4+p]; z=v[4+p:]
    W=[z[t*m:(t+1)*m] for t in range(p)]
    asc=[z[p*m+t*m:p*m+(t+1)*m] for t in range(p)]
    desc=[]
    for t in range(p):
        old,nxt=W[t],W[(t+1)%p]
        if gam[t]==0: d=[(nxt[j]-asc[t][j])%2 for j in range(m)]
        else: d=[(nxt[(j+1)%m]-old[(j+1)%m]-old[j]-asc[t][(j+1)%m])%2 for j in range(m)]
        desc.append(d)
    for L in range(nb+2,nb+2+m):
        idx=lambda i:(i-nb)%m
        left=[]
        for t in range(p):
            X=(asc[t][idx(L)]-10*desc[t][idx(L-1)]) if gam[t]==0 else (W[t][idx(L-1)]+asc[t][idx(L)]-10*desc[t][idx(L-2)])
            left.append(pow(10,L,99)*X%99)
        S=0
        for t in range(192):
            S=((2 if gam[t%8]==0 else 11)*S+left[t%8])%99
        assert S%9==0,(L,S)
    print('PASS: 90,000 real RAA steps, bases 2..31; 48 rec2 cut residues, 192-step mod-9 flux')

if __name__=='__main__':
    run()

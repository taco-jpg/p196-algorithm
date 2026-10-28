#!/usr/bin/env python3
"""Exact all-modulus time-dependent pair-weight and 384 carry weights obstruction."""
from pathlib import Path
from math import gcd
import sys

def load(path):
    raw=list(map(int,Path(path).read_text().split()))
    assert raw[:4]==[8,11,48,10] and raw[4:12]==[1,0]*4
    z=raw[12:]
    assert len(z)==8*(48*2+11)
    return [z[t*48:(t+1)*48] for t in range(8)]

def carries(P):
    n=len(P);au=[];de=[]
    for x in (0,1):
        u=[x]
        for v in P:u.append(int(v+u[-1]>=10))
        if u[-1]==x:au.append(u[:-1])
        d=[0]*n;d[-1]=x
        for j in range(n-1,0,-1):d[j-1]=int(P[j]+d[j]>=10)
        if x==int(P[0]+d[0]>=10):de.append(d)
    assert len(au)==len(de)==1
    return au[0],de[0]

def transition(P,g):
    u,d=carries(P);n=len(P)
    if g==0:
        return [2*P[j]+u[j]+d[j]-10*(u[(j+1)%n]+d[(j-1)%n]) for j in range(n)]
    return [P[j]+P[(j-1)%n]+u[j]+d[(j-1)%n]-10*(u[(j+1)%n]+d[(j-2)%n]) for j in range(n)]

def formal(t,P):
    g=1-t%2;A=11 if g else 2
    T=transition(P,g);_,d=carries(P);_,dn=carries(T)
    coeff={}
    for j in range(48):
        if dn[j]:coeff[('a',(t+1)%8,j)]=10**j*dn[j]
        if d[j]:coeff[('a',t,j)]=-A*10**j*d[j]
    for k,v in [(t,-A*sum(10**j*P[j] for j in range(48))),((t+1)%8,sum(10**j*T[j] for j in range(48)))]:
        coeff[('b',k)]=coeff.get(('b',k),0)+v
    return coeff

def delta(W,t,j,s):
    v=formal(t,W[t]);P=W[t].copy();P[j]+=s
    assert 0<=P[j]<=18
    u=formal(t,P)
    return {k:u.get(k,0)-v.get(k,0) for k in u.keys()|v.keys() if u.get(k,0)!=v.get(k,0)}

def run(path):
    W=load(path)
    for t in range(8):assert transition(W[t],1-t%2)==W[(t+1)%8]
    for t in range(4):
        assert delta(W,t,0,-1)=={('b',(t+1)%8):-(11 if t%2==0 else 2),('b',t):(11 if t%2==0 else 2)}
    assert delta(W,0,47,1)=={('b',0):-11*10**47,('b',1):10**47+1}
    assert delta(W,2,5,1)=={('b',2):-11*10**5,('b',3):11*10**5,('a',3,4):10**4}
    assert delta(W,3,5,1)=={('b',3):-2*10**5,('b',4):-79*10**4,('a',3,4):-2*10**4}
    H=10**48-1
    assert H%2 and H%5 and gcd(H,990000)==99
    for M in (3,9,11,33,99):
        for t in range(8):
            g=1-t%2;A=11 if g else 2
            for j in [-1]+list(range(48)):
                for s in ([0] if j<0 else [-1,1]):
                    P=W[t].copy()
                    if j>=0:
                        P[j]+=s
                        if not 0<=P[j]<=18:continue
                    N=transition(P,g)
                    lhs=sum(pow(10,k,M)*v for k,v in enumerate(N))%M
                    rhs=A*sum(pow(10,k,M)*v for k,v in enumerate(P))%M
                    assert lhs==rhs,(M,t,j,s)
    print('PASS: 8 phases, 4 stable-site witnesses, 3 defect witnesses, 3/9/11/33/99 complete controls')
    print('CERTIFICATE: 11(b1-b0)=0; 2(b2-b1)=0; 11(b3-b2)=0; 2(b4-b3)=0')
    print('CERTIFICATE: (10^47+1)b1-11*10^47*b0=0')
    print('CERTIFICATE: 11*10^5(b3-b2)+10^4*a34=0')
    print('CERTIFICATE: -79*10^4*b4-2*10^5*b3-2*10^4*a34=0')
    print('CONCLUSION: M|(10^48-1), M|99*10^4, gcd=99; beta0=1 => M|99')

if __name__=='__main__':run(sys.argv[1] if len(sys.argv)>1 else str(Path(__file__).with_name('lat2.txt')))

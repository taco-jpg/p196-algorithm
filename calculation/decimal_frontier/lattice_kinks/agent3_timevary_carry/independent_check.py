#!/usr/bin/env python3
"""Independent digit-normalized cyclic rec2 eight-phase witness and controls."""
from pathlib import Path
from random import Random
from math import gcd
import sys
def run(filename):
 raw=[int(s) for s in Path(filename).read_text().split()]
 assert raw[:4]==[8,11,48,10]
 z=raw[12:];W=[z[t*48:(t+1)*48] for t in range(8)]
 def carries(P):
  n=len(P);asc=[];desc=[]
  for a0 in (0,1):
   c=a0;l=[]
   for x in P:l.append(c);c=(x+c)//10
   if c==a0:asc.append(l)
  for c0 in (0,1):
   c=c0;l=[0]*n
   for j in range(n-1,-1,-1):l[j]=c;c=(P[j]+c)//10
   if c==c0:desc.append(l)
  assert len(asc)==len(desc)==1
  return asc[0],desc[0]
 def forward(P,g):
  u,d=carries(P);n=len(P)
  low=[(P[j]+u[j])%10 for j in range(n)]
  high=[(P[j]+d[j])%10 for j in range(n)]
  return [low[j]+high[j if not g else (j-1)%n] for j in range(n)]
 def flux(t,P):
  g=1-t%2;A=11 if g else 2;N=forward(P,g)
  _,c=carries(P);_,dn=carries(N)
  bare=sum(10**j*(N[j]-A*P[j]) for j in range(48));coeff={}
  for j in range(48):
   v=10**j*dn[j]
   if v:coeff[((t+1)%8)*48+j]=v
   v=-A*10**j*c[j]
   if v:coeff[t*48+j]=v
  return bare,coeff
 for t in range(8):assert forward(W[t],1-t%2)==W[(t+1)%8]
 def pert(t,i):
  b,u=flux(t,W[t]);x=W[t].copy();x[i]+=1;B,v=flux(t,x)
  return B-b,{j:v.get(j,0)-u.get(j,0) for j in set(u)|set(v) if v.get(j,0)!=u.get(j,0)}
 a,u=pert(0,47);b,v=pert(2,5);c,w=pert(3,5)
 assert a==1-10**48 and u=={}
 assert b==0 and v=={148:10000}
 assert c==-990000 and w=={148:-20000}
 assert 2*v[148]+w[148]==0 and gcd(-a,-(2*b+c))==99
 rng=Random(3196)
 for _ in range(1200):
  P=[rng.randrange(19) for _ in range(48)]
  for g in (0,1):
   N=forward(P,g)
   for mod in (3,9,11,33,99):
    Q=lambda x:sum(pow(10,j,mod)*x[j] for j in range(48))%mod
    assert Q(N)==(11 if g else 2)*Q(P)%mod
 print("INDEPENDENT PASS: modulo-normalization witness and 2400 positive cyclic controls across divisors of 99")
if __name__=="__main__":
 run(sys.argv[1] if len(sys.argv)>1 else str(Path(__file__).with_name("lat2.txt")))

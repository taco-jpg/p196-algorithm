#!/usr/bin/env python3
"""Exact cyclic rec2 coefficient/carry linear equations for the certificate generator."""
from pathlib import Path
def parse(path):
 a=list(map(int,Path(path).read_text().split()))
 assert a[:4]==[8,11,48,10] and a[4:12]==[1,0]*4
 z=a[12:];assert len(z)==8*(48*2+11)
 W=[z[t*48:(t+1)*48] for t in range(8)]
 cu=[z[8*48+t*48:8*48+(t+1)*48] for t in range(8)]
 return W,cu
def carries(P):
 n=len(P);up=[];down=[]
 for seed in (0,1):
  u=[seed]
  for z in P:u.append(int(z+u[-1]>=10))
  if u[-1]==seed:up.append(u[:-1])
  d=[0]*n;d[-1]=seed
  for j in range(n-1,0,-1):d[j-1]=int(P[j]+d[j]>=10)
  if seed==int(P[0]+d[0]>=10):down.append(d)
 assert len(up)==len(down)==1
 return up[0],down[0]
def step(P,g):
 a,d=carries(P);n=len(P)
 if g==0:
  return [2*P[j]+a[j]+d[j]-10*(a[(j+1)%n]+d[(j-1)%n]) for j in range(n)]
 return [P[j]+P[(j-1)%n]+a[j]+d[(j-1)%n]-10*(a[(j+1)%n]+d[(j-2)%n]) for j in range(n)]
def signature(t,P):
 A=11 if t%2==0 else 2;N=step(P,1-t%2);_,d=carries(P);_,dn=carries(N);r={}
 def add(i,x):
  z=r.get(i,0)+x
  if z:r[i]=z
  elif i in r:del r[i]
 for j in range(48):
  add(((t+1)%8)*48+j,N[j]);add(t*48+j,-A*P[j])
  add(384+((t+1)%8)*48+j,dn[j]);add(384+t*48+j,-A*d[j])
 return r
def row(W,tag):
 t,j,s1,s2=tag;ref=signature(t,W[t]);P=W[t].copy()
 if j>=0:
  P[j]+=s1
  if s2:P[(j+1)%48]+=s2
  assert all(0<=v<=18 for v in P)
 z=signature(t,P)
 if j>=0:z={i:z.get(i,0)-ref.get(i,0) for i in z.keys()|ref.keys()}
 z={i:v for i,v in z.items() if v}
 fixed=z.pop(0,0)
 return {i-1:v for i,v in z.items()},-fixed
def all_tags(W):
 for t in range(8):
  yield (t,-1,0,0)
  for j in range(48):
   for s in (-1,1):
    if 0<=W[t][j]+s<=18:yield (t,j,s,0)
  for j in range(48):
   for s in (-1,1):
    for z in (-1,1):
     if 0<=W[t][j]+s<=18 and 0<=W[t][(j+1)%48]+z<=18:yield (t,j,s,z)

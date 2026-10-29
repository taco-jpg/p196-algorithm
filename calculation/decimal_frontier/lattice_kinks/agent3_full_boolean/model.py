#!/usr/bin/env python3
"""All 64 local Boolean functions on six adjacent cyclic decimal carry/parity bits."""
from pathlib import Path
from itertools import product
HERE=Path(__file__).resolve().parent
z=list(map(int,(HERE/'lat2.txt').read_text().split()))
assert z[:12]==[8,11,48,10,1,0,1,0,1,0,1,0]
W=[z[12+48*t:12+48*(t+1)] for t in range(8)]
EVAL=[sum(1<<m for m in range(64) if (m&bits)==m) for bits in range(64)]

def carries(P):
 n=len(P);A=[];D=[]
 assert n==48 and all(0<=x<=18 for x in P) and any(x!=9 for x in P)
 for seed in (0,1):
  a=[seed]
  for x in P:a.append(int(x+a[-1]>=10))
  if a[-1]==seed:A.append(a[:-1])
  d=[0]*n;d[-1]=seed
  for j in range(n-1,0,-1):d[j-1]=int(P[j]+d[j]>=10)
  if seed==int(P[0]+d[0]>=10):D.append(d)
 assert len(A)==len(D)==1
 return A[0],D[0]

def step(P,g):
 a,d=carries(P);n=len(P)
 if g==0:return [2*P[j]+a[j]+d[j]-10*(a[(j+1)%n]+d[(j-1)%n]) for j in range(n)]
 return [P[j]+P[(j-1)%n]+a[j]+d[(j-1)%n]-10*(a[(j+1)%n]+d[(j-2)%n]) for j in range(n)]

def feat(P):
 a,d=carries(P);n=len(P);z=0
 for j in range(n):
  k=(j+1)%n
  bits=(P[j]&1)|((P[k]&1)<<1)|(a[j]<<2)|(d[j]<<3)|(a[k]<<4)|(d[k]<<5)
  z^=EVAL[bits]
 return z

def cov(t,P):
 v=feat(step(P,1-t%2))<<(64*((t+1)%8))
 if t%2==0:v^=feat(P)<<(64*t)
 return v

def tags():
 for t in range(8):
  yield (t,-1,0,0)
  for j in range(48):
   for s in (-1,1):
    if 0<=W[t][j]+s<=18:yield (t,j,s,0)
  for j in range(48):
   for s,u in product((-1,1),repeat=2):
    if 0<=W[t][j]+s<=18 and 0<=W[t][(j+1)%48]+u<=18:yield (t,j,s,u)

def tagged(tag):
 t,j,s,u=tag;P=W[t].copy()
 if j>=0:
  P[j]+=s
  if u:P[(j+1)%48]+=u
 return cov(t,P)

def add(piv,v):
 while v:
  k=v.bit_length()-1
  if k in piv:v^=piv[k]
  else:piv[k]=v;return True
 return False

def rank(rows):
 piv={}
 for v in rows:add(piv,v)
 return len(piv)

def kernel(piv,n):
 keys=set(piv)
 for free in range(n):
  if free in keys:continue
  v=1<<free
  for k in sorted(keys):
   if (v&piv[k]).bit_count()%2:v^=1<<k
  assert all((v&row).bit_count()%2==0 for row in piv.values())
  yield v
